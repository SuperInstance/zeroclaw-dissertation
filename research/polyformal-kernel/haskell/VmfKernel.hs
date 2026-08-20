-- Polyformal vMF kernel — Haskell port (base only, no aeson, no hmatrix).
--
-- Implements the three functions of SPEC.md:
--   A7(k)     — closed-form half-integer Bessel ratio I_{7/2}/I_{5/2} via sinh/cosh
--   vmf_fit   — (mu_hat, kappa) MLE via Banerjee init + Newton solve, jackknife SE
--   edge      — field step between two fits
--
-- No external vMF/Bessel libraries — sinh/cosh + Newton, base only.
-- Differential test: Test.hs (reads ../golden.json + ../inputs.json).
--
-- Run:  runghc Test.hs   (from haskell/)

module VmfKernel
  ( d, kmax, nmin, rhomax
  , a7, vmfFit, edge
  , Fit(..), Edge(..)
  ) where

import Data.List (foldl', foldl1')

type Vec = [Double]

-- ---------- SPEC §0: constants ----------
d :: Int
d = 7                     -- dimension of the field space (S^6 ⊂ R^7)

kmax :: Double
kmax = 500.0              -- κ saturation cap

nmin :: Int
nmin = 10                 -- below this many windows, κ is not identifiable

rhomax :: Double
rhomax = 0.999            -- ρ clamp (unclipped Banerjee init overflows sinh)

-- ---------- SPEC §1: A7 ----------
a7 :: Double -> Double
a7 k
  | k < 0.5 = k / 7.0     -- leading Taylor term; closed form cancels for small κ
  | otherwise =
      let s = sinh k
          c = cosh k
          k2 = k * k
      in ((1.0 + 15.0 / k2) * c - (6.0 / k + 15.0 / (k2 * k)) * s)
       / ((1.0 + 3.0 / k2) * s - (3.0 / k) * c)

clip :: Double -> Double -> Double -> Double
clip x lo hi = max lo (min hi x)

norm :: Vec -> Double
norm v = sqrt (sum (map (^ 2) v))

-- ---------- SPEC §2: vmf_fit ----------
data Fit = Fit
  { muHat      :: Vec
  , fitKappa   :: Double
  , fitRho     :: Double
  , warmthVmf  :: Double
  , muSe       :: Double
  , fitN       :: Int
  , saturated  :: Bool
  } deriving (Show)

-- Component-wise mean of a list of vectors.
meanRows :: [Vec] -> Vec
meanRows [] = error "meanRows: empty input"
meanRows xs = map (/ fromIntegral (length xs)) (foldl1' (zipWith (+)) xs)

-- zs: list of n 7-vectors; warm: the fixed 7-vector WARM from golden.json.
-- Returns Just Fit, or Nothing when unidentifiable/isotropic — never a fake number.
vmfFit :: Vec -> [Vec] -> Maybe Fit
vmfFit warm zs
  | n < nmin = Nothing
  | otherwise =
      let rows = map renorm zs
          r = meanRows rows
          rho = min (norm r) rhomax
      in if rho < 1e-12
         then Nothing                                   -- isotropic — no mean direction
         else
           let mh = map (/ rho) r                       -- mean direction
               -- Banerjee et al. init, clipped to [1e-6, KMAX]
               kappa0 = clip (rho * (fromIntegral d - rho * rho) / (1.0 - rho * rho)) 1e-6 kmax
               -- Newton solve on A7(kappa) = rho, g = 1 - A7² - (D-1)·A7/κ
               kappa = newton rho kappa0
               -- warmth = WARM · μ̂
               warmth = sum (zipWith (*) warm mh)
               -- jackknife SE(μ̂): leave-one-out mean directions, renormalized
               jks = jackknives rows
               jm = meanRows jks
               acc = sum [ sum (zipWith (\a b -> (a - b) ^ 2) jk jm) | jk <- jks ]
               muSe = sqrt (fromIntegral (n - 1) / fromIntegral n * acc)
               -- saturation flag
               sat = rho >= rhomax || kappa >= kmax
           in Just Fit { muHat = mh, fitKappa = kappa, fitRho = rho
                       , warmthVmf = warmth, muSe = muSe, fitN = n
                       , saturated = sat }
  where
    n = length zs
    renorm row = let nr = norm row in map (/ nr) row   -- defensive renormalization
    newton r0 = go (0 :: Int)
      where
        go it k
          | it >= 60 = k
          | otherwise =
              let a = a7 k
                  g = 1.0 - a * a - fromIntegral (d - 1) * a / k
                  step = (a - r0) / g
                  k' = clip (k - step) 1e-6 kmax
              in if abs g < 1e-12 || abs step < 1e-9 then k' else go (it + 1) k'
    jackknives rows' =
      [ let m = map (/ fromIntegral (n - 1))
                  (foldl1' (zipWith (+)) (take i rows' ++ drop (i + 1) rows'))
            nm = norm m
        in map (/ nm) m
      | i <- [0 .. n - 1] ]

-- ---------- SPEC §3: edge ----------
data Edge = Edge
  { dMu       :: Double
  , dWarmth   :: Double
  , dLogKappa :: Double
  , isReal    :: Bool
  } deriving (Show)

edge :: Fit -> Fit -> Edge
edge fb fa =
  let dm = norm (zipWith (-) (muHat fa) (muHat fb))
      dw = warmthVmf fa - warmthVmf fb
      dlk = log (fitKappa fa / fitKappa fb)
      -- db_factor = 2.0 — the drift deadband
      real = dm > 2.0 * max (muSe fb) (muSe fa)
  in Edge dm dw dlk real
