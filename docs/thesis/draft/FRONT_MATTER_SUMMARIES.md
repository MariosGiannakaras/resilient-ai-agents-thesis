# Προκαταρκτικό υλικό — Περίληψη / Abstract

**Επίσημος ελληνικός τίτλος:** Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα  
**Official English title:** Comparison and Evaluation of Resilient AI Agents in Uncertain Environments

> Το T-710 παγώνει το επιστημονικό περιεχόμενο των περιλήψεων. Η τελική τοποθέτηση, μορφοποίηση, σελιδοποίηση και Word fields ανήκουν στο T-711.

## Περίληψη

Η παρούσα διπλωματική εργασία μελετά συγκριτικά τη συμπεριφορά πρακτόρων ενισχυτικής μάθησης όταν ένα περιβάλλον μεταβάλλεται μετά την αρχική εκπαίδευσή τους. Στόχος είναι να διαχωριστούν τρεις διαφορετικές διαστάσεις: η ονομαστική ικανότητα μάθησης, το όφελος της συνεχιζόμενης προσαρμογής μετά από διαταραχή και η χρονική ανάκαμψη μετά από μόνιμη αλλαγή. Αξιολογούνται πέντε μέθοδοι — Q-Learning, SARSA, Deep Q-Network (DQN), Proximal Policy Optimization (PPO) και Dyna-Q+ — σε ελεγχόμενο GridWorld με κοινό budget πραγματικών αλληλεπιδράσεων, δύο held-out διατάξεις και δώδεκα ανεξάρτητες ρίζες.

Το πειραματικό πρωτόκολλο χωρίζεται σε ονομαστική Phase A και matched Phase B. Από το ίδιο ακριβές checkpoint δημιουργούνται Frozen Nominal, Frozen Disturbed, Adaptive Nominal και Adaptive Disturbed κλάδοι, ώστε να υπολογίζεται το όφελος προσαρμογής χωρίς να συγχέεται με τη φυσική μεταβολή της συνεχιζόμενης μάθησης. Η ανάκαμψη αξιολογείται χωριστά σε παθητικά παράθυρα 32 αλληλεπιδράσεων, με προκαθορισμένη ανοχή, σταθερότητα δύο διαδοχικών παραθύρων και ρητή right-censoring όταν δεν παρατηρείται ανάκαμψη εντός του ορίζοντα.

Τα αποτελέσματα δείχνουν ότι Q-Learning, SARSA και Dyna-Q+ φτάνουν στο ίδιο τελικό ονομαστικό επίπεδο, ενώ η Dyna-Q+ αξιοποιεί ταχύτερα το διαθέσιμο interaction budget. Στα persistent action remaps, η online μάθηση παρέχει μεγάλο όφελος κυρίως για Q-Learning και SARSA και θετικό όφελος για Dyna-Q+, αλλά η επίδρασή της δεν είναι καθολικά θετική στις υπόλοιπες μορφές αβεβαιότητας. Ως προς την ανάκαμψη, Q-Learning και SARSA εμφανίζουν τη μεγαλύτερη συνέπεια στα δύο persistent remaps. Συνολικά, η εργασία δείχνει ότι η ανθεκτικότητα δεν αποτυπώνεται από μία ενιαία κατάταξη, αλλά απαιτεί χωριστή αξιολόγηση μάθησης, απώλειας, προσαρμογής και ανάκαμψης.

**Λέξεις-κλειδιά:** Ενισχυτική Μάθηση, Ανθεκτικοί Πράκτορες, Μη Στασιμότητα, Προσαρμογή, Ανάκαμψη

## Abstract

This thesis presents a controlled comparison of reinforcement-learning agents when the environment changes after nominal training. The study separates three distinct dimensions of behavior: nominal learning capability, the benefit of continued adaptation after a disturbance, and temporal recovery after a persistent change. Five methods are evaluated — Q-Learning, SARSA, Deep Q-Network (DQN), Proximal Policy Optimization (PPO), and Dyna-Q+ — in a controlled GridWorld under a common real environment-interaction budget, two held-out layouts, and twelve independent roots.

The experimental protocol consists of a nominal Phase A followed by a matched Phase B. Each exact Phase-A checkpoint is branched into Frozen Nominal, Frozen Disturbed, Adaptive Nominal, and Adaptive Disturbed conditions, allowing adaptation benefit to be estimated without conflating it with nominal drift caused by continued learning. Recovery is evaluated separately using passive 32-interaction windows, a predeclared tolerance, a two-window stability criterion, and explicit right-censoring when stable recovery is not observed within the fixed horizon.

The results show that Q-Learning, SARSA, and Dyna-Q+ reach the same final nominal performance, while Dyna-Q+ uses the available interaction budget more efficiently over the learning trajectory. Under persistent action remapping, continued learning produces a large adaptation benefit for Q-Learning and SARSA and a positive benefit for Dyna-Q+, but adaptation is not uniformly beneficial across the other uncertainty conditions. In terms of recovery, Q-Learning and SARSA exhibit the most consistent stable recovery across both persistent remapping conditions. Overall, the findings show that resilience cannot be reduced to a single method ranking. It requires separate assessment of learning efficiency, disturbance-associated loss, adaptation benefit, recovery incidence, and recovery timing under an explicit information and change contract.

**Keywords:** Reinforcement Learning, Resilient Agents, Non-Stationarity, Adaptation, Recovery