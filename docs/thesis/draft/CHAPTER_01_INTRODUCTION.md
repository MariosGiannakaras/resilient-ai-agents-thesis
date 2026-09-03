# Κεφάλαιο 1 — Εισαγωγή

> **Σημείωση drafting:** οι παραπομπές `[@SRC-…]` είναι σταθερά citation-ready source IDs. Η τελική IEEE αρίθμηση παράγεται στο T-711 χωρίς αλλαγή της πηγής.

## 1.1 Αντικείμενο και κίνητρο

Οι πράκτορες ενισχυτικής μάθησης (Reinforcement Learning, RL) μαθαίνουν να λαμβάνουν διαδοχικές αποφάσεις μέσω αλληλεπίδρασης με ένα περιβάλλον. Η κλασική διατύπωση υποθέτει ότι οι σχέσεις μεταξύ καταστάσεων, ενεργειών, μεταβάσεων και ανταμοιβών είναι αρκετά σταθερές ώστε η εμπειρία που αποκτήθηκε στο παρελθόν να παραμένει χρήσιμη [@SRC-701E163AC8]. Σε πραγματικά ή μακρόβια συστήματα, όμως, αυτή η υπόθεση μπορεί να παραβιάζεται: η δυναμική του περιβάλλοντος μπορεί να αλλάζει, οι ενέργειες να έχουν διαφορετικές συνέπειες, οι παρατηρήσεις να αλλοιώνονται ή η διαθέσιμη εμπειρία να μην αντιπροσωπεύει πλέον το τρέχον καθεστώς.

Η non-stationarity δημιουργεί ένα διαφορετικό πρόβλημα από την απλή ονομαστική μάθηση. Ένας agent που είχε μάθει ικανοποιητική policy πριν από μια μεταβολή πρέπει αφενός να αντέξει την άμεση πτώση επίδοσης και αφετέρου, όταν η μάθηση συνεχίζεται, να προσαρμόσει τη συμπεριφορά του χωρίς να στηρίζεται σε privileged γνώση ότι «συνέβη αλλαγή». Η continual-RL βιβλιογραφία επισημαίνει ότι η διατήρηση προηγούμενης γνώσης και η ικανότητα απόκτησης νέας γνώσης δημιουργούν stability–plasticity trade-offs, ενώ η συνεχιζόμενη εκπαίδευση δεν εγγυάται από μόνη της απεριόριστη δυνατότητα προσαρμογής [@SRC-660560956D; @SRC-4C34DF3E17; @SRC-46CF36BC1E].

Παράλληλα, διαφορετικοί RL mechanisms διαχειρίζονται την εμπειρία με διαφορετικό τρόπο. Οι tabular TD methods ενημερώνουν άμεσα action values από τις νέες μεταβάσεις, η DQN επαναχρησιμοποιεί εμπειρία μέσω replay, η PPO βελτιστοποιεί on-policy batches και η Dyna-Q+ συνδυάζει πραγματική εμπειρία με learned-model planning και directed re-exploration. Οι διαφορές αυτές δημιουργούν εύλογη επιστημονική ερώτηση: υπό το ίδιο information contract και τον ίδιο πραγματικό interaction budget, πώς διαφοροποιούνται η ονομαστική μάθηση, το όφελος προσαρμογής και η ανάκαμψη όταν το περιβάλλον μεταβάλλεται;

Η παρούσα διπλωματική προσεγγίζει το ερώτημα ως ελεγχόμενη συγκριτική μελέτη και όχι ως αναζήτηση ενός καθολικά «καλύτερου» αλγορίθμου. Η αξιόπιστη εμπειρική σύγκριση RL methods απαιτεί σαφή budgets, πολλαπλές ανεξάρτητες επαναλήψεις, ελεγχόμενη tuning opportunity και προσεκτική αναφορά uncertainty, επειδή διαφορετικά implementation details και random seeds μπορούν να επηρεάσουν ουσιαστικά το παρατηρούμενο αποτέλεσμα [@SRC-4ED8B918E3; @SRC-8D4F62D85D].

## 1.2 Πρόβλημα και ερευνητικό πλαίσιο

Το βασικό πρόβλημα της εργασίας είναι η σύγκριση διαφορετικών μηχανισμών RL όταν μια policy, αφού πρώτα εκπαιδευτεί σε ονομαστικές συνθήκες, αναπτύσσεται σε περιβάλλον όπου μπορεί να εμφανιστεί μη αναγγελθείσα διαταραχή ή μόνιμη μεταβολή.

Για να απομονωθεί αυτό το πρόβλημα από παράγοντες που δεν αποτελούν αντικείμενο της μελέτης, χρησιμοποιείται project-owned GridWorld ως ελεγχόμενο πειραματικό testbed. Το GridWorld δεν αποτελεί το θέμα της διπλωματικής. Χρησιμοποιείται επειδή επιτρέπει ακριβή ορισμό της κατάστασης, των ενεργειών, των disturbances, των πηγών τυχαιότητας και των matched deployment branches. Με αυτόν τον τρόπο η συμπεριφορά των methods μπορεί να εξεταστεί χωρίς η ερμηνεία να εξαρτάται από ανεξέλεγκτες ιδιότητες ενός σύνθετου πραγματικού συστήματος.

Η μελέτη συγκρίνει πέντε τελικές μεθόδους:

- Q-Learning,
- SARSA,
- Deep Q-Network (DQN),
- Proximal Policy Optimization (PPO),
- Dyna-Q+.

Οι μέθοδοι επιλέχθηκαν ώστε να καλύπτουν διαφορετικούς μηχανισμούς: off-policy και on-policy tabular TD control, deep value learning με replay, on-policy policy optimization και learned-model planning με directed re-exploration. Δεν αποτελούν εξαντλητική taxonomy του continual RL.

Το πείραμα χωρίζεται σε δύο κύριες φάσεις. Στη **Phase A**, κάθε method/root/layout μαθαίνει ανεξάρτητα στο nominal environment μέχρι το παγωμένο interaction budget και παράγει exact scientific checkpoint. Στη **Phase B**, από το ίδιο checkpoint δημιουργούνται matched κλάδοι Frozen Nominal (FN), Frozen Disturbed (FD), Adaptive Nominal (AN) και Adaptive Disturbed (AD). Οι όροι Frozen και Adaptive δεν δηλώνουν διαφορετικούς αλγορίθμους: στο Frozen regime η μάθηση είναι απενεργοποιημένη, ενώ στο Adaptive regime η ίδια μέθοδος συνεχίζει να μαθαίνει.

Η δομή αυτή επιτρέπει να διαχωριστεί η επίδραση του disturbance από τη φυσική μεταβολή που μπορεί να προκαλεί η συνέχιση της μάθησης ακόμη και στο nominal environment. Για αυτό η κύρια μέτρηση του RQ2 δεν είναι απλώς η διαφορά AD−FD, αλλά matched difference-of-losses μεταξύ Frozen και Adaptive regimes.

## 1.3 Σκοπός και στόχοι

Σκοπός της διπλωματικής είναι η **σύγκριση και αξιολόγηση ανθεκτικών πρακτόρων τεχνητής νοημοσύνης σε περιβάλλοντα με αβεβαιότητα**, με έμφαση στη συμπεριφορά RL methods όταν το περιβάλλον μεταβάλλεται μετά την αρχική μάθηση.

Οι επιμέρους στόχοι είναι:

1. να συγκριθεί η ονομαστική μάθηση των πέντε methods υπό κοινό budget πραγματικών αλληλεπιδράσεων,
2. να διαχωριστεί η επίδοση frozen deployment από την επίδραση continued online learning μετά από disturbance,
3. να ποσοτικοποιηθεί το adaptation benefit με matched FN/FD/AN/AD design,
4. να μετρηθεί χωριστά η stable recovery μετά από persistent action remapping, με ρητή αντιμετώπιση της μη ανάκαμψης,
5. να διατηρηθεί η root ως ανεξάρτητη στατιστική μονάδα και να αποφευχθεί η ψευδο-επανάληψη από episodes, layouts ή temporal windows,
6. να διατηρηθεί πλήρης αλυσίδα reproducibility και provenance από το frozen protocol μέχρι τα τελικά figures/tables,
7. να υλοποιηθεί desktop εφαρμογή που καθιστά το experiment και το evidence επιθεωρήσιμα χωρίς να μεταφέρει scientific computation στο UI.

Οι στόχοι αυτοί είναι σκόπιμα στενότεροι από μια γενική αξιολόγηση «AI robustness». Η εργασία δεν επιχειρεί να καλύψει κάθε μορφή uncertainty ούτε κάθε algorithm family.

## 1.4 Ερευνητικά ερωτήματα

Το τελικό protocol-v2.1 ορίζει τρία ερευνητικά ερωτήματα.

### RQ1 — Ονομαστική μάθηση

**Πώς συγκρίνονται η ονομαστική επίδοση και η learning efficiency των πέντε methods υπό κοινό actual-environment-interaction budget και κοινό information contract;**

Η ερώτηση διαχωρίζει την τελική nominal performance από την time-average επίδοση κατά μήκος της Phase-A trajectory. Έτσι, μέθοδοι που καταλήγουν στο ίδιο επίπεδο μπορούν να διαχωριστούν ως προς το πόσο γρήγορα αξιοποίησαν το διαθέσιμο experience budget.

### RQ2 — Ανθεκτικότητα και προσαρμογή

**Πόση disturbance-associated απώλεια εμφανίζεται στα Frozen και Adaptive regimes και ποιο είναι το matched adaptation benefit της continued learning;**

Το κύριο estimand είναι:

\[
B_{adapt}=(FN-FD)-(AN-AD).
\]

Θετική τιμή σημαίνει ότι η συνέχιση της μάθησης μείωσε τη disturbance-associated απώλεια σε σχέση με frozen deployment. Η ερώτηση δεν προϋποθέτει ότι η adaptation είναι πάντοτε ωφέλιμη.

### RQ3 — Ανάκαμψη

**Πώς εξελίσσεται η Adaptive-Disturbed trajectory σε σχέση με την matched Adaptive-Nominal trajectory μετά από persistent, μη αναγγελθείσα αλλαγή και αν/πότε επιτυγχάνεται stable recovery;**

Η κύρια οικογένεια αλλαγής είναι persistent action remapping. Η recovery αξιολογείται σε fixed 32-interaction windows, με primary tolerance 0,10, δύο συνεχόμενα qualifying windows και right-censoring όταν δεν παρατηρείται recovery μέχρι το frozen horizon των 256 interactions.

## 1.5 Συνεισφορά της εργασίας

Η συνεισφορά της εργασίας είναι κυρίως μεθοδολογική, πειραματική και συστημική.

Πρώτον, εφαρμόζεται κοινό **actual-environment-interaction fairness boundary** σε πέντε ετερογενείς RL methods. Η σύγκριση δεν επιβάλλει ίσο πλήθος internal updates, επειδή replay, optimizer steps και planning steps έχουν διαφορετική σημασία μεταξύ methods.

Δεύτερον, χρησιμοποιείται exact-checkpoint **matched FN/FD/AN/AD design**. Η σχεδίαση διαχωρίζει τη disturbance-associated απώλεια από τη μεταβολή που οφείλεται στην ίδια τη continued learning και επιτρέπει την προκαθορισμένη εκτίμηση adaptation benefit.

Τρίτον, η recovery αντιμετωπίζεται ως ξεχωριστό temporal construct και όχι ως συνώνυμο του aggregate adaptation benefit. Η μη ανάκαμψη παραμένει ρητά right-censored, ενώ ο observed recovery time δεν αντικαθίσταται από το horizon όταν το event δεν έχει συμβεί.

Τέταρτον, η τελική scientific pipeline είναι πλήρως versioned και provenance-aware: frozen protocol, deterministic Study plan, exact checkpoints, validated run bundles, frozen evidence, predeclared analysis και registered thesis assets συνδέονται με IDs και hashes.

Πέμπτον, η PySide6 εφαρμογή υλοποιείται ως experiment-first thin client πάνω από το framework-neutral Study/evidence backend. Παρουσιάζει Run, Results και Evidence χωρίς να υπολογίζει εκ νέου estimands, thresholds ή intervals.

Σε επίπεδο αποτελεσμάτων, η τελική μελέτη δείχνει ότι οι τρεις διαστάσεις δεν ευθυγραμμίζονται σε έναν ενιαίο «winner». Η Dyna-Q+ αξιοποίησε ταχύτερα το nominal interaction budget, ενώ Q-Learning και SARSA εμφάνισαν την πιο συνεπή stable recovery στα persistent remaps. Επιπλέον, η online adaptation ήταν έντονα condition-dependent: ωφέλιμη στα persistent action remaps για ορισμένες methods, αλλά όχι καθολικά προστατευτική σε όλες τις uncertainty conditions. Τα ακριβή αποτελέσματα, intervals και censoring counts παρουσιάζονται στο Κεφάλαιο 5 και ερμηνεύονται στο Κεφάλαιο 6.

## 1.6 Πεδίο, παραδοχές και οριοθέτηση

Η εργασία χρησιμοποιεί ένα μικρό, ελεγχόμενο discrete environment και δύο held-out τελικές layouts. Συνεπώς, δεν επιχειρεί να τεκμηριώσει εξωτερική εγκυρότητα προς robotics, continuous control ή large-scale autonomous-agent systems.

Οι πέντε frozen methods/configurations είναι μηχανιστικά διαφορετικά comparators και όχι πλήρης κατάλογος continual-RL τεχνικών. Δεν αξιολογούνται explicit changepoint detectors, latent-context inference, meta-learning, specialized replay-reset strategies, continual-learning regularizers ή safe-RL constraint mechanisms. Σύγχρονες εργασίες σε context-aware continual RL και modular model-based adaptation δείχνουν ότι τέτοιες παρεμβάσεις μπορούν να αλλάξουν το adaptation problem, αλλά βασίζονται σε διαφορετικές πληροφοριακές ή αρχιτεκτονικές παραδοχές [@SRC-6F4F8BE003; @SRC-D38364B32C].

Η persistent action remapping, η action failure και η observation corruption αντιμετωπίζονται ως διαφορετικές disturbance families. Δεν συνδυάζονται σε ένα ενιαίο uncertainty score. Το RQ3 εστιάζει στα action remaps, ενώ οι υπόλοιπες conditions παρέχουν κυρίως supporting evidence για την condition-dependence του RQ2.

Η στατιστική inference χρησιμοποιεί 12 roots ως ανεξάρτητες μονάδες. Layouts, episodes και recovery windows δεν αντιμετωπίζονται ως ανεξάρτητα samples. Τα reported intervals είναι pointwise 95% Student-t intervals και δεν συνοδεύονται από formal p-value superiority family ή multiplicity-adjusted simultaneous inference.

Τέλος, η εργασία διαχωρίζει τη scientific evidence authority από την εφαρμογή και από το τελικό έγγραφο. Τα quantitative claims προέρχονται από το frozen T-611/T-612/T-613 evidence chain. Screenshots ή live visualization μπορούν να εξηγήσουν το workflow, αλλά δεν αποτελούν πηγή αριθμητικών αποτελεσμάτων.

## 1.7 Δομή της διπλωματικής

Η υπόλοιπη διπλωματική οργανώνεται σε έξι κεφάλαια.

Το **Κεφάλαιο 2 — Θεωρητικό Υπόβαθρο και Σχετική Βιβλιογραφία** παρουσιάζει τις βασικές έννοιες MDP/RL, τις πέντε methods, το πρόβλημα non-stationarity και τη σχετική βιβλιογραφία για adaptation, replay, planning και continual learning. Καταλήγει στο συγκεκριμένο ερευνητικό κενό της παρούσας μελέτης.

Το **Κεφάλαιο 3 — Μεθοδολογία και Πειραματικός Σχεδιασμός** περιγράφει το GridWorld testbed, τα frozen method configurations, τις Phase A/Phase B διαδικασίες, τις disturbance conditions, τα RQ estimands, τις roots/layouts και το statistical contract.

Το **Κεφάλαιο 4 — Αρχιτεκτονική και Υλοποίηση του Ερευνητικού Συστήματος** παρουσιάζει το framework-neutral Study backend, τα deterministic plans, τα exact checkpoints, το evidence/analysis layer, την provenance αλυσίδα και την PySide6 εφαρμογή.

Το **Κεφάλαιο 5 — Πειραματικά Αποτελέσματα** παρουσιάζει τα accepted RQ1/RQ2/RQ3 αποτελέσματα, τα intervals, τις paired contrasts, τη right-censoring και το predeclared sensitivity analysis χωρίς εισαγωγή νέων estimands.

Το **Κεφάλαιο 6 — Συζήτηση** ερμηνεύει τα αποτελέσματα σε σχέση με τους διαφορετικούς learning/adaptation mechanisms και τη βιβλιογραφία, και εξετάζει threats to validity και όρια γενίκευσης.

Τέλος, το **Κεφάλαιο 7 — Συμπεράσματα και Μελλοντική Εργασία** απαντά συνοπτικά στα ερευνητικά ερωτήματα, αποτιμά τη συνεισφορά της εργασίας και προτείνει ερευνητικές επεκτάσεις που απορρέουν από τα πραγματικά όρια της μελέτης.