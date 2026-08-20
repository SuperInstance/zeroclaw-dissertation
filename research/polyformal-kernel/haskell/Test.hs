-- Polyformal vMF kernel — Haskell differential test.
--
-- Reads ../golden.json + ../inputs.json and asserts SPEC §4 tolerances:
--   A7 ≤ 1e-9; fit values ≤ 1e-6; edge ≤ 1e-6; n == 30; saturated == false; real == false.
-- The second fit in `edge` is vmf_fit on zs + 0.05 element-wise (SPEC §4).
--
-- No aeson dependency: golden.json/inputs.json are flat, so numbers are
-- extracted with a tiny scanner (base only, same approach as the C++ port).
--
-- Run:  runghc Test.hs   (from haskell/)

module Main (main) where

import Data.Char (isDigit)
import Data.IORef
import Data.List (isPrefixOf, tails)
import System.Exit (exitFailure, exitSuccess)
import Text.Printf (printf)
import Text.Read (readMaybe)

import VmfKernel

-- ---------- minimal JSON number extraction (base only) ----------
numbersAfter :: String -> String -> Int -> [Double]
numbersAfter text key count =
  let pat = "\"" ++ key ++ "\""
      rest = case dropWhile (not . isPrefixOf pat) (tails text) of
               [] -> error ("key not found: " ++ key)
               (t : _) -> drop (length pat) t
  in take count (scanNumbers rest)

scanNumbers :: String -> [Double]
scanNumbers s =
  let s' = dropWhile (\c -> not (isDigit c || c == '-' || c == '+')) s
  in case s' of
       [] -> []
       _ ->
         let (tok, rest) = span (\c -> isDigit c || c `elem` ("-+eE." :: String)) s'
         in case readMaybe tok :: Maybe Double of
              Just x  -> x : scanNumbers rest
              Nothing -> scanNumbers rest

-- ---------- SPEC §4: differential test ----------
main :: IO ()
main = do
  golden <- readFile "../golden.json"
  inputs <- readFile "../inputs.json"
  failures <- newIORef (0 :: Int)

  let check name got want tol = do
        let err = abs (got - want)
        if err > tol
          then do
            printf "FAIL %s: got %.12f want %.12f (err %.3e > %g)\n" name got want err tol
            modifyIORef' failures (+ 1)
          else printf "ok   %s: %.12f (err %.3e)\n" name got err

  -- --- A7 ---
  let kappas = numbersAfter golden "kappas" 11
      values = numbersAfter golden "values" 11
  mapM_ (\(k, v) -> check ("A7(" ++ show k ++ ")") (a7 k) v 1e-9) (zip kappas values)

  -- --- inputs ---
  let flat = numbersAfter inputs "z" (30 * d)
      zs = [ take d (drop (i * d) flat) | i <- [0 .. 29] ]
      warm = numbersAfter golden "WARM" d

  -- --- vmf_fit on zs ---
  case vmfFit warm zs of
    Nothing -> do
      putStrLn "FAIL vmf_fit returned Nothing on golden input"
      exitFailure
    Just fb -> do
      let g_kappa = head (numbersAfter golden "kappa" 1)
          g_rho = head (numbersAfter golden "rho" 1)
          g_warmth = head (numbersAfter golden "warmth_vmf" 1)
          g_mu_se = head (numbersAfter golden "mu_se" 1)
          g_mu = numbersAfter golden "mu_hat" d
      check "kappa" (fitKappa fb) g_kappa 1e-6
      check "rho" (fitRho fb) g_rho 1e-6
      check "warmth_vmf" (warmthVmf fb) g_warmth 1e-6
      check "mu_se" (muSe fb) g_mu_se 1e-6
      let mu_err = maximum (zipWith (\a b -> abs (a - b)) (muHat fb) g_mu)
      if mu_err > 1e-6
        then do
          printf "FAIL mu_hat: max abs err %.3e\n" mu_err
          modifyIORef' failures (+ 1)
        else printf "ok   mu_hat: max abs err %.3e\n" mu_err
      if fitN fb /= 30
        then do
          printf "FAIL n: %d != 30\n" (fitN fb)
          modifyIORef' failures (+ 1)
        else putStrLn "ok   n == 30"
      if saturated fb
        then do
          putStrLn "FAIL saturated: expected false"
          modifyIORef' failures (+ 1)
        else putStrLn "ok   saturated == false"

      -- --- edge: second fit on zs + 0.05 element-wise ---
      let zs2 = map (map (+ 0.05)) zs
      case vmfFit warm zs2 of
        Nothing -> do
          putStrLn "FAIL vmf_fit returned Nothing on shifted input"
          exitFailure
        Just fa -> do
          let e = edge fb fa
          check "edge.d_mu" (dMu e) (head (numbersAfter golden "d_mu" 1)) 1e-6
          check "edge.d_warmth" (dWarmth e) (head (numbersAfter golden "d_warmth" 1)) 1e-6
          check "edge.d_log_kappa" (dLogKappa e) (head (numbersAfter golden "d_log_kappa" 1)) 1e-6
          if isReal e
            then do
              putStrLn "FAIL edge.real: expected false"
              modifyIORef' failures (+ 1)
            else putStrLn "ok   edge.real == false"

          -- --- summary ---
          putStrLn ""
          printf "actual values: kappa=%.6f rho=%.6f warmth=%.6f\n" (fitKappa fb) (fitRho fb) (warmthVmf fb)
          printf "golden values: kappa=%.6f rho=%.6f warmth=%.6f\n" g_kappa g_rho g_warmth

          nfail <- readIORef failures
          if nfail == 0
            then do
              putStrLn "PASS: all differential checks within SPEC §4 tolerances"
              exitSuccess
            else do
              printf "FAIL: %d check(s) failed\n" nfail
              exitFailure
