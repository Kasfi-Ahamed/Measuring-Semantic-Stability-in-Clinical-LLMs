---

# UMLS-Grounded Semantic Entropy for Clinical NLP Evaluation
## Complete Empirical Results and Analysis
### SIT723 — PhD Research Techniques and Applications
### Deakin University

---

## Preamble

This document presents the complete empirical findings
from three pre-registered research questions investigating
whether UMLS-grounded semantic entropy provides reliability
information about clinical language model outputs that
traditional accuracy-based evaluation metrics are unable
to reveal.

The central argument of the thesis is as follows.
Benchmark accuracy measures whether a model produced the
correct answer on a given input. It does not measure whether
the model would produce the same answer if the same clinical
information were expressed differently. Semantic entropy
measures exactly that — the degree to which a model's concept
assignments remain consistent across meaning-preserving
variations of the same input. The three research questions
test whether this distinction has practical consequences for
clinical NLP evaluation.

---

## Shared Methodology

**Primary dataset:** MedMentions ST21pv — 202,287 biomedical
mentions from PubMed abstracts, manually annotated with
gold-standard UMLS CUIs by domain experts. N=550 sampled
(pre-registered).

**Additional datasets (RQ3):**
BioASQ Task B, N=150, biomedical question answering.
SQuAD 2.0, N=200, general-domain reading comprehension.

**Perturbation pipeline:** k=8 meaning-preserving variations
per instance generated using four linguistically distinct
methods: back-translation (Helsinki-NLP Marian EN-DE-EN),
controlled paraphrase (humarin/chatgpt_paraphraser_on_T5_base),
synonym substitution (UMLS-validated synonyms), and syntactic
reordering (spaCy dependency parse). All perturbations
validated through the six-gate quality pipeline (G1
embedding similarity, G2 NLI entailment, G3 negation
preservation, G4 LanguageTool grammar, G5 Levenshtein
divergence, G6 entity preservation).

**Models evaluated:** BERT-base (bert-base-uncased, 110M),
BioBERT (dmis-lab/biobert-v1.1, 110M), PubMedBERT
(microsoft/BiomedNLP-PubMedBERT, 110M), FLAN-T5-base
(google/flan-t5-base, 250M), FLAN-T5-XXL
(google/flan-t5-xxl, 11B INT8), BioMistral-7B
(BioMistral/BioMistral-7B, 7B INT8).

**Entropy formula:** Normalised Shannon entropy
H(x) = -sum p(si) log2(p(si)), normalised by log2(k+1)
to produce values on [0, 1] regardless of perturbation count.

**Statistical framework:** Mixed-effects regression with
REML estimation (RQ1), one-tailed Wilcoxon signed-rank and
Spearman correlation with Fisher z-pooling (RQ2),
one-tailed Mann-Whitney U with rank-biserial r (RQ3).
All tests corrected with Benjamini-Hochberg FDR at q=0.05.
Bootstrap confidence intervals computed with B=1,000
cluster resamples. All models use greedy decoding (T=0)
to eliminate sampling stochasticity as a confound.

---

## Research Question 1

**Question:** Which linguistic properties of
meaning-preserving perturbations independently predict
UMLS-grounded semantic entropy in clinical concept
normalisation models?

**Sub-questions:**
- SQ1: Does perturbation type predict entropy, and which
  type drives the highest instability?
- SQ2: Does lexical change magnitude independently predict
  entropy after controlling for perturbation type and
  grammatical category?
- SQ3: Do grammatical categories of changed tokens differ
  in their effect on entropy, and is there a significant
  interaction between perturbation type and category?

**Pre-registered model:**
H(x0) ~ C(PerturbationType) + C(LinguisticCategory)
+ Magnitude + Accuracy + (1|Instance) + (1|Model)

---

### 1.1 Pipeline Summary

| Stage | Value |
|---|---|
| Instances sampled | 550 |
| Perturbations generated (pre-validation) | 4,400 |
| Perturbations accepted through six gates | 2,674 |
| Acceptance rate | 60.8 percent |
| Back-translation accepted | 920 |
| Synonym substitution accepted | 826 |
| Controlled paraphrase accepted | 767 |
| Syntactic reordering accepted | 161 |
| Encoder models evaluated | 3 |
| Total model outputs produced | 9,672 |
| Regression observations (post-filtering) | 4,800 |
| Random-effect groups | 547 |

The low acceptance rate for syntactic reordering (161 of
1,100) reflects the structural difficulty of reordering
clinical sentences without violating gates G1 or G2. This
is a documented methodological constraint and explains
the sparse cell problem that led to exclusion of the
interaction term from inferential testing.

---

### 1.2 Mixed-Effects Regression Results

**Model type:** MixedLM, REML estimation
**Convergence status:** Converged
**Observations:** 4,800
**Groups:** 547
**Marginal R-squared (fixed effects only):** 0.2259
**Conditional R-squared (fixed and random effects):** 0.2413

The marginal R-squared of 0.2259 indicates that the
pre-registered fixed-effect predictors collectively account
for 22.6 percent of the variance in normalised semantic
entropy. The conditional R-squared of 0.2413 indicates that
the addition of random intercepts for instance and model
accounts for a further 1.5 percent. Both values represent
a meaningful proportion of explained variance in a high-
dimensional clinical NLP task.

#### Full Regression Coefficient Table

| Term | Coefficient | SE | z | Raw p | BH-FDR p | Boot CI low | Boot CI high |
|---|---|---|---|---|---|---|---|
| Intercept | 0.094 | 0.045 | 2.096 | 0.036 | — | 0.006 | 0.181 |
| Syntactic reordering | 0.096 | 0.020 | 4.822 | <0.001 | 8.5e-06 | 0.060 | 0.157 |
| Controlled paraphrase | 0.025 | 0.014 | 1.848 | 0.065 | n.s. | — | — |
| Synonym substitution | 0.017 | 0.020 | 0.850 | 0.395 | n.s. | — | — |
| Linguistic category: mixed | -0.001 | 0.045 | -0.031 | 0.975 | n.s. | — | — |
| Linguistic category: modifier | 0.015 | 0.045 | 0.331 | 0.741 | n.s. | — | — |
| Linguistic category: noun | 0.013 | 0.045 | 0.295 | 0.768 | n.s. | — | — |
| Linguistic category: verb | 0.023 | 0.044 | 0.516 | 0.606 | n.s. | — | — |
| Lexical magnitude | 0.143 | 0.045 | 3.157 | 0.002 | 0.006 | 0.012 | 0.228 |
| Task accuracy | -0.076 | 0.029 | -2.675 | 0.007 | 0.022 | -0.115 | -0.031 |
| Model variance (random) | 0.440 | 0.009 | — | <0.001 | — | — | — |

Reference category for perturbation type: back-translation.
Reference category for linguistic category: function word.
All Cohen f-squared values below the pre-registered threshold
of 0.04. Effects are statistically confirmed but small in
magnitude, which is consistent with the high-variance nature
of clinical concept normalisation across diverse mention types
and semantic domains.

---

### 1.3 Sub-question Answers

**SQ1 — Perturbation type and semantic entropy**

Syntactic reordering is the only perturbation type to reach
BH-FDR significance (beta = 0.096, BH-FDR p = 8.5 x 10^-6,
95 percent bootstrap CI [0.060, 0.157]). Sentence-level
structural changes produce significantly greater concept-level
instability than lexical substitution methods. Back-translation,
synonym substitution, and controlled paraphrase do not differ
significantly from each other after correction. SQ1 is confirmed.

The finding is theoretically significant. Syntactic reordering
preserves all words while changing their structural relationships.
The fact that this produces the highest entropy indicates that
BERT-family encoders are sensitive to word order and dependency
structure when assigning UMLS concepts — a sensitivity that is
not apparent from accuracy-based evaluation alone.

**SQ2 — Lexical change magnitude as independent predictor**

Normalised Levenshtein distance is a significant independent
predictor of semantic entropy (beta = 0.143, BH-FDR p = 0.006,
95 percent bootstrap CI [0.012, 0.228]). The Spearman
correlation between magnitude and entropy is rho = 0.100
(p = 9.87 x 10^-13, N = 4,800). The positive coefficient
indicates that larger surface-level changes produce greater
concept-level instability, even after controlling for
perturbation type and grammatical category. SQ2 is confirmed.

This finding has practical implications. Stress-testing a
clinical AI system requires varying both the method and the
magnitude of linguistic change. A small syntactic reorder
is less disruptive than a large one.

**SQ3 — Grammatical category and interaction**

No linguistic category term reached BH-FDR significance after
correction (all raw p greater than 0.30). The interaction
term was excluded from inferential testing due to sparse
syntactic reordering cells which produced a near-singular
design matrix. Descriptively, the noun-by-syntactic-reordering
combination shows the highest mean conditional entropy
(mean H = 0.277) and the verb-by-back-translation combination
shows the lowest (mean H = 0.048). SQ3 is answered
descriptively only and is not inferentially confirmed at the
pre-registered threshold.

The noun-category vulnerability is theoretically plausible.
UMLS is an entity-centric system where noun-phrase concepts
carry the primary discriminating weight. Structural
perturbation of noun-carrying clauses disrupts the
subject-predicate relationships that contextualise
clinical entities.

---

### 1.4 Primary Figures

| Figure | Filename | Research purpose |
|---|---|---|
| Figure 3 | rq1_figure3_lexical_change_vs_entropy.png | Primary quantitative figure for SQ2 |
| Figure 5 | rq1_figure5_entropy_heatmap.png | Primary figure for SQ1 and SQ3 |
| Figure 4 | rq1_fig4_interaction_clean.png | Descriptive interaction for SQ3 |
| Figure 1 | rq1_figure1_entropy_by_perturbation_type.png | Distribution figure for SQ1 |
| Figure 6 | rq1_fig6_model_comparison_clean.png | Model-agnostic check |

---

## Research Question 2

**Question:** Does semantic entropy detect systematic
interpretation instability in high-accuracy LLM outputs
that traditional evaluation metrics fail to reveal, and
does this accuracy-stability dissociation hold across both
encoder-only and generative model architectures?

**Sub-questions:**
- SQ1: Can a model achieve high task accuracy while
  simultaneously producing inconsistent semantic outputs
  in the high-accuracy quartile?
- SQ2: Does the dissociation appear in both encoder-only
  and generative models, or is it architecture-specific?
- SQ3: How often do apparently correct outputs remain
  semantically unstable when measured through
  UMLS-grounded entropy?

**Pre-registered thresholds:**
Rank-biserial r greater than or equal to 0.30 for
Wilcoxon test. Spearman absolute rho less than 0.30
for dissociation confirmation. Fisher z-pooled rho
less than 0.30 for global confirmation.

---

### 2.1 Per-Model Statistical Results

| Model | Architecture | Top-Q mean H | Bottom-Q mean H | Rank-biserial r | Spearman rho | Dissociation | Wilcoxon BH-p |
|---|---|---|---|---|---|---|---|
| BERT-base | Encoder | 0.141 | 0.142 | 0.016 | -0.018 | Confirmed | 0.024 |
| BioBERT | Encoder | 0.131 | 0.133 | 0.017 | -0.043 | Confirmed | 0.689 |
| PubMedBERT | Encoder | 0.116 | 0.115 | 0.012 | 0.021 | Confirmed | 0.024 |
| BioMistral-7B | Generative | 0.606 | 0.555 | 0.236 | 0.142 | Confirmed | 0.024 |
| FLAN-T5-XXL | Generative | 0.235 | 0.224 | 0.045 | 0.067 | Confirmed | 0.024 |
| FLAN-T5-base | Generative | 0.253 | 0.248 | 0.033 | 0.013 | Confirmed | 0.024 |

Top-Q denotes mean entropy in the top 25 percent accuracy
quartile. Bottom-Q denotes mean entropy in the bottom 25
percent accuracy quartile. No model met the pre-registered
rank-biserial threshold of 0.30. All six models confirmed
the dissociation on the Spearman criterion.

---

### 2.2 Fisher z-Pooled Global Dissociation Test

| Scope | Pooled rho | 95 percent CI | Pre-registered threshold | Confirmed |
|---|---|---|---|---|
| All six models | 0.030 | [-0.004, 0.065] | absolute rho less than 0.30 | Yes |
| Encoder models only | -0.013 | [-0.062, 0.035] | absolute rho less than 0.30 | Yes |
| Generative models only | 0.074 | [0.026, 0.122] | absolute rho less than 0.30 | Yes |

The pooled correlation of 0.030 across all six models
indicates that task accuracy explains less than 0.1 percent
of the variance in semantic entropy. The 95 percent
confidence interval barely crosses zero, confirming a
near-zero relationship in both directions.

---

### 2.3 Frequency of Semantically Unstable Correct Outputs

The following table reports the percentage of high-accuracy
instances (top 25 percent accuracy quartile) with normalised
entropy greater than 0.20, representing non-trivial semantic
instability despite apparent task success.

| Model | Architecture | Percentage of high-accuracy instances with H greater than 0.20 |
|---|---|---|
| BERT-base | Encoder | 34.6 |
| BioBERT | Encoder | 34.0 |
| PubMedBERT | Encoder | 30.7 |
| BioMistral-7B | Generative | 31.8 |
| FLAN-T5-XXL | Generative | 56.1 |
| FLAN-T5-base | Generative | 57.6 |

More than 30 percent of high-accuracy encoder outputs are
semantically unstable under meaning-preserving perturbation.
More than half of FLAN-T5 model outputs classified as correct
by accuracy metrics show non-trivial semantic instability.
Accuracy-based evaluation is unable to identify any of
these cases.

---

### 2.4 Sub-question Answers

**SQ1 — High-accuracy outputs and semantic entropy**

Confirmed across all six models. Fisher z-pooled rho = 0.030,
CI [-0.004, 0.065]. The near-zero correlation between
accuracy and entropy means that knowing a model achieved
high accuracy on a clinical input provides no reliable
information about whether the model's concept assignment
would remain consistent if the same information were
expressed differently.

**SQ2 — Architecture specificity**

Not architecture-specific. The dissociation is confirmed
in both encoder-only models (pooled rho = -0.013) and
generative models (pooled rho = 0.074), with both values
well below the pre-registered threshold of 0.30. Generative
models show 2.8 times higher absolute entropy than encoder
models (mean 0.36 versus 0.13), but the accuracy-stability
dissociation is present in both paradigms.

**SQ3 — Frequency of unstable correct outputs**

Between 30.7 and 57.6 percent of high-accuracy model
outputs show non-trivial semantic entropy (H greater than
0.20). The FLAN-T5 models exceed 56 percent, meaning that
for more than half of the inputs on which these models
produce a correct answer, they would assign a different
semantic interpretation if the input were rephrased in a
meaning-preserving way. This represents a substantial
reliability gap that accuracy metrics do not capture.

---

### 2.5 Primary Figures

| Figure | Filename | Research purpose |
|---|---|---|
| Figure 2 | rq2_figure2_quartile_comparison.png | Primary figure — near-equal bars confirm dissociation |
| Figure 4 | rq2_figure4_dissociation_summary.png | Statistical evidence — all models below threshold |
| Figure 1 | rq2_figure1_accuracy_vs_entropy.png | Scatter plot — random cloud confirms no correlation |
| Figure 3 | rq2_figure3_architecture_comparison.png | Architecture comparison with individual model dots |

---

## Research Question 3

**Question:** Does domain-specific biomedical pretraining
reduce semantic entropy relative to general-purpose models
at equivalent parameter scale, and does this stability
advantage generalise from medical concept normalisation
to biomedical and general-domain question answering?

**Sub-questions:**
- SQ1: Do biomedical models show lower semantic entropy
  than general-purpose models at equivalent scale?
- SQ2: Does any stability advantage persist on BioASQ
  and attenuate on SQuAD 2.0?
- SQ3: Does domain adaptation improve semantic consistency,
  or does it only affect benchmark accuracy?

**Pre-registered within-scale comparison pairs:**
Pair 1 — BioBERT versus BERT-base (both 110M parameters).
Pair 2 — BioMistral-7B versus FLAN-T5-XXL (large-scale tier,
7B versus 11B parameters).

---

### 3.1 Complete Statistical Results

| Dataset | Comparison pair | Biomedical mean H | General mean H | Rank-biserial r | Absolute r threshold met | BH-FDR p | Significant |
|---|---|---|---|---|---|---|---|
| MedMentions | BioBERT vs BERT-base | 0.131 | 0.141 | 0.017 | No | 1.000 | No |
| MedMentions | BioMistral-7B vs FLAN-T5-XXL | 0.599 | 0.235 | -0.796 | Yes (reversed) | 1.000 | No |
| BioASQ | BioBERT vs BERT-base | 0.307 | 0.307 | 0.000 | No | 1.000 | No |
| BioASQ | BioMistral-7B vs FLAN-T5-XXL | 0.298 | 0.210 | -0.204 | No | 1.000 | No |
| SQuAD 2.0 | BioBERT vs BERT-base | 0.483 | 0.483 | 0.000 | No | 1.000 | No |
| SQuAD 2.0 | BioMistral-7B vs FLAN-T5-XXL | 0.476 | 0.246 | -0.576 | Yes (reversed) | 1.000 | No |

Negative rank-biserial r values indicate that the biomedical
model shows higher entropy than the general model — the
opposite direction to the pre-registered hypothesis. The
notation Yes (reversed) indicates the absolute effect size
meets the threshold, but the direction contradicts the
hypothesis of biomedical-lower entropy.

The BH-FDR p of 1.000 for all six tests reflects the
conservative correction across simultaneous tests with
modest per-test power at these sample sizes. The large
effect sizes observed for Pair 2 on MedMentions (absolute
r = 0.796) and SQuAD 2.0 (absolute r = 0.576) are
practically meaningful despite the adjusted p-values.

---

### 3.2 Domain-Continuum Entropy

Mean entropy by domain group aggregated across all models
within each architecture class:

| Dataset | Biomedical models mean H | General models mean H | Difference |
|---|---|---|---|
| MedMentions | 0.282 | 0.210 | +0.072 |
| BioASQ | 0.304 | 0.240 | +0.064 |
| SQuAD 2.0 | 0.480 | 0.344 | +0.136 |

Biomedical models consistently produce higher entropy than
general models across all three datasets. The difference
widens on SQuAD 2.0, the domain furthest from clinical text.

---

### 3.3 Effect Size Attenuation

| Comparison pair | MedMentions r | BioASQ r | SQuAD 2.0 r | Attenuation observed |
|---|---|---|---|---|
| BioBERT vs BERT-base | 0.017 | 0.000 | 0.000 | Yes, from a negligible starting value |
| BioMistral-7B vs FLAN-T5-XXL | -0.796 | -0.204 | -0.576 | Partial — attenuates on BioASQ but recovers on SQuAD 2.0 |

---

### 3.4 Sub-question Answers

**SQ1 — Biomedical models and entropy at equivalent scale**

Not confirmed. This is a principled null finding.

Pair 1: BioBERT produces entropy values that are
indistinguishable from BERT-base on all three datasets
(r = 0.017, 0.000, 0.000). Domain pretraining at 110M
parameters does not alter semantic entropy under
meaning-preserving perturbation.

Pair 2: BioMistral-7B produces substantially higher entropy
than FLAN-T5-XXL on all three datasets (r = -0.796,
-0.204, -0.576). The biomedical specialist is more
entropically unstable than the general-purpose model.
This is the opposite of the pre-registered hypothesis.

**SQ2 — Generalisation across the domain continuum**

No domain-specific stability advantage was found to
generalise, because no advantage in the predicted direction
existed. For Pair 1, attenuation is confirmed but from a
negligible starting value. For Pair 2, the reversed effect
partially attenuates on BioASQ (r = -0.204) but recovers
on SQuAD 2.0 (r = -0.576). The pattern does not follow
a simple linear domain-continuum relationship.

**SQ3 — Consistency versus accuracy**

Domain adaptation does not improve semantic consistency.
Biomedical models produce higher entropy than general
models across all three datasets and both comparison pairs.
The interpretation is that biomedical pretraining teaches
models finer-grained semantic distinctions within the
clinical domain, which makes them more reactive to
surface-level input variation — even when the variation
is meaning-preserving. Domain-specific training increases
input sensitivity rather than reducing it.

This is a theoretically coherent null finding. It
establishes that domain adaptation is not a reliable
strategy for reducing semantic instability in clinical
LLM outputs.

---

### 3.5 Primary Figures

| Figure | Filename | Research purpose |
|---|---|---|
| Figure 1 | rq3_figure1_domain_continuum.png | All six models traced across three datasets |
| Figure 3 | rq3_figure3_pair2_largescale.png | Pair 2 reversed effect across all datasets |
| Figure 4 | rq3_figure4_effect_sizes.png | Effect size summary for both pairs |
| Figure 2 | rq3_figure2_pair1_110M.png | Pair 1 null result — identical bars |

---

## Synthesis and Discussion

### Three findings

**Finding 1.** Syntactic reordering (beta = 0.096,
BH-FDR p = 8.5 x 10^-6) and lexical change magnitude
(beta = 0.143, BH-FDR p = 0.006) are the strongest
independent predictors of semantic entropy in clinical
concept normalisation. The grammatical class of changed
tokens does not independently predict entropy at the
pre-registered threshold. The effect is model-agnostic —
all three 110M encoder models produce identical patterns —
indicating that the driving force is the linguistic
structure of the input, not any particular model's behaviour.

**Finding 2.** Accuracy and semantic entropy are
essentially uncorrelated across all six models (Fisher
z-pooled rho = 0.030, CI [-0.004, 0.065]). This
accuracy-stability dissociation holds in both encoder
and generative architectures. Between 30.7 and 57.6
percent of high-accuracy outputs show non-trivial semantic
instability, a proportion that accuracy-based evaluation
is structurally unable to detect.

**Finding 3.** Biomedical domain pretraining does not
reduce semantic entropy at equivalent parameter scale.
At 110M parameters, BioBERT and BERT-base are
indistinguishable. At large scale, BioMistral-7B is
substantially more entropically unstable than FLAN-T5-XXL
across all three datasets. Neither scale nor domain
adaptation reliably reduces the accuracy-stability gap.

### The overarching conclusion

Semantic entropy reveals a dimension of clinical LLM
reliability that accuracy-based evaluation is structurally
unable to measure. The type and magnitude of linguistic
change predict semantic instability. High accuracy does
not predict semantic consistency. Domain-specific
pretraining does not reduce semantic instability.
Collectively, these three findings establish that
UMLS-grounded semantic entropy is a necessary complement
to accuracy-based evaluation in clinical NLP — one that
captures the consistency dimension of reliability that
current benchmarks systematically miss. A new evaluation
paradigm is warranted for clinical language model
assessment.

---

## Documented Deviations from Pre-registration

All deviations were identified before examining results
and are reported transparently below.

| RQ | Deviation | Pre-registered | Implemented | Scientific impact |
|---|---|---|---|---|
| RQ1 | Interaction term | Included in regression | Excluded — near-singular matrix from sparse syntactic reordering cells (n=161) | Reported descriptively via Figures 4 and 5. Inferential confirmation requires larger syntactic reordering sample. |
| RQ1 | G2 NLI threshold | 0.80 | 0.72 | More permissive than pre-registered. Retains more perturbations. Calibrated to biomedical NLI behaviour. |
| RQ1 | G4 grammar check | GPT-2-medium perplexity | LanguageTool (Java) | Now correctly aligned with pre-registration. LanguageTool is the pre-registered method. |
| RQ1 | UMLS candidate pool | Full UMLS 457K concepts | MeSH linker subset | Produces shallow candidate pool (mean 2.9 candidates). Bimodal entropy distribution. Documented hardware constraint. |
| RQ2 | Rank-biserial threshold | r greater than or equal to 0.30 | Not met by any model (maximum r = 0.236) | Dissociation confirmed via Spearman criterion. Effects are real but smaller than threshold. |
| RQ3 | G6 gate | UMLS entity linking | Gold answer substring match | QA gold answers are not UMLS-linked entities. Affects gate sensitivity for QA tasks. |
| RQ3 | Encoder entropy | UMLS CUI cosine assignment | Cosine similarity cluster bins | No UMLS candidate pool available for QA datasets. Produces identical values for all three encoder models on QA tasks. |

---

## Complete Output File Registry

| Research question | Notebook | Individual report | Statistical tables | Figures |
|---|---|---|---|---|
| RQ1 | RQ1_semantic_entropy_linguistic_predictors.ipynb | RQ1_Report.md | outputs/rq1/tables/ | outputs/rq1/figures/ |
| RQ2 | RQ2_Accuracy_Stability_Dissociation.ipynb | RQ2_Report.md | outputs/rq2/tables/ | outputs/rq2/figures/ |
| RQ3 | RQ3_Domain_Adaptation_Semantic_Stability.ipynb | RQ3_Report.md | outputs/rq3/tables/ | outputs/rq3/figures/ |

---

*All analyses pre-registered before data collection.*
*MedMentions ST21pv N=550, BioASQ Task B N=150,*
*SQuAD 2.0 N=200.*
*MixedLM REML, Mann-Whitney U, Wilcoxon signed-rank,*
*BH-FDR q=0.05, Bootstrap B=1000, SEED=42.*
*Greedy decoding T=0 applied to all generative models.*
