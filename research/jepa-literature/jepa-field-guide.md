# JEPA — A Field Guide for the Dissertation

*Compiled by the advisor's research subagent for ZeroClaw, 2026-08-19/20. Every load-bearing citation below was verified against arXiv/OpenReview metadata on 2026-08-20 (arXiv Atom API + OpenReview); items I could NOT verify to bibliographic certainty are flagged in §9, per the convention in `related-work.md`. This file is the literature-side complement to `research/doctrine/nurse-jepa.md` (advisor doctrine) and `research/skills/jepa-rag-reference.md` (what the fleet ships); it exists so the dissertation can cite the real field, not the fleet's internal sketch of it.*

---

## 0. The one-paragraph definition

**JEPA (Joint-Embedding Predictive Architecture)** is a self-supervised learning architecture in which an encoder maps an input to a latent representation, a predictor network maps a *context* representation to its estimate of a *target* representation, and training minimizes the discrepancy between predicted and actual target representations — **both sides live in embedding space; neither the input nor the target is ever reconstructed in pixel/token space** (LeCun, 2022, OpenReview position paper, v0.9.2, 27 June 2022 — the source document of the term). The prediction target is produced by a second encoder (the *target encoder*), typically a stop-gradient, exponential-moving-average copy of the context encoder, because a trivial constant solution otherwise exists and must be suppressed (§3). Because the target itself is learned, JEPA can *choose what to make predictable* — it discards unpredictable surface detail and keeps predictable structure — which is the entire epistemic bet: **prediction in representation space buys abstraction that prediction in input space cannot afford** (LeCun 2022; Dawid & LeCun 2023; instantiated for images in Assran et al., CVPR 2023, and video in Bardes et al., 2024).

The lineage in one line: contrastive prediction in latent space (van den Oord et al. 2018) → latent-target self-distillation without negatives (Grill et al., NeurIPS 2020; Chen & He, CVPR 2021; Baevski et al. 2022) → formalized as a world-model architecture with energy-based semantics (LeCun 2022) → scaled to images (I-JEPA, CVPR 2023), video (V-JEPA 2024, V-JEPA 2 2025), audio (A-JEPA 2023), and, most recently and provisionally, language (LLM-JEPA, VL-JEPA 2025).

---

## 1. LeCun (2022): the proposal, precisely

**Citation:** Y. LeCun, "A Path Towards Autonomous Machine Intelligence," OpenReview position paper, id `BZ5a1r-kVsf`, Version 0.9.2, June 27, 2022. (Related-work entry B3 flags "exact version flagged below" — resolved: v0.9.2, 2022-06-27. Companion formalization: A. Dawid & Y. LeCun, "Introduction to Latent Variable Energy-Based Models," arXiv:2306.02572, 2023 — Les Houches lectures.)

### 1.1 The problem the paper poses

Not "how do we learn better image features" but: how could a system learn a **world model** — an internal predictor of how the world responds to observation and action — from observation alone, mostly without supervision, and plan with it? The three named challenges: learn to represent/predict/act largely by observation; make reasoning and planning compatible with gradient-based learning; do it hierarchically, at multiple abstraction levels and time scales.

### 1.2 The cognitive architecture

The proposal (a blueprint, not an implementation) is a set of differentiable modules: **perception**, **world model**, **cost** (including intrinsic motivation), **actor**, **short-term memory**, and a **configurator** that wires the rest for the task at a given moment. The actor plans by *back-propagating gradients through the frozen world model* to minimize the cost module's output over imagined action sequences — planning-as-inference, not policy learning. The world model is the load-bearing module, and JEPA is its proposed form.

### 1.3 JEPA's place in it

The world model takes the current state representation sₓ (and, in the full proposal, an action aₜ and a latent z), and a **predictor** outputs ŷ, an estimate of the representation s_y of the *next* observation y. The energy to minimize is the discrepancy:

> **F(x, y) = D(s_y, ŷ)**, with ŷ = Pred(s_x, a, z)

where s_x = enc(x), s_y = enc(y), D a distance (typically L2/L1), and z an optional latent variable that indexes *multiple plausible futures* (the latent-variable form handles multimodal prediction — §1.5).

### 1.4 The trichotomy — where JEPA sits, and what it is NOT

LeCun's architecture taxonomy (2022, §2; elaborated in Dawid & LeCun 2023):

| Family | What is predicted | Training signal | Pathology it risks |
|---|---|---|---|
| **Generative** (autoregressive, autoencoding, diffusion) | the input itself (pixels, tokens) | reconstruction in input space | wastes capacity on unpredictable detail; deterministic predictors average multimodal futures into mush |
| **Contrastive** (InfoNCE family) | a discrimination (is this pair compatible?) | energy pushed down on compatible pairs, up on incompatibles | needs negatives and hard-negative mining; energy landscape design; does not by itself learn to *predict* |
| **Joint-embedding** (JEPA family) | the **representation** of the target | minimize D(s_y, ŷ) while preventing collapse | **collapse** — the trivial solution (§3) |

So: **JEPA ≠ generative** because it never synthesizes the input; the target encoder decides what part of y is even representable, hence predictable. **JEPA ≠ contrastive** because it needs no negatives — compatibility is enforced by prediction accuracy in latent space plus anti-collapse machinery, not by repulsion. Energy-based models are the *parent formalism*: JEPA's F(x,y) is an (unnormalized) EBM energy; inference over futures = minimize F over y (and z); the contrastive and generative families are alternative ways to shape the same energy surface.

### 1.5 Why latent-space prediction — the two arguments in the paper

1. **The abstraction argument.** A predictor made to output pixels must account for every bit of the target, including the intrinsically unpredictable parts (exact texture, noise, phrasing). A predictor made to output a *learned representation* can be good at the parts of the world that are predictable and let the target encoder *discard the rest*. "Prediction in representation space" is thus a built-in information filter — the model allocates capacity to structure, not surface.
2. **The multimodality argument.** If the future is stochastic and the predictor is deterministic in input space, the best pixel-space prediction is the *average over modes* — the classic blurry-frame problem. In latent space, a latent variable z can index the mode ("the ball went left / right"), and the energy F(x, y, z) stays low on each mode without ever averaging them.

### 1.6 H-JEPA (hierarchical JEPA)

The full proposal stacks JEPA predictors: a low level predicts representations seconds ahead; higher levels predict the *trajectories of lower-level representations* over longer horizons, with latent variables absorbing what cannot be predicted deterministically. Multiple abstraction levels × multiple time scales, steered by the configurator. **As of 2025, H-JEPA remains a proposal** — V-JEPA 2 (§4.3) is the largest realized piece (flat, action-conditioned), and no system ships the full hierarchy. Cite it as vision, not result.

---

## 2. What came before, in one breath (so the dissertation doesn't over-credit 2022)

- **Contrastive Predictive Coding** — van den Oord, Li, Vinyals, arXiv:1807.03748 (2018): predict future *latents* of a sequence from context latents, trained with the InfoNCE contrastive loss. Latent prediction with negatives; the direct ancestor of the "predict representation" idea.
- **BYOL** — Grill, Strub, Altché, Tallec, Richemond, et al., NeurIPS 2020 (arXiv:2006.07733): online network predicts the *target-network representation* of another view; target = EMA of online; **no negatives**. First large-scale demonstration that latent-target prediction + asymmetry alone suffices.
- **SimSiam** — X. Chen & K. He, CVPR 2021 (arXiv:2011.10566): strips even the EMA; shows a **stop-gradient alone** prevents collapse. The minimal proof that asymmetry, not momentum, is the active ingredient.
- **data2vec** — Baevski, Hsu, Xu, Babu, Gu, Auli, arXiv:2202.03555 (2022): one recipe (masked view → predict full-input latent, EMA teacher, regression loss) across speech, vision, language. The first *cross-modal* latent-target method; conceptually the nearest ancestor of I-JEPA.
- **Masked Autoencoders** — He, Chen, Xie, Li, Dollár, Girshick, CVPR 2022 (arXiv:2111.06377): the *pixel-space* twin of I-JEPA (same masking, reconstructs pixels). Every JEPA paper positions against it; the latent-vs-pixel comparison is now a standard experimental axis.

LeCun 2022 is the *systematization* — the EBM framing, the world-model architecture, the trichotomy, the hierarchy — not the first instance of latent-target training. Say exactly that when citing.

---

## 3. The objective, and the collapse problem (the math, not the hand-waving)

### 3.1 The trivial solution

Let the loss be L = 𝔼 D(s_y, Pred(s_x)). If s_y were fixed, this is an ordinary regression and cannot collapse. But in a joint-embedding architecture **s_y is itself produced by a trained encoder**, so the learner controls both sides. The global minimum is then degenerate: make the encoder a constant function, enc(·) = c for all inputs. Prediction error is exactly zero; nothing was learned. Two named forms (Jing, Vincent, LeCun, Tian, ICLR 2022, arXiv:2110.09348):

- **Complete collapse:** all embeddings → one point.
- **Dimensional collapse:** embeddings span only a low-rank subspace — per-dimension variance dies in some coordinates; information crams into a few directions. Happens *even with contrastive losses*, driven by dominant perturbation directions of the encoder.

### 3.2 The honest statement about "predict latent, not pixels"

The dissertation's internal shorthand — "predict latent, not pixels, prevents collapse" — has the causality backwards and should not be quoted that way in front of a committee. Correct statement:

- **Pixel-space targets cannot collapse** because the target is *anchored in the data*: a constant output is a catastrophically bad reconstruction of non-constant pixels. Reconstruction buys collapse-immunity for free — and pays for it by forcing the representation to support every unpredictable bit (LeCun's abstraction argument, §1.5).
- **Latent-space targets are collapse-prone by construction** — the anchor is learned, so it can drift. JEPA accepts this liability *deliberately*, as the purchase price of abstraction: the target encoder gets to decide what is predictable, and the anti-collapse machinery (§3.3) forces it to keep deciding on informative grounds.
- Net: "predict latent, not pixels" **purchases abstraction at the cost of a collapse liability, which the training recipe then services**. That is the design trade, and it is the single most examinable sentence in this guide.

### 3.3 The fix families (all of them, with mechanisms)

1. **Negatives (contrastive).** Push energy up on incompatible pairs (van den Oord et al. 2018; SimCLR lineage). Cost: negative mining, batch size, and — per Jing et al. 2022 — still permits *dimensional* collapse. JEPA's defining move is to refuse this family.
2. **Asymmetry (EMA + stop-gradient + predictor).** The BYOL/SimSiam/data2vec/I-JEPA recipe: target encoder receives no gradient (stop-grad); its weights are an EMA of the online encoder; only the online side sees the loss through the predictor. The theory (Tian, Chen & Ganguli, ICML 2021, arXiv:2102.06810 — the DirectPred paper) analyzes the linear case: with a *trainable* predictor and stop-grad, the collapsed fixed point becomes unstable under gradient flow when the predictor's spectrum outruns the encoder's feature decay — the predictor amplifies cross-feature variance differences, making collapse dynamically repulsive rather than attractive. Their DirectPred sets the linear predictor in closed form from feature-covariance eigenvectors and still works, which pins the mechanism to covariance structure, not to some mystical property of momentum. EMA (vs. plain stop-grad, SimSiam) buys smoothness of the target, not collapse immunity per se.
3. **Variance–covariance regularization (no asymmetry needed).**
   - **VICReg** — Bardes, Pujol, Babaeizadeh, Vincent, LeCun, Ballas (ICLR 2022; arXiv:2105.04906 — see §9 author-list flag): adds to the invariance term a **hinge on per-dimension standard deviation**, v(Z) = (1/d) Σⱼ max(0, γ − √(Var(Zⱼ)+ε)) — a hard floor: no embedding dimension may die — plus a **covariance term** c(Z) = (1/d) Σ_{i≠j} [ZᵀZ]_{ij}² penalizing off-diagonal correlation, i.e., explicit decorrelation. Collapse becomes *impossible by constraint*, not by dynamics.
   - **Barlow Twins** — Zbontar, Jing, Misra, LeCun, Deny, ICML 2021 (arXiv:2103.03230): make the cross-correlation matrix between the two branches' normalized outputs the identity: L = Σᵢ (1 − Cᵢᵢ)² + λ Σ_{i≠j} Cᵢⱼ². Same two demands (per-dimension variance = 1; dimensions decorrelated) written as one matrix identity. Named for H. Barlow's redundancy-reduction principle from neuroscience.
   - **Whitening (W-MSE)** — Ermolov, Siarohin, Sangineto, Sebe, ICML 2021 (arXiv:2007.06346): whiten the batch's embeddings (Cholesky of inverse covariance) before the MSE, so the *batch* is forced onto a sphere; collapse has no fixed point under the transform.
4. **Distillation/clustering asymmetries.** DINO (Caron et al., ICCV 2021, arXiv:2104.14294): teacher = EMA centering + sharpening; collapse suppressed by centering operations. Listed because LeCun 2022 groups it among joint-embedding anti-collapse strategies.

I-JEPA and V-JEPA use **family 2** (EMA target encoder + stop-grad + trainable predictor, L2 resp. L1 loss). Some video variants (e.g., VJ-VCR) use **family 3** (VICReg variance–covariance on the top layer) instead — the fixes are interchangeable parts.

### 3.4 Practical collapse telemetry

Dimensional collapse is *quiet* — loss goes to zero exactly as designed. Field practice monitors representation health independently: per-dimension standard deviations, and the **effective rank** of the embedding matrix (spectral entropy of the singular-value distribution). If effective rank trends toward 1 while loss falls, the model is succeeding at nothing. (No canonical citation needed; this is standard practice — but see Jing et al. 2022 for the dynamics and §7.5 for why the fleet already believes it.)

---

## 4. The instantiations, and what each contributed

### 4.1 I-JEPA — images (Assran, Duval, Misra, Bojanowski, Vincent, Rabbat, LeCun, Ballas; CVPR 2023; arXiv:2301.08243)

- **Task:** from one visible *context block* of an image, predict the representations of several *target blocks* (other regions) in the same image. Target representations come from the EMA target encoder run on the target regions; the context encoder sees only the context block; a lightweight ViT predictor outputs per-patch latents for each target block; loss = L2 between predicted and target patch representations.
- **The contribution that matters for us:** the masking design is the abstraction dial. Target blocks must be **large-scale (semantic)**; context must be **spatially distributed and informative** — and crucially, the context has the target-block-interior masked out of it (no leakage). The paper's attenuation study shows: larger target blocks → representations tuned to semantics (object-level, depth, counting); smaller targets → low-level texture features. **The unit you predict determines the abstraction you learn.** No hand-crafted augmentations anywhere — the corruption is masking, not crop-and-recolor.
- **Scale datum:** ViT-H/14, ImageNet-1K, 16 A100s, <72 h. Strong linear-probe, counting, depth.

### 4.2 V-JEPA — video (Bardes, Garrido, Ponce, X. Chen, Rabbat, LeCun, Assran, Ballas; arXiv:2404.08471, Feb 2024; remained a preprint — see §9 flag on venue)

- **Task:** same recipe over 3D spatio-temporal tubes: encode a temporally-conditioned masked video (the context), predict the EMA-encoded representations of the masked-out spatio-temporal tubes. Trained on 2M public videos, no image init, no text, no negatives, no reconstruction.
- **Two contributions to take:**
  1. **Latent prediction works on *dynamics*, not just appearance.** ViT-H/16 frozen-backbone: 81.9% K400 (action), 72.2% Something-Something-v2 (motion-heavy), 77.9% ImageNet-1K (appearance transfer from video alone). The representation carries *what happens*, which is the property any "temperature dynamics" model needs.
  2. **The frozen-evaluator protocol.** All headline numbers are probes on a frozen backbone (linear or attentive probe, no finetuning) — the field's standard answer to "how do you measure a representation without teaching it the test?" (§7.4 maps this onto the dissertation's blind reader-delta test.)
- **Masking finding:** temporal masking (hiding time extents) matters more than spatial masking — the *when* of the cut carries the learnable signal. Related-work B3's "V-JEPA year/authors lower-confidence" is resolved: 2024, Bardes et al., as above.

### 4.3 The world-model turn: IWM and V-JEPA 2

- **Image World Models** — Garrido, Assran, Ballas, Bardes, Najman, LeCun (arXiv:2403.00504, 2024): generalizes the JEPA prediction task from *masking* to *transformations* — predict the latent of the same image under a global photometric transformation, given the transformation. Findings: a JEPA can be tuned between **invariant** (contrastive-like: transformation-blind) and **equivariant** (predictive: transformation-aware) representations by controlling conditioning, prediction difficulty, and predictor capacity — and the **world model itself** (the predictor) can be finetuned into a task solver. The phrase to cite: *the abstraction level of a JEPA's representations is a controllable dial, and the predictor is a reusable world model.*
- **V-JEPA 2 / V-JEPA 2-AC** — Assran, Bardes, Fan, Garrido, et al. (incl. LeCun; FAIR + Mila), arXiv:2506.09985, June 2025: pre-train action-free JEPA on >1M hours of video; then **post-train an action-conditioned predictor (V-JEPA 2-AC) on <62 h of unlabeled robot trajectories** (Droid); zero-shot planning by gradient descent through the latent world model onto image goals, deployed on Franka arms (65–80% pick/place success) with zero environment-specific data. For the dissertation: the existence proof that (a) latent prediction pre-training transfers to *action and intervention* questions, and (b) the action-conditioning can be added *after* representation learning — the predictor is where agency enters, not the encoder.

### 4.4 Audio — the design-transfer caution

- **A-JEPA** — Fei, Fan, Huang, arXiv:2311.15830 (2023): I-JEPA over mel-spectrogram patches; the transfer is *not* free — random image-style block masking underperforms **time-frequency-aware curriculum masking** (spectrograms are locally correlated in both axes; naive blocks are trivially predictable from neighbors). SOTA on several audio/speech classification tasks without external supervision.
- **Riou, Lattner, Hadjeres, Peers** — arXiv:2405.08679 (ICASSP 2024 SASB workshop): systematic study of JEPA design choices for general audio; headline for us: **several choices that are optimal for images produce poor models on audio** — which part of the input is context vs. target significantly changes what is learned. The pairing/masking structure is modality-specific and decisive.
- Adjacent: Audio-JEPA (arXiv:2507.02915, 2025; authors unverified — flagged §9) — ViT over spectrogram patches, competitive with wav2vec 2.0/data2vec on less data.

### 4.5 Language — the open frontier

- **LLM-JEPA** — Hai Huang, Yann LeCun, Randall Balestriero, arXiv:2509.14252 (2025): a first JEPA-style objective for LLM finetuning *and* pretraining — predict representations of held-out content rather than reconstruct tokens; reports beating standard input-space objectives across Llama3/OpenELM/Gemma2/OLmo on NL-RX, GSM8K, Spider, RottenTomatoes, with overfitting robustness. The authors' own framing: the absence of JEPA-style LLMs "is a testimony of the challenge in designing such objectives for language."
- **VL-JEPA** — D. Chen, Shukor, Moutakanni, Chung, Yu, Kasarla, Bang, Bolourchi, LeCun, Fung, arXiv:2512.10942 (2025): a vision-language model whose objective predicts the **continuous embedding of the target text** instead of autoregressively generating tokens — abstracting away surface linguistic form toward task-relevant semantics, with fewer trainable parameters than generative VLMs.
- **Why language was last:** tokens are discrete and the reconstruction objective (next-token prediction) is already a solved, scalable pretext; there is no natural continuous "physics of the stream" for the target encoder to filter; and what a latent should retain for language is contested. The field's honest position: *latent prediction for discrete symbolic sequences is a 2025 experiment, not an established result.* (This is the literature anchor for Casey's "JEPA is vision, not text" — §7.3.)

### 4.6 What the field says JEPA *is*

Three coexisting readings, in decreasing order of consensus:

1. **An SSL objective family** (the mainstream): masked latent prediction + EMA target + anti-collapse. "JEPA" as the name for I-JEPA-style pretraining. Every paper above participates in this reading.
2. **A world-model architecture** (LeCun's reading): a predictor over learned state that supports planning by backprop-through-predictor; masking is just the cheapest way to manufacture (context, target) pairs from unlabeled data. IWM and V-JEPA 2-AC are the strongest current evidence this reading is load-bearing.
3. **An EBM formulation** (the theory reading): F(x, y[, z]) = D(s_y, Pred(s_x[, z])) as an unnormalized energy; inference = energy minimization over y and z; collapse = the degenerate flat energy surface. Dawid & LeCun 2023 is the reference.

The dissertation will be asked which reading it uses. The safe answer: reading 1 supplies the training recipe; reading 2 supplies the dissertation's *object* (a reading of a room as prediction target); reading 3 supplies the vocabulary for the deadband (§7.3).

---

## 5. The training recipe, as concrete steps

The canonical modern recipe (I-JEPA/V-JEPA configuration). Written as steps because the dissertation may want to specify a literal run:

1. **Choose the prediction unit** (the masking structure). Scale determines abstraction (I-JEPA attenuation study); the choice is modality-specific (Riou et al. 2024). For a stream: windows/regions large enough that the latent of the window is semantic, small enough that prediction is not vacuous.
2. **Sample, per input:** one *context* (e.g., the visible remainder) and M *target* blocks (e.g., 4 large-scale, semantically-sized regions), with context guaranteed not to contain the target interiors.
3. **Context path:** context encoder f (online, trained) → context representation s_x. In I-JEPA a small set of positional/query tokens for each target block attend into s_x through a lightweight predictor ViT g, emitting per-target predicted latents ŷ.
4. **Target path:** target encoder f_EMA (same architecture; weights = EMA of f, momentum ~0.996→1.0 cosine schedule over training in the reference implementation) applied to the *unmasked* target regions; **stop-gradient** on this branch. Targets are the per-patch latents of f_EMA, optionally layer-averaged (data2vec trick; I-JEPA uses last layer).
5. **Loss:** L = Σ_targets D(ŷ, s_y) averaged over targets and patches; D = L2 (I-JEPA) resp. L1 (V-JEPA configuration).
6. **Anti-collapse:** provided by stop-grad + EMA + trainable predictor (family 2). If training runs without asymmetry, add family 3 explicitly (VICReg variance hinge + covariance term, or Barlow identity) — required if both branches receive gradients (e.g., VJ-VCR).
7. **Telemetry (not optional):** log per-dimension std of s_y, effective rank of the batch embedding matrix, and the *energy floor* — the loss achievable by a constant predictor on the same targets. A model whose loss approaches the constant-predictor floor with falling effective rank is collapsing *invisibly*.
8. **Evaluation:** frozen-backbone probes (linear/attentive), never finetuning, never in-training metrics. Report probe task families spanning the claimed abstraction (for V-JEPA: motion AND appearance).

---

## 6–7. Mapping JEPA to THIS dissertation

*(§7 renumbered from here; the mapping sections carry a standing caveat: **no fleet component implements a JEPA architecture** — related-work.md B3's honesty ruling. The correspondences below are structural: they say what the dissertation's objects *are* in JEPA vocabulary, and what would have to be built for the vocabulary to be literal.)*

### 7.1 Conversation temperature is a latent to predict

The elephant's dial readings (warmth, κ, joke-landing, presence, volume, earnestness) are neither the input (words) nor a label (a category) — they are a *learned representation of the room produced by an encoder the fleet does not train*. In the trichotomy's terms (§1.4): a model that predicted the words would be generative; a model that classified rooms warm/cold would be contrastive-ish; the elephant predicts *the representation of the room* — the third family. "Conversation temperature" is s_y. This is not decoration: it fixes what can and cannot be asked of the instrument. A latent can be compared (D(s_y, s_y′)), decomposed (μ̂, κ), and *predicted* — it cannot be paraphrased, and it has no vocabulary. Every failure the fleet logged when it treated readings as text-like objects (the 768-dim cosine confusion, the v0 κ-collinearity) is the trichotomy predicting what happens when you use one family's tools on another family's object.

### 7.2 The room, not the stream, is the unit — because the unit is the abstraction dial

I-JEPA's central empirical lesson (§4.1): **the scale of the prediction target selects the abstraction learned**; A-JEPA/Riou et al. (§4.4): the unit is modality-specific and naive transfer fails. The dissertation's thesis v2 claim — the unit is the room-window (field snapshot) and the conversation is the *edge* between two snapshots, never the stream — is the same design move, with one empirical witness already in hand: the deadband silence at message grain (0/50) with signal at condition grain is exactly the "target too small to be semantic" regime of the I-JEPA attenuation curve. Message-grain latents are the audio analogy of pixel-grain blocks: locally correlated, trivially predictable or unpredictable in the wrong directions; condition-grain field states are the large-block regime where the latent carries structure worth predicting. When the committee asks "why not per-message readings," the field answer is: *because I-JEPA showed the unit determines the abstraction, and Riou et al. showed the right unit is found empirically per modality — and we measured ours* (fine-gap 1.229 chord at condition grain vs. deadband 0/50 at message grain).

### 7.3 The field-edge is JEPA's prediction target

The formal mapping, term by term:

| JEPA term | Dissertation object |
|---|---|
| context x (masked input) | the room's state before the conversation: field_before, with the conversation's interior masked out |
| target y | the room after the conversation |
| s_y = enc(y) | field_after: the vMF state (μ̂, κ, stamps) — the dial-tier latent |
| predictor Pred(s_x) → ŷ | the thing the dissertation wants but does not yet train: the predicted field_after from field_before |
| F = D(s_y, ŷ) | the **edge**: the signed sauna/plunge gap + Δκ — *the energy residual of the room's prediction problem* |
| latent variable z | whatever in the conversation selects *which* plunge: the topic, the personalities — never predicted, only conditioned on |

Two payoffs. First, the edge-as-object gets a principled defense: in JEPA terms, comparing conversations by their edges is comparing *prediction residuals in latent space* — which is exactly what two rooms' edges have in common even when their pixels (words) share nothing. The galley fight and galley coffee share s_x (same start field); their different F-residuals *are* their difference — measurable at condition grain (12.3× deadman threshold), invisible at message grain. Second, **the deadband is the energy floor.** LeCun's abstraction argument (§1.5) says the target encoder may discard what is intrinsically unpredictable; the dissertation's measured deadband (0/50 at message grain, conservative) is the empirical size of exactly that discarded set. "Words are constraints; JEPA is perfect pitch for the shape inside" (nurse doctrine) is the doctrine's phrasing of §1.5: the words are the unpredictable surface; the field trajectory is the predictable structure the latent keeps.

### 7.4 The two samenesses, in JEPA vocabulary

- **Reading 1 (nurse→patient) = first-order JEPA:** comparable features across rooms — a *context encoder applied across instances*, correlations that spot causalities. This is I-JEPA/A-JEPA applied to rooms: the nurse's skill is a trained context encoder whose latents align across patients. That it is "the obvious, less important one" tracks the field: first-order latent prediction is now commodity (§4).
- **Reading 2 (doctor→nurse) = probing a frozen evaluator.** The doctor's read is *not* a reading of the room; it is a reading of a **known instrument's output distribution** — the nurse's drift from her baseline across the last two patients (tempo, softness, mood-change). In field vocabulary: the nurse is a **frozen encoder with known statistics**, and the doctor's reader-delta is the probe on that frozen backbone — V-JEPA's frozen-evaluator protocol (§4.2), pointed at the encoder instead of the task. "A JEPA of a JEPA" is structurally the H-JEPA move (§1.6): the second level predicts *trajectories of first-level representations* — here, the trajectory of the nurse's readings, not of the room. And the pre-registered blind reader-delta discrimination test (baseline+drift vs. first-order similarity, ≥2× noise floor, 3/3 replays, held-out nurse) is the dissertation's translation of frozen-probe evaluation discipline: no finetuning on the test, the probe must transfer to held-out instances of the encoder.
- The **stratified half-life memory ladder** (message → session → memory → identity, monotonically increasing revision half-lives) is the fleet's existing multi-timescale representation stack — H-JEPA's "multiple time scales" (§1.6) realized as architecture rather than as training objective. Note the direction of the analogy: the fleet *has* the hierarchy and lacks the JEPA; LeCun's proposal *has* the JEPA and lacks an implementation of the hierarchy.

### 7.5 Collapse, in fleet terms (why the deadman and the zeitgeist quarantine are the same idea)

- **The zeitgeist loop is a collapse channel.** If the retrieval index feeds its own hits back into the field vector (retrieval→retrieval feedback), the system is optimizing a loss whose target is its own output — the exact structure of §3.1's trivial solution, with "retrieval score" playing D and "the corpus the index serves" playing enc. The predicted end state is dimensional collapse of retrieval toward the zeitgeist mode: everything retrievable becomes what was already retrieved. The doctrine's quarantine — zeitgeist lives in a separate sampler layer, never inside the field vector — is family-3 anti-collapse by construction: it re-anchors the representation in a signal *outside* the learning loop, exactly as VICReg's variance hinge anchors embeddings in the batch statistics (which the model does not fully control).
- **The deadman switch is a collapse tripwire.** A measured ≥2×-noise-floor requirement on the fine gap is a demand that the energy stay above the floor in a way a trivial predictor cannot fake — the experimental analog of §3.4's telemetry (if the gap collapses toward the noise floor while the system "succeeds," the instrument has learned nothing). The dial-tier deadman *fired* (1.229 chord ≈ 12.3× threshold, noise floor 0.000); the encoder-tier deadman remains armed and untested — in JEPA terms, the fleet has verified the *dial-tier latent has anti-collapse structure* and has not yet tested the encoder tier at all.
- **The nurse's baseline is an EMA target encoder.** Her baseline (the median of her own readings, Shewhart/Jacobson–Truax machinery per related-work A1–A2) is a slow-moving average of her own encoder — stop-grad, no gradient from the doctor's read flows back into the nurse. The doctor reads the *residual against the EMA target*. This is the cleanest one-line answer to "where is JEPA in the fleet": the nurse doctrine, described in 2022-paper vocabulary, is *a stop-gradient EMA target encoder whose residuals are consumed as a retrieval key.* (It is an analogy — the nurse is not trained, she is hired — but it is the analogy the committee will understand, and it is honest about what's missing: nobody trains the predictor that would make it literal.)

### 7.6 What would make it literal (future-work-sized, not this-defense-sized)

To move "JEPA" from doctrine to architecture, the minimal run is small: (1) freeze the elephant's dial-tier encoder; (2) train a predictor field_before → field_after over the edge log's (from_field, to_field) pairs, with the elephant as stop-grad target encoder (it is frozen, so no collapse channel exists — the anchor is external, pixel-space-like in its stability); (3) evaluate on held-out edges: does predicted field_after beat the constant predictor (predict "no change") by ≥2× the noise floor, and do prediction residuals cluster by edge-class? That is one chapter-7 experiment, it inherits the pre-registration discipline, and it would convert related-work B3's concession ("the namesake is doctrinal") into "the namesake is a small, frozen-target JEPA over room edges." Note the elegant part: a frozen external target encoder cannot collapse, so the dissertation's first literal JEPA needs no anti-collapse machinery at all — the collapse problem only begins when you *train* the target side, which the fleet, for now, should not.

---

## 8. Open problems in the field (honest, current, citable)

1. **No complete theory of collapse avoidance.** The DirectPred analysis (Tian et al. 2021) covers linear networks; Jing et al. (2022) covers dimensional collapse under contrastive losses; the full nonlinear EMA+predictor picture remains open — "why BYOL doesn't collapse" is still partially an empirical regularity. Consequence: anti-collapse is a recipe, not a guarantee, and effective-rank telemetry is standard practice because theory cannot yet certify training runs.
2. **Language and discrete modalities.** JEPA-style objectives for text are a 2025 experiment (LLM-JEPA, VL-JEPA), explicitly framed as a first step by authors including LeCun. Discrete tokens resist the continuous-latent recipe; what a text latent should retain is unsettled. (Direct literature support for the nurse doctrine's "vision, not text" claim — with the caveat that the field considers it *open*, not settled.)
3. **H-JEPA is unrealized.** No system implements the full hierarchical, multi-timescale, configurator-steered architecture; V-JEPA 2 is flat with one action-conditioned predictor. Claims about hierarchical latent world models at scale are currently promissory.
4. **The multimodality mechanism is unbuilt at scale.** The latent-variable z path (§1.5) is in the proposal and the EBM tutorial; deployed JEPAs are deterministic predictors over single-mode targets. Handling genuinely multimodal futures (a plunge *or* a sauna, undetermined until it happens) is theory-ahead-of-practice.
5. **Evaluation is proxy-based.** Frozen-probe performance is the standard, but probes measure what probes measure; "world model" claims (IWM's predictor-as-solver, V-JEPA 2's planning) are the exception in providing non-probe evidence. A dissertation claiming latent structure for *unmeasured* constructs (temperature) should note that the field itself accepts probe-mediated evidence only provisionally.
6. **Abstraction control is task-relative.** IWM shows the invariant↔equivariant dial exists; nothing says where to set it. The "right" level of abstraction depends on the downstream question — which is the dissertation's tier problem (dial tier ≠ encoder geometry; the fine/coarse ordering inversion) restated in field vocabulary, and the field's honest answer is "it depends, and we're learning to measure it."
7. **Non-vision transfer is design-fragile.** Riou et al. (§4.4): image-optimal choices fail on audio; every new modality re-finds its own masking/pairing structure empirically. For conversations: nobody has published the right prediction unit for social-dynamical latents — the room-window/edge choice is the dissertation's own empirical answer, and it should be defended as such (with the deadband measurement as its attenuation study).

---

## 9. Bibliography (verified 2026-08-20 unless flagged) and flags

**Core:**
- LeCun, Y. (2022). *A Path Towards Autonomous Machine Intelligence.* OpenReview position paper `BZ5a1r-kVsf`, Version 0.9.2, 27 June 2022. [Position paper; not peer-reviewed — say so when citing.]
- Dawid, A., & LeCun, Y. (2023). *Introduction to Latent Variable Energy-Based Models: A Path Towards Autonomous Machine Intelligence.* arXiv:2306.02572. (Les Houches lectures.)
- Assran, M., Duval, Q., Misra, I., Bojanowski, P., Vincent, P., Rabbat, M., LeCun, Y., & Ballas, N. (2023). *Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture (I-JEPA).* CVPR 2023; arXiv:2301.08243. [arXiv v3 comment mislabels the venue as ICCV — it is CVPR 2023.]
- Bardes, A., Garrido, Q., Ponce, J., Chen, X., Rabbat, M., LeCun, Y., Assran, M., & Ballas, N. (2024). *Revisiting Feature Prediction for Learning Visual Representations from Video (V-JEPA).* arXiv:2404.08471. [No peer-reviewed venue on record as of 2026-08; cite as preprint.]
- Assran, M., Bardes, A., Fan, D., Garrido, Q., et al. (2025). *V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning.* arXiv:2506.09985. [Large author list; first five verified via arXiv API; includes LeCun. Preprint.]
- Garrido, Q., Assran, M., Ballas, N., Bardes, A., Najman, L., & LeCun, Y. (2024). *Learning and Leveraging World Models in Visual Representation Learning (IWM).* arXiv:2403.00504. [Venue not stated on arXiv — verify before claiming CVPR/ICML; cite as arXiv if unverified.]

**Anti-collapse and lineage:**
- van den Oord, A., Li, Y., & Vinyals, O. (2018). *Representation Learning with Contrastive Predictive Coding.* arXiv:1807.03748.
- Grill, J.-B., Strub, F., Altché, F., Tallec, C., Richemond, P. H., et al. (2020). *Bootstrap Your Own Latent (BYOL).* NeurIPS 2020; arXiv:2006.07733.
- Chen, X., & He, K. (2021). *Exploring Simple Siamese Representation Learning (SimSiam).* CVPR 2021; arXiv:2011.10566.
- Baevski, A., Hsu, W.-N., Xu, Q., Babu, A., Gu, J., & Auli, M. (2022). *data2vec.* arXiv:2202.03555. [Venue unlisted on arXiv record checked; commonly cited as ICML 2022 — verify before filing.]
- Zbontar, J., Jing, L., Misra, I., LeCun, Y., & Deny, S. (2021). *Barlow Twins.* ICML 2021; arXiv:2103.03230.
- Bardes, A., Pujol, J., Babaeizadeh, T., Vincent, P., LeCun, Y., & Ballas, N. (2022). *VICReg.* ICLR 2022; arXiv:2105.04906. **Flag:** arXiv v3 metadata lists authors as Bardes–Ponce–LeCun only; the ICLR/OpenReview version carries the six-author list. Cite the ICLR version's list; if the discrepancy matters, footnote it.
- Ermolov, A., Siarohin, A., Sangineto, E., & Sebe, N. (2021). *Whitening for Self-Supervised Representation Learning (W-MSE).* ICML 2021; arXiv:2007.06346.
- Tian, Y., Chen, X., & Ganguli, S. (2021). *Understanding Self-Supervised Learning Dynamics without Contrastive Pairs.* ICML 2021; arXiv:2102.06810.
- Jing, L., Vincent, P., LeCun, Y., & Tian, Y. (2022). *Understanding Dimensional Collapse in Contrastive Self-supervised Learning.* ICLR 2022; arXiv:2110.09348.
- He, K., Chen, X., Xie, S., Li, Y., Dollár, P., & Girshick, R. (2022). *Masked Autoencoders Are Scalable Vision Learners.* CVPR 2022; arXiv:2111.06377.
- Caron, M., Touvron, H., Misra, I., Jégou, H., Mairal, J., Bojanowski, P., & Joulin, A. (2021). *Emerging Properties in Self-Supervised Vision Transformers (DINO).* ICCV 2021; arXiv:2104.14294. [Standard citation; not re-verified this pass.]

**Modality extensions:**
- Fei, Z., Fan, M., & Huang, J. (2023). *A-JEPA: Joint-Embedding Predictive Architecture Can Listen.* arXiv:2311.15830. [arXiv notes text overlap with arXiv:2207.06405 by other authors.]
- Riou, A., Lattner, S., Hadjeres, G., & Peeters, G. (2024). *Investigating Design Choices in Joint-Embedding Predictive Architectures for General Audio Representation Learning.* ICASSP 2024 SASB workshop; arXiv:2405.08679.
- Huang, H., LeCun, Y., & Balestriero, R. (2025). *LLM-JEPA: Large Language Models Meet Joint Embedding Predictive Architectures.* arXiv:2509.14252. [Preprint; "first step" framing is the authors'.]
- Chen, D., Shukor, M., Moutakanni, T., Chung, W., Yu, J., Kasarla, T., Bang, Y., Bolourchi, A., LeCun, Y., & Fung, P. (2025). *VL-JEPA: Joint Embedding Predictive Architecture for Vision-Language.* arXiv:2512.10942. [Preprint; author-list spelling variants exist across indexes — verify against final version.]
- *Audio-JEPA* (2025), arXiv:2507.02915. **Flag:** exists per search metadata; authors not verified — do not cite by author until checked.

**Standing flags (per `related-work.md` convention):**
1. LeCun 2022 version/date now verified (v0.9.2, 2022-06-27) — resolves related-work flag #7's first half; V-JEPA (Bardes et al. 2024, arXiv:2404.08471) resolves its second half.
2. Loss functions and EMA schedules quoted in §5 are from the reference implementations as described in the papers; if the dissertation quotes them numerically (L1 vs L2, momentum 0.996→1.0), verify against the paper bodies and code before filing.
3. Everything in §7 is the subagent's structural mapping, not a claim made anywhere in the cited literature. The literature contains no JEPA-of-social-latents work as of 2026-08; if the committee asks "who else does this," the honest answer is "nobody — the ancestors are Shewhart/GMM-UBM/InfoNCE per related-work.md, and the JEPA mapping is ours."

---

*End of guide. Companion files: `research/doctrine/nurse-jepa.md` (the doctrine this guide grounds), `research/dissertation/related-work.md` §B3 (the honesty ruling this guide must respect), `research/skills/jepa-rag-reference.md` (what ships).*
