# Pre-Import Agent-Family Review

**Status:** `PROPOSED / PRE-IMPORT / NON-BINDING`  
**Date:** 2026-08-03  
**Scope:** candidate capability roles for the primary persistent rule/dynamics-change experiment.

## Purpose

This review asks a narrower question than `MODEL_CANDIDATES.md`:

> Can the thesis answer its provisional resilience/recovery question with a small, interpretable, CPU-friendly set of agent capability roles before considering heavier deep-RL methods?

The current answer is **probably yes**, but this is not yet a final model shortlist.

Final algorithm selection remains gated by:

1. successful controlled import of the verified bibliography package;
2. accepted target-system capability inventory;
3. final GridWorld prototype/ADR;
4. implementation and correctness prototypes;
5. fair information-access and tuning rules;
6. pilot runtime/variance measurements;
7. the required literature refresh before protocol freeze.

No canonical source identifiers are used here because `research/bibliography/` has not yet been installed and canonical `SRC-*` references outside the generated import are intentionally validated against that manifest.

## Main conclusion

A small discrete GridWorld makes several scientifically distinct comparison roles possible without requiring neural networks merely for scale.

The provisional capability spectrum is:

1. **Frozen nominal policy** — no post-change learning; measures zero-shot resistance/generalization.
2. **Naive continual learner** — continues ordinary updates after the change but has no explicit detector or context memory.
3. **Robust uncertainty-aware policy** — optimized against a declared transition uncertainty set; can be frozen at deployment and exposes conservativeness versus robustness.
4. **Explicit change/context-aware learner** — detects changes and maintains/reuses context-specific knowledge; measures structured online adaptation and, conditionally, recurring-context recall.

These roles are more useful than a catalogue of fashionable algorithms because each isolates a different capability or information assumption.

The final experiment may retain only three of the four roles if pilots show that one role is redundant, infeasible, or unfairly incomparable.

## Why start from tabular/discrete methods

A simple finite GridWorld changes the feasibility landscape.

For the primary scientific question, tabular methods provide several advantages:

- exact state/action semantics are inspectable;
- reference trajectories and Bellman backups can be checked by hand on small fixtures;
- deterministic replay is easier to validate;
- transition uncertainty sets can be represented explicitly;
- Q-table changes can be audited around a changepoint;
- training/runtime cost is likely to remain manageable on CPU;
- more experimental budget can be spent on independent repetitions and severity curves rather than neural-network tuning;
- differences in recovery are less likely to be confounded by optimizer instability or architecture size.

Deep RL should therefore be introduced only if the selected environment/observation representation or research question actually requires function approximation.

This is a scope-control principle, not an assertion that tabular methods are generally superior.

## Role F0 — frozen nominal policy

### Scientific purpose

Establish a clean zero-shot reference for what happens when a policy learned in the nominal environment encounters an unannounced persistent change and receives **no learning updates** afterward.

This role answers:

- how much immediate performance survives the change;
- whether the nominal policy generalizes at all;
- how large the initial degradation is;
- whether apparent robustness exists without adaptation.

### Candidate implementation form

The simplest candidate is a policy obtained from ordinary tabular learning or planning in the nominal environment and then frozen for shifted evaluation.

The final training method does not have to be identical to the online learner, but using a common nominal learner where possible would reduce confounds.

### Information access

- nominal training environment only;
- no true change-point signal;
- no post-change gradient/Q/model updates;
- no special uncertainty set unless explicitly part of the method;
- recurrent/internal state reset policy must be defined if applicable.

### Why retain this role

Without a frozen reference, post-change performance cannot distinguish zero-shot resistance from benefits caused by continued updates.

### Implementation risk

**Low** for a discrete GridWorld.

## Role C0 — naive continual learner

### Scientific purpose

Measure what ordinary online learning can recover **without an explicit change detector or context-memory mechanism**.

This is a critical comparator because “the agent keeps learning” is already an adaptation mechanism. A structured non-stationary method should demonstrate value beyond merely allowing standard updates to continue.

### Candidate implementation form

Ordinary tabular Q-learning is the leading provisional form because:

- it is model-free;
- its update rule is simple and transparent;
- it can continue updating the same Q-table before and after a change;
- it is directly discussed as a baseline in the selected non-stationary literature;
- it can be validated on known small MDP/GridWorld fixtures.

Repeated-update or restart variants can be considered only if they add a distinct diagnostic role.

### Information access

- receives ordinary state/observation, reward, and transition experience;
- no true change-point signal;
- no explicit environment identity;
- no separate context-specific policy store;
- same update rule continues after the change.

### What it isolates

Comparison against F0 estimates the benefit of allowing ordinary online updates.

Comparison against a change/context-aware learner estimates the added value of structured detection, policy separation, or recall.

### Main risk

A single Q-table can mix samples from incompatible contexts and can overwrite knowledge from earlier contexts. That is a scientifically useful failure mode, not necessarily an implementation defect.

### Implementation risk

**Low**.

## Role R0 — robust uncertainty-aware policy

### Scientific purpose

Represent **robustness without post-change learning** and expose its trade-off against nominal utility.

Classical finite robust MDP theory provides an especially clean comparator in a small GridWorld: transition probabilities belong to an explicit structured uncertainty set and the policy is optimized for worst-case value through robust Bellman-style backups.

### Leading provisional form

A small project-owned tabular robust-MDP/value-iteration implementation is preferable to introducing a large dependency if the final uncertainty set remains simple.

This role would record explicitly:

- nominal transition model;
- uncertainty-set family;
- radius/size/severity parameter;
- whether the post-change model lies inside or outside the assumed set;
- nominal value/performance;
- disturbed or worst-case performance;
- conservativeness gap.

### Information access

This role has a **stronger prior assumption** than ordinary model-free learners:

- it is given a declared transition uncertainty set during planning/training;
- it need not know which member becomes active at deployment;
- if evaluated as frozen robustness, it receives no post-change learning updates.

Therefore it must not be ranked as if it had the same information as an agent that must infer structure solely from online samples.

### What it isolates

- benefit of preparing for an uncertainty family before deployment;
- cost of worst-case conservativeness;
- difference between resistance and actual recovery;
- in-set versus out-of-set generalization.

### Why a tabular implementation is attractive

The selected theoretical literature provides finite-state robust Bellman formulations. For a small GridWorld, implementing and testing the required backup may be more auditable than adopting a deep robust-RL codebase whose theory, function approximation, and optimizer behavior introduce additional assumptions.

### Main risks

- rectangular or otherwise structured uncertainty assumptions may be stronger than the final scenario warrants;
- a wide uncertainty set can produce an overly conservative policy;
- an in-set robust policy and an online adaptive learner have different prior information;
- exact robust backup details must be reproduced carefully from the verified source before implementation.

### Implementation risk

**Low-to-moderate**, conditional on a simple finite uncertainty set.

## Role X0 — explicit change/context-aware learner

### Scientific purpose

Represent **structured online adaptation** rather than only continuous generic updating.

The leading provisional family uses:

- online change detection from observed experience;
- separate context-specific policies or value estimates;
- reuse of previously learned knowledge when a context recurs;
- new-context learning when existing contexts do not fit.

This role is the strongest direct match to the provisional primary recovery question.

### Leading provisional algorithm family

Context Q-learning is the most directly aligned tabular/model-free candidate in the current canonical corpus.

The verified full text describes a method that:

- adapts Q-learning for dynamically changing environment models;
- uses state/reward samples to detect model changes;
- learns and stores policies for multiple contexts;
- improves an existing policy when a previously experienced model returns;
- reports reward together with detector metrics such as mean detection delay, precision, and recall.

### Important assumption

The method assumes known model-change patterns. This is not a minor implementation detail; it constrains what claims the thesis may make.

A Context-Q-learning-style method therefore cannot be presented as a universal solution to arbitrary unknown non-stationarity.

### Current implementation availability review

As of the 2026-08-03 pre-screen:

- the paper and later references are readily discoverable;
- the initial public search did **not** identify a clear maintained official code repository for Context Q-learning;
- code-index pages currently show a request-code state rather than a verified official implementation.

This is **not proof that no implementation exists**. It means the project must not rely on an assumed external package before the implementation audit is complete.

If no trustworthy reference implementation is found, feasibility depends on whether the algorithm and detector can be reproduced unambiguously from the verified paper and validated on known fixtures.

### Information access

Must be documented precisely:

- what samples feed the detector;
- whether the number/order/pattern of contexts is assumed known;
- whether the true context label is ever revealed;
- how a new versus recurring context is identified;
- how detector thresholds are selected without using final-test outcomes.

### What it isolates

Comparison against C0 can test whether explicit detection/context memory improves recovery beyond naive continual Q-learning.

If recurring-context testing is retained, X0 can additionally measure recall versus relearning.

### Main risks

- detector threshold/hyperparameter sensitivity;
- false positives and false negatives;
- known-pattern assumption;
- ambiguous or difficult reproduction if no trustworthy code exists;
- added memory/state-management complexity;
- risk of giving it privileged context information not available to other agents.

### Implementation risk

**Moderate** until a paper-to-code reproduction prototype passes.

## Optional decomposition role — detector plus restart/reset

A simple detector-triggered reset/restart learner may be useful as a diagnostic comparator if it can be implemented without expanding the thesis disproportionately.

Its purpose would be to separate:

- benefit from detecting that a change happened;
- benefit from retaining and recalling context-specific knowledge.

For example:

- C0: no detector, same Q-table continues;
- D0: detector fires, learning state is reset/reinitialized;
- X0: detector fires and context-specific prior knowledge can be reused.

This role is **optional**. It should be dropped if it substantially expands tuning or if C0/F0 already provide enough decomposition for the final RQs.

## Methods that are scientifically relevant but currently too heavy for the default path

### Bayesian/deep robust adaptation

Bayesian robust-RL work demonstrates an important robustness–conservativeness trade-off and faster online adaptation than fixed robust uncertainty sets in specific experiments. It is valuable literature for interpretation and may become a candidate if hardware/prototypes justify it.

However, a DQN-style uncertainty head introduces:

- neural-network architecture choices;
- optimizer/tuning burden;
- approximation assumptions beyond the finite robust theory;
- additional stochastic variance;
- substantially more correctness surface than a tabular GridWorld needs by default.

Therefore it is **not the default implementation candidate** before the target-system and feasibility gates.

### Deep action-robust methods

Action-Robust RL has public code links and strong literature support, including tabular theory and continuous-control deep implementations. For this thesis, action failure is currently a supporting diagnostic rather than the primary recovery axis.

Adding a dedicated deep action-robust agent solely for that diagnostic would violate the current scope-control principle unless it also fills a distinct role in the primary rule/dynamics-change experiment.

### PPO/SAC/other generic deep baselines

These remain valid RL families, but no deep baseline should be included merely because it is standard or popular. Function approximation must solve a research or environment requirement that a simpler method cannot.

## Candidate minimal comparison shapes

These are **design alternatives**, not shortlisted final sets.

### Shape A — minimum recovery decomposition

- F0 frozen nominal policy;
- C0 naive continual Q-learning;
- X0 explicit change/context-aware learner.

**Strengths:** smallest direct test of zero-shot versus ordinary updating versus structured adaptation.

**Weakness:** lacks a dedicated pre-trained robustness comparator.

### Shape B — robustness plus adaptation

- F0 frozen nominal policy;
- R0 robust uncertainty-aware policy;
- C0 naive continual Q-learning;
- X0 explicit change/context-aware learner.

**Strengths:** explicitly distinguishes nominal, robust, naive adaptive, and structured adaptive capabilities.

**Weakness:** four roles increase the experiment matrix and information assumptions differ materially.

### Shape C — compact robustness/adaptation contrast

- R0 robust uncertainty-aware frozen policy;
- C0 naive continual Q-learning;
- X0 explicit change/context-aware learner.

**Strengths:** three capability-distinct agents.

**Weakness:** loses a clean nominal frozen reference unless C0 is also evaluated frozen from the same nominal checkpoint; may complicate interpretation.

### Shape D — detector mechanism decomposition

- C0 naive continual Q-learning;
- D0 detector-triggered reset learner;
- X0 context-aware recall learner.

**Strengths:** isolates the value of detection and memory/recall.

**Weakness:** does not represent robust pre-training and may turn the thesis into a detector study.

## Current preferred prototype order

Without selecting the final set, prototype risk should be reduced in this order:

1. **ordinary tabular Q-learning** on deterministic and stochastic reference GridWorld fixtures;
2. **frozen-policy evaluation mode** using the same nominal learner;
3. **small robust Bellman/value-iteration fixture** with an analytically checkable uncertainty set;
4. **Context-Q-learning reproduction spike** focused first on detector/context switching correctness rather than benchmark performance;
5. optional detector-reset comparator only if needed to explain X0 gains.

This order gives useful validation even if a later prototype fails.

## Fairness matrix

| Role | Model knowledge | Uncertainty-set knowledge | True change point | Context label | Post-change updates | Context memory |
|---|---|---|---|---|---|---|
| F0 frozen nominal | none or nominal-training information | none by default | hidden | hidden | no | no |
| C0 naive continual | model-free experience | none | hidden | hidden | yes | one shared learner state |
| R0 robust policy | explicit/estimated finite model as required by robust planning | yes, declared before evaluation | hidden | hidden | no in frozen regime | not required |
| X0 context-aware | model-free experience in leading candidate | pattern assumptions may exist | inferred, not revealed | inferred, not revealed | yes | yes |
| D0 detector-reset, optional | model-free experience | none unless detector requires it | inferred | no reusable context label | yes after reset | no |

This table is a reminder that the agents do not necessarily solve identical information problems. The final thesis should compare **capability regimes under declared assumptions**, not present an unqualified universal ranking.

## Primary recovery experiment implications

For the persistent rule/dynamics-change experiment:

- F0 establishes immediate zero-shot failure/resistance;
- C0 establishes how much ordinary ongoing learning recovers;
- R0 tests whether pre-deployment robustness avoids failure and at what nominal cost;
- X0 tests whether explicit change/context handling improves recovery or recall;
- D0, if retained, helps attribute gains to detection versus memory.

The primary analysis should preserve both:

- performance level before the change;
- the full post-change trajectory.

A method that starts with poor nominal performance and drops little is not automatically preferable to a method that starts higher, drops further, and recovers rapidly.

## Observation/action diagnostic implications

The same retained agents should be reused where their interfaces make sense.

Do not add an extra observation-robust or action-robust deep algorithm merely to populate the supporting diagnostic suite unless that algorithm also answers a retained research question.

For observation disturbance:

- evaluate clean versus corrupted observations by severity;
- keep ground-truth state separate from delivered observation;
- interpret frozen-policy results as robustness, not recovery.

For action failure:

- record intended and executed actions separately;
- vary failure/replacement probability systematically;
- report nominal performance alongside stressed performance.

## Implementation-source policy

For every algorithm that survives into the actual model matrix:

1. prefer an official or author-linked implementation when trustworthy and compatible;
2. inspect license, version/revision, dependencies, tests, and paper-code correspondence;
3. if implementing from the paper, record the exact equations/algorithm sections used;
4. write known-answer unit tests before running comparative experiments;
5. do not silently “improve” an algorithm in ways that change its scientific identity;
6. separate necessary compatibility fixes from algorithmic modifications;
7. document any unresolved ambiguity as a limitation or exclusion reason.

## Prototype acceptance criteria

### Q-learning/frozen reference

- known deterministic GridWorld optimal-policy fixture passes;
- seeded stochastic transition fixture reproduces exactly;
- disabling updates after the declared freeze is testable;
- Q-table serialization/checksum is stable.

### Robust finite-MDP comparator

- nominal radius/set degenerates to the nominal solution when mathematically expected;
- hand-computed tiny MDP robust backup matches implementation;
- widening uncertainty does not silently change unrelated reward/observation semantics;
- in-set/out-of-set evaluation is explicit;
- frozen deployment performs no hidden learning.

### Context/change-aware prototype

- detector can be tested on synthetic known changepoints independent of policy reward;
- false positive/negative behavior is observable;
- new context and recurring context are distinguishable;
- policy/Q-state storage does not overwrite other contexts;
- context recall can be disabled for an ablation if later required;
- no true change point or context ID leaks into the agent unless explicitly part of the method.

## Decision rules after the target-system and import gates

Prefer the **smallest set** that satisfies all retained research questions.

A candidate should be excluded if:

- it duplicates an existing capability role;
- its information assumptions make a fair interpretation impossible;
- the paper-to-code mapping cannot be validated;
- runtime/tuning cost threatens sufficient independent repetitions;
- its primary value appears only in observation/action diagnostics rather than the main recovery question;
- it requires a more complex environment representation solely to accommodate the method;
- its addition would force a substantially larger hyperparameter search without distinct scientific value.

## Current recommendation

The most promising low-complexity path to prototype after the hard gates clear is:

> **ordinary tabular Q-learning as the common reference/naive continual learner, a small finite robust-MDP comparator, and a tabular explicit change/context-aware method; retain a separate frozen evaluation regime and make detector-reset/context-recall additions conditional.**

This would keep the primary comparison interpretable, CPU-friendly, and closely aligned with the distinction between resistance and recovery.

It is **not** yet a final shortlist. In particular, the Context-Q-learning reproduction risk and the robust comparator's information advantage must be resolved before any model is selected.
