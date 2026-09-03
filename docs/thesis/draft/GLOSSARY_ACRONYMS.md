# Γλωσσάριο και Ακρωνύμια

> Draft authority for the alphabetical terminology section required by the thesis guidance. T-711 formats/sorts this material in Word and removes terms that do not occur in the accepted manuscript.

## Ακρωνύμια

| Ακρωνύμιο | Όρος | Χρήση στην εργασία |
|---|---|---|
| AD | Adaptive Disturbed | Adaptive Phase-B branch με ενεργό disturbance και learning on. |
| AI | Artificial Intelligence / Τεχνητή Νοημοσύνη | Ευρύτερο πεδίο στο οποίο εντάσσεται η εργασία. |
| AN | Adaptive Nominal | Matched nominal Adaptive Phase-B reference με learning on. |
| CI | Confidence Interval | Στο manuscript χρησιμοποιείται για τα pointwise 95% Student-t intervals. |
| DQN | Deep Q-Network | Deep value-based RL comparator με replay και target network. |
| FD | Frozen Disturbed | Frozen Phase-B branch με disturbance και learning off. |
| FN | Frozen Nominal | Matched nominal Frozen Phase-B reference με learning off. |
| MDP | Markov Decision Process | Κλασικό μαθηματικό πλαίσιο διαδοχικής λήψης αποφάσεων. |
| PPO | Proximal Policy Optimization | On-policy policy-gradient comparator. |
| RL | Reinforcement Learning / Ενισχυτική Μάθηση | Κύριο επιστημονικό πεδίο της μελέτης. |
| RNG | Random Number Generator | Χρησιμοποιείται σε διαχωρισμένα deterministic random streams. |
| RQ | Research Question / Ερευνητικό Ερώτημα | RQ1 nominal learning, RQ2 adaptation benefit, RQ3 recovery. |
| TD | Temporal Difference | Οικογένεια bootstrapped value-learning updates. |

## Βασικοί όροι

### Actual environment interaction
Μία πραγματική αλληλεπίδραση agent–environment. Αποτελεί το κύριο κοινό fairness budget της μελέτης και διακρίνεται από optimizer, replay ή planning updates.

### Adaptation benefit
Το κύριο RQ2 estimand:

\[
(FN-FD)-(AN-AD).
\]

Θετική τιμή σημαίνει ότι το Adaptive regime μείωσε τη disturbance-associated απώλεια σε σχέση με το Frozen regime.

### Adaptive regime
Deployment του ίδιου method checkpoint με τη μάθηση ενεργή. Δεν είναι ξεχωριστός αλγόριθμος.

### Censoring / Right-censoring
Κατάσταση όπου το recovery event δεν παρατηρείται μέχρι το τέλος του fixed Phase-B horizon. Στην περίπτωση αυτή `recovery_time=null` και δεν αντικαθίσταται από ψευδή observed time 256.

### Checkpoint
Αποθηκευμένη επιστημονική κατάσταση που επιτρέπει ακριβή συνέχεια της method-native learning process. Περιλαμβάνει περισσότερα από weights/Q-values όταν ο αλγόριθμος απαιτεί replay, optimizer, RNG, recency/model ή update-boundary state.

### Continual / continued learning
Στο thesis δηλώνει ότι η ίδια frozen method configuration συνεχίζει ordinary method-native online learning μετά το boundary. Δεν σημαίνει specialized continual-learning algorithm.

### Disturbance-associated loss
Η διαφορά nominal−disturbed μέσα στο ίδιο deployment regime. Διατηρείται ξεχωριστά για Frozen και Adaptive branches.

### Dyna-Q+
Tabular RL method που συνδυάζει direct learning, learned-model planning και recency-driven directed re-exploration.

### Equal-layout reduction
Ίσος συνδυασμός των δύο held-out layouts μέσα σε κάθε root πριν από between-root statistical summaries. Τα layouts δεν αποτελούν ανεξάρτητα replicates.

### Frozen regime
Deployment του ίδιου method checkpoint με τη μάθηση απενεργοποιημένη. Χρησιμοποιείται για matched resistance/loss comparison και δεν δηλώνει άλλο algorithm.

### GridWorld
Project-owned ελεγχόμενο πειραματικό και visualization testbed. Δεν αποτελεί το αντικείμενο ή την claimed application domain της διπλωματικής.

### Hidden change
Μεταβολή περιβάλλοντος που δεν παρέχεται στον agent ως explicit context/regime/change indicator. Στο κύριο RQ3 η persistent action remap είναι hidden change.

### Independent root
Η ανεξάρτητη randomization/statistical unit της τελικής μελέτης. Episodes, layouts, probes και recovery windows είναι nested/repeated observations.

### Non-stationarity
Μεταβολή σε dynamics, rewards, observations, action semantics ή άλλη περιβαλλοντική δομή κατά τη διάρκεια learning/deployment.

### Pointwise interval
Interval που αφορά το συγκεκριμένο estimand/contrast. Τα reported 95% Student-t intervals δεν είναι simultaneous confidence bands και δεν συνοδεύονται από formal p-value family.

### Recovery
Για το primary RQ3, stable προσέγγιση της Adaptive-Disturbed trajectory στην Adaptive-Nominal reference σύμφωνα με frozen tolerance και two-window stability rule.

### Recovery incidence / recovered proportion
Το ποσοστό ή πλήθος independent roots που επιτυγχάνουν το frozen stable-recovery criterion μέσα στον Phase-B horizon.

### Recovery time
Observed interaction endpoint του πρώτου qualifying window της πρώτης ακολουθίας δύο διαδοχικών in-tolerance windows. Υπάρχει μόνο για recovered roots.

### Restricted recovery delay
Censoring-aware fixed-horizon comparison quantity. Χρησιμοποιεί observed recovery time όταν υπάρχει και τον horizon όταν υπάρχει censoring. Δεν ταυτίζεται με observed recovery time.

### Resilience / Ανθεκτικότητα
Στην εργασία δεν αποτελεί ένα composite score. Αναλύεται μέσω διακριτών quantities: nominal learning, disturbance-associated loss, adaptation benefit, recovery incidence και recovery timing.

### Stable recovery
Recovery που ικανοποιεί το in-tolerance criterion για δύο συνεχόμενα passive 32-interaction windows.

### Study
Versioned execution entity με immutable recipe, deterministic plan, durable lifecycle state, registered artifacts και provenance.

### StudyRecipe
Immutable machine-readable περιγραφή της πειραματικής πρόθεσης και των execution constraints από την οποία παράγεται deterministic job plan.

### Time-average return
RQ1 trajectory summary πάνω στον interaction axis. Διατηρείται ξεχωριστά από την final nominal performance και αποτυπώνει learning efficiency μέσα στο fixed budget.