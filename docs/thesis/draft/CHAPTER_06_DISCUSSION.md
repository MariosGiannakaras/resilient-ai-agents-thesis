# Κεφάλαιο 6 — Συζήτηση

## 6.1 Σκοπός και ερμηνευτικό όριο

Το προηγούμενο κεφάλαιο παρουσίασε τι έδειξε η προδηλωμένη ανάλυση. Το παρόν κεφάλαιο εξετάζει τι σημαίνουν τα αποτελέσματα, πώς συνδέονται με το θεωρητικό και εμπειρικό πλαίσιο και ποια είναι τα όρια της γενίκευσής τους. Η διάκριση είναι ουσιώδης: η Συζήτηση δεν αποτελεί χώρο για νέα estimands, νέες στατιστικές δοκιμές ή εκ των υστέρων επιλογή thresholds.

Οι ερμηνείες που ακολουθούν παραμένουν δεσμευμένες από τρεις αρχές. Πρώτον, τα αποτελέσματα αφορούν το συγκεκριμένο controlled GridWorld, το frozen interaction budget και τις συγκεκριμένες implementations/configurations. Δεύτερον, οι μηχανισμοί που προτείνονται από τη βιβλιογραφία — όπως stale replay, loss of plasticity ή model interference — χρησιμοποιούνται ως ερμηνευτικά πλαίσια και όχι ως αιτιώδεις εξηγήσεις που αποδείχθηκαν από το πείραμα. Τρίτον, η απόδοση μιας μεθόδου σε ένα ερευνητικό ερώτημα δεν μετατρέπεται σε καθολική κατάταξη για όλα τα ερωτήματα.

## 6.2 RQ1: τελική επίδοση και sample efficiency δεν είναι το ίδιο

Το πρώτο βασικό εύρημα είναι η σαφής διάκριση ανάμεσα στην τελική ονομαστική επίδοση και στην αποτελεσματικότητα μάθησης κατά μήκος του interaction budget. Οι Q-Learning, SARSA και Dyna-Q+ κατέληξαν στην ίδια τελική mean return (-0,100), αλλά η Dyna-Q+ είχε πολύ υψηλότερο time-average return (-0,485 έναντι περίπου -1,61 για τις δύο TD methods). Η διαφορά αυτή δείχνει ότι η ερώτηση «πού κατέληξε η policy;» είναι διαφορετική από την ερώτηση «πόσο αποτελεσματικά χρησιμοποίησε το διαθέσιμο experience budget;».

Η παρατήρηση είναι συμβατή με τη βασική αρχή του Dyna ότι η πραγματική εμπειρία αξιοποιείται τόσο για άμεση value learning όσο και για model-based planning updates [@SRC-F6BD3A6B18; @SRC-701E163AC8]. Στο συγκεκριμένο μικρό discrete task, τα δέκα planning steps της Dyna-Q+ ανά πραγματική αλληλεπίδραση προσφέρουν έναν μηχανισμό με τον οποίο η ίδια εξωτερική εμπειρία μπορεί να οδηγήσει σε περισσότερη εσωτερική ενημέρωση. Αυτό όμως δεν σημαίνει ότι η Dyna-Q+ είχε «περισσότερο δίκαιο» ή «λιγότερο δίκαιο» budget: το project όρισε εξαρχής ως κοινό fairness axis τις πραγματικές αλληλεπιδράσεις, όχι τον αριθμό εσωτερικών updates. Η επιλογή αυτή είναι συνεπής με τη σύγχρονη βιβλιογραφία empirical RL design, η οποία επισημαίνει ότι episode counts, update counts και tuning opportunity μπορούν να δημιουργήσουν παραπλανητικές συγκρίσεις αν δεν οριστεί ρητά κοινό experience currency [@SRC-4ED8B918E3; @SRC-8D4F62D85D].

Η Q-Learning και η SARSA είχαν σχεδόν ταυτόσημη time-average συμπεριφορά, παρά τη θεωρητική τους διαφορά ως off-policy και on-policy TD control. Η βιβλιογραφία υποστηρίζει ότι η Q-Learning χρησιμοποιεί greedy maximum στον one-step target, ενώ η SARSA χρησιμοποιεί την επόμενη ενέργεια της behavior policy [@SRC-701E163AC8; @SRC-D52DF7B9A4]. Στο συγκεκριμένο nominal GridWorld και με κοινό ε=0,1, η διαφορά αυτή δεν οδήγησε σε ουσιαστικό διαχωρισμό στο aggregate learning-efficiency estimand.

Οι DQN και PPO είχαν χαμηλότερη τελική και time-average επίδοση και μεγαλύτερη μεταξύ-root διακύμανση. Αυτό δεν πρέπει να ερμηνευθεί ως γενική αδυναμία deep RL. Οι δύο μέθοδοι έχουν μεγαλύτερη παραμετρική και optimization πολυπλοκότητα από αυτή που απαιτεί το μικρό discrete GridWorld. Επιπλέον, η βιβλιογραφία έχει δείξει ότι η απόδοση deep-RL μεθόδων μπορεί να εξαρτάται σημαντικά από implementation details, hyperparameters και random variation [@SRC-8D4F62D85D; @SRC-5D0E7E5BD7]. Η εργασία ελέγχει αυτά τα στοιχεία μέσω frozen configurations και πολλαπλών roots, αλλά δεν μπορεί να μετατρέψει το συγκεκριμένο interaction budget σε καθολικό τεστ δυνατοτήτων DQN ή PPO.

## 6.3 RQ2: η προσαρμογή είναι condition-dependent

Το δεύτερο βασικό εύρημα είναι ότι η online adaptation δεν λειτουργεί ως καθολικά προστατευτικός μηχανισμός. Στα persistent action remaps, η συνέχιση της μάθησης μείωσε έντονα τη disturbance-associated απώλεια για Q-Learning, SARSA και Dyna-Q+. Στην action-failure condition δεν παρατηρήθηκε καθαρό aggregate benefit. Στην observation corruption, οι Q-Learning και SARSA είχαν αρνητικό adaptation benefit.

Η διαφοροποίηση αυτή είναι αναμενόμενη όταν οι disturbance mechanisms αλλοιώνουν διαφορετικό τμήμα του agent-environment loop. Η persistent action remapping αλλάζει τη σχέση ανάμεσα στην επιλεγμένη ενέργεια και στην περιβαλλοντική της συνέπεια. Ένα TD learner που συνεχίζει να ενημερώνει τις action values μπορεί σταδιακά να αντικαταστήσει τις παλιές εκτιμήσεις με εμπειρία από το νέο mapping. Αντίθετα, η observation corruption εισάγει περιστασιακά λανθασμένο input στο learning process. Η online ενημέρωση πάνω σε αλλοιωμένες παρατηρήσεις μπορεί να μεταφέρει το σφάλμα στις value estimates αντί να «διορθώσει» μια σταθερή νέα δυναμική.

Η βιβλιογραφία για non-stationary και continual RL υποστηρίζει γενικά ότι αλλαγές στο environment distribution μπορούν να καταστήσουν παλιές value/policy/model εκτιμήσεις ανεπαρκείς και ότι η συνεχιζόμενη μάθηση δεν εγγυάται από μόνη της διατήρηση ικανότητας προσαρμογής [@SRC-660560956D; @SRC-4C34DF3E17; @SRC-46CF36BC1E]. Το πρόσφατο ICLR 2025 work για online RL σε non-stationary context-driven environments τοποθετεί το catastrophic forgetting και το stability–plasticity trade-off στο κέντρο της continual deployment διαδικασίας [@SRC-6F4F8BE003]. Ωστόσο, η συγκεκριμένη εργασία παρέχει ρητό exogenous context στην policy, σε αντίθεση με το παρόν protocol όπου η action remap αλλαγή δεν ανακοινώνεται. Η διαφορά αυτή είναι κρίσιμη: τα αποτελέσματα της παρούσας μελέτης αφορούν adaptation χωρίς explicit regime label και δεν πρέπει να εξισωθούν με context-conditioned control.

Το γεγονός ότι η PPO είχε σχεδόν μηδενικό aggregate adaptation benefit στα remaps δεν σημαίνει ότι το clipping objective της «δεν είναι robust». Το PPO clipping σχεδιάστηκε για να περιορίζει υπερβολικά μεγάλες policy updates, όχι για να παρέχει εγγύηση έναντι αλλαγής environmental dynamics [@SRC-CD5F67F3E6]. Η βιβλιογραφία μάλιστα δείχνει ότι implementation-level choices παίζουν σημαντικό ρόλο στην παρατηρούμενη συμπεριφορά PPO/TRPO-like methods [@SRC-5D0E7E5BD7].

Αντίστοιχα, το μικρό/αβέβαιο DQN benefit δεν μπορεί να αποδοθεί αιτιωδώς στο replay buffer μόνο από τα αποτελέσματα της παρούσας εργασίας. Είναι όμως θεμιτό να σημειωθεί ως βιβλιογραφικά τεκμηριωμένο threat ότι replay design και retained history επηρεάζουν τη μάθηση [@SRC-CBA29E303A]. Σε non-stationary setting, pre-change replay μπορεί να λειτουργήσει ως stale evidence, ενώ η επιθετική απομάκρυνσή του μπορεί να οδηγήσει σε forgetting παλιών αλλά ακόμη έγκυρων transitions. Αυτή ακριβώς τη διαμάχη interference-versus-forgetting αναδεικνύει και το πρόσφατο work για partial models [@SRC-D38364B32C]. Στην παρούσα μελέτη δεν έγινε replay reset, reweighting ή specialized continual intervention, επειδή αυτά θα αποτελούσαν διαφορετικό ερευνητικό ερώτημα.

## 6.4 Dyna-Q+: γρήγορη ονομαστική μάθηση δεν συνεπάγεται ταχύτερη ανάκαμψη

Η Dyna-Q+ παρουσιάζει ιδιαίτερο ενδιαφέρον επειδή συνδυάζει δύο φαινομενικά αντίθετα αποτελέσματα. Στο RQ1 είχε μακράν το καλύτερο time-average nominal performance. Στο RQ2 είχε μεγάλο θετικό adaptation benefit στα persistent remaps. Ωστόσο, στο RQ3 δεν ήταν η ταχύτερη μέθοδος ανάκαμψης: στο cycle remap ανακτήθηκε σε 12/12 roots, αλλά με restricted delay 176 interactions, έναντι 98,7 για Q-Learning και 136 για SARSA. Στο swap remap ανακτήθηκε μόνο σε 8/12 roots.

Το αποτέλεσμα αποτρέπει μια απλοϊκή ερμηνεία σύμφωνα με την οποία «model-based planning ισοδυναμεί με γρηγορότερη adaptation». Η Dyna οικογένεια χρησιμοποιεί learned model για planning και η Dyna-Q+ προσθέτει recency-driven exploration ώστε να ενθαρρύνει την επανεξέταση ενεργειών που δεν έχουν δοκιμαστεί πρόσφατα [@SRC-F6BD3A6B18; @SRC-701E163AC8]. Σε changing environment, όμως, ένα learned model μπορεί προσωρινά να περιέχει stale consequences μέχρι να ανανεωθούν τα επηρεασμένα state-action pairs. Τα planning updates μπορούν τότε να διαδώσουν παλιά πληροφορία μαζί με τη νέα.

Το πρόσφατο work των partial models παρέχει ένα σύγχρονο παράδειγμα όπου η οργάνωση ενός learned model και του replay/history επηρεάζει την local adaptation [@SRC-D38364B32C]. Οι συγγραφείς δείχνουν ότι modular/partial model updating μπορεί να βελτιώσει την adaptation σε συγκεκριμένα deep model-based agents και LoCA settings. Η σύνδεση με την παρούσα εργασία είναι εννοιολογική και όχι άμεση: το deep Dyna-Q/PlaNet/Dreamer setting του source δεν ταυτίζεται με το bounded tabular Dyna-Q+ protocol. Παρ' όλα αυτά, υποστηρίζει τη γενικότερη θέση ότι η κατοχή μοντέλου δεν εγγυάται από μόνη της ταχεία προσαρμογή· έχει σημασία τι πληροφορία παραμένει stale και πώς ενημερώνεται.

Η παρούσα εργασία δεν έχει σχεδιαστεί ώστε να μετρήσει ξεχωριστά «χρόνο ανανέωσης του model» ή να αποδώσει αιτιότητα σε συγκεκριμένο planning mechanism. Επομένως, η σωστή ερμηνεία είναι περιορισμένη: η frozen Dyna-Q+ configuration έμαθε γρήγορα nominally και είχε θετικό aggregate adaptation benefit, αλλά η stable recovery trajectory της ήταν λιγότερο συνεπής ή πιο αργή από Q-Learning/SARSA στα tested remaps.

## 6.5 RQ3: recovery incidence, timing και censoring

Το RQ3 δείχνει γιατί ένα aggregate post-change metric δεν αρκεί. Η Q-Learning και η SARSA είχαν 12/12 recoveries και στα δύο remaps. Η Dyna-Q+ είχε πλήρη recovery incidence στο cycle αλλά 8/12 στο swap. Η DQN και η PPO είχαν ακόμη περισσότερη right-censoring.

Η right-censoring αλλάζει τον τρόπο ερμηνείας του χρόνου. Για παράδειγμα, στο swap remap η PPO έχει conditional recovery-time mean 56 interactions, μικρότερο από την Q-Learning (106,7) και τη SARSA (98,7). Αν αγνοηθεί ότι η PPO ανακτήθηκε μόνο σε 4/12 roots, η τιμή αυτή μπορεί να οδηγήσει στο λανθασμένο συμπέρασμα ότι «η PPO ανακάμπτει γρηγορότερα». Στην πραγματικότητα, το conditional mean περιγράφει μόνο το subset των roots που ανακτήθηκαν. Για αυτό η εργασία παρουσιάζει ταυτόχρονα recovered proportion και restricted delay through horizon.

Η διάκριση αυτή αποτελεί σημαντικό construct-validity σημείο. Το recovery status, ο observed recovery time και το restricted delay απαντούν διαφορετικές ερωτήσεις. Η αντικατάσταση του `null` recovery time με 256 θα έκρυβε τη μη ανάκαμψη και θα μπέρδευε ένα censoring horizon με πραγματικό event time.

## 6.6 Ευαισθησία στον operational ορισμό της ανάκαμψης

Το primary tolerance 0,10 ήταν παγωμένο πριν από τα τελικά αποτελέσματα, με 0,05 και 0,20 ως sensitivity thresholds. Η sensitivity analysis έδειξε ότι το broad pattern υπέρ Q-Learning/SARSA ως προς recovery consistency παραμένει, αλλά η ακριβής incidence είναι ιδιαίτερα ευαίσθητη για DQN, Dyna-Q+ και PPO.

Η Dyna-Q+ στο cycle αποτελεί χαρακτηριστικό παράδειγμα: 0/12 roots ανακτώνται στο tolerance 0,05, ενώ 12/12 στο 0,10 και 12/12 στο 0,20. Άρα η δήλωση «ανακτήθηκε πλήρως» είναι σωστή μόνο όταν συνοδεύεται από τον operational ορισμό που χρησιμοποιείται. Το ίδιο ισχύει για κάθε recovery metric που βασίζεται σε neighborhood/tolerance criterion.

Η ευαισθησία αυτή δεν ακυρώνει το RQ3. Αντίθετα, δείχνει γιατί το protocol περιλαμβάνει προκαθορισμένο sensitivity analysis. Ο στόχος δεν είναι να βρεθεί ένα μοναδικό «αληθινό» threshold, αλλά να φανεί αν η βασική ερμηνεία εξαρτάται δραματικά από μια λογική μεταβολή του operational definition.

## 6.7 Σχέση με continual RL και hidden change

Το thesis protocol μελετά ordinary method-native continued learning μετά από hidden persistent change. Δεν χρησιμοποιεί explicit changepoint detector, context label, specialized meta-learning ή continual-learning regularizer. Η επιλογή αυτή είναι σκόπιμη: το ερευνητικό ερώτημα είναι πώς συμπεριφέρονται οι συγκεκριμένοι standard mechanisms όταν η ίδια η εκτέλεσή τους συνεχίζεται μετά τη μεταβολή.

Η σύγχρονη continual-RL βιβλιογραφία δείχνει ότι υπάρχουν πιο εξειδικευμένες παρεμβάσεις που αντιμετωπίζουν stability/plasticity, retention και context recurrence [@SRC-6F4F8BE003]. Η παρούσα μελέτη δεν τις ανταγωνίζεται άμεσα. Αντίθετα, τα αποτελέσματά της παρέχουν baseline evidence για το πόσο μακριά μπορούν να φτάσουν οι standard configurations χωρίς explicit change awareness.

Η πληροφοριακή διαφορά έχει ιδιαίτερη σημασία. Στο ICLR 2025 context-driven setting, το current exogenous context παρέχεται στην policy [@SRC-6F4F8BE003]. Στο παρόν action-remap setting, ο πράκτορας δεν λαμβάνει ούτε context label ούτε change indicator. Επομένως, η adaptation πρέπει να προκύψει από τις παρατηρούμενες συνέπειες των ενεργειών και την ίδια τη learning dynamics.

## 6.8 Απειλές προς την εσωτερική εγκυρότητα

### 6.8.1 Fairness και tuning

RL comparisons είναι ευαίσθητες σε hyperparameter choices, implementation details και tuning opportunity [@SRC-4ED8B918E3; @SRC-8D4F62D85D]. Το project περιόρισε τον κίνδυνο με προκαθορισμένη tuning διαδικασία σε non-final evidence, κοινό actual-interaction budget, frozen final configurations και 12 roots. Παρ' όλα αυτά, «fair» δεν σημαίνει ότι όλες οι μέθοδοι έχουν ίση πιθανότητα να εκφράσουν τη μέγιστη δυνατή απόδοσή τους σε κάθε task. Μια άλλη tuning budget ή architecture family θα μπορούσε να αλλάξει τα numerical outcomes.

### 6.8.2 Checkpoint equivalence

Η matched Phase B εξαρτάται από την ακριβή ισότητα του scientific state πριν από το branching. Η αρχική T-610 αποτυχία απέδειξε ότι boundary details μπορούν να είναι κρίσιμα. Η τελική replacement execution αντιμετώπισε το πρόβλημα fail-closed, από νέα καθαρή εκτέλεση, και το T-611 επικύρωσε checkpoint lineage. Παρ' όλα αυτά, το θέμα αποτελεί σημαντικό methodological lesson: ένα «checkpoint» που διατηρεί μόνο weights αλλά όχι method-native continuation state δεν θα ήταν επαρκές για αυτή τη μελέτη.

### 6.8.3 Information leakage

Η εφαρμογή disturbance flags, true state ή change indicators μόνο για evaluator/visualization δημιουργεί κίνδυνο ακούσιας διαρροής προς τον agent. Το project επιβάλλει explicit information boundary και διαχωρισμένα observation contracts. Η internal validity εξαρτάται από τη συνέπεια αυτού του boundary σε environment, adapters, checkpoints και live instrumentation.

## 6.9 Construct validity

Η «ανθεκτικότητα» είναι πολυδιάστατη. Η εργασία αποφεύγει να τη συμπτύξει σε ένα score και διαχωρίζει nominal learning, disturbance-associated loss, adaptation benefit, recovery incidence και recovery timing. Η επιλογή αυτή μειώνει τον κίνδυνο ένα composite metric να κρύψει αντίθετα patterns.

Η online continuation επίσης δεν αποκαλείται specialized continual-learning method. Οι Adaptive branches είναι οι ίδιες μέθοδοι με learning ενεργό. Ομοίως, το PPO clipping δεν ταυτίζεται με environmental robustness, και η Dyna-Q+ planning δομή δεν ταυτίζεται με εγγυημένη resilience.

Οι τρεις uncertainty mechanisms δεν είναι ισοδύναμοι. Persistent action remapping αλλάζει action semantics, action failure εισάγει stochastic actuation uncertainty και observation corruption αλλοιώνει το input. Η condition-dependent συμπεριφορά του RQ2 επιβεβαιώνει εμπειρικά ότι η κοινή ετικέτα «uncertainty» δεν αρκεί για να προβλέψει την επίδραση της adaptation.

## 6.10 Statistical conclusion validity

Η inference χρησιμοποιεί roots ως ανεξάρτητες μονάδες. Layouts, episodes και windows είναι nested/repeated observations. Αυτό περιορίζει την ψευδο-επανάληψη αλλά αφήνει n=12 ως σχετικά μικρό independent sample για κάθε πλήρες block.

Τα 95% Student-t intervals είναι pointwise και δεν συνοδεύονται από multiplicity correction ή formal p-value family. Για αυτό το κείμενο χρησιμοποιεί τα intervals ως uncertainty summaries και όχι ως βάση για εκτεταμένες significance claims.

Στο RQ3, τα conditional recovery-time summaries μπορεί να έχουν ακόμη μικρότερο n. Στην ακραία περίπτωση PPO/cycle, n=1 και δεν υπάρχει interval. Η αναφορά αυτών των values είναι χρήσιμη περιγραφικά μόνο όταν συνοδεύεται από recovery incidence και censoring information.

## 6.11 External validity

Το μεγαλύτερο όριο γενίκευσης είναι το controlled testbed. Η εργασία χρησιμοποιεί μία οικογένεια μικρού GridWorld, δύο held-out layouts, discrete action space και συγκεκριμένα disturbance definitions. Τα αποτελέσματα δεν μπορούν να μεταφερθούν άμεσα σε robotics, continuous control, Atari-like domains ή large-scale autonomous agents.

Οι DQN και PPO χρησιμοποιούν compact CPU-feasible architectures, όχι large-scale deep-RL tuning. Αντίστοιχα, η Dyna-Q+ είναι bounded tabular implementation. Η σύγκριση επομένως απαντά πώς συμπεριφέρονται αυτές οι frozen implementations υπό κοινό contract, όχι πώς θα συμπεριφέρονταν όλες οι πιθανές εκδοχές των algorithm families.

Η σύγχρονη βιβλιογραφία partial models και context-aware continual RL περιλαμβάνει πλουσιότερες representations και structural assumptions [@SRC-D38364B32C; @SRC-6F4F8BE003]. Αυτές οι διαφορές περιορίζουν τις direct cross-study comparisons αλλά ταυτόχρονα δείχνουν σαφείς κατευθύνσεις για επέκταση της παρούσας εργασίας.

## 6.12 Reproducibility validity

Η reproducibility απειλείται ιδιαίτερα στα deep-RL methods από implementation choices και incomplete checkpoints [@SRC-5D0E7E5BD7; @SRC-8D4F62D85D]. Η παρούσα εργασία αντιμετωπίζει το πρόβλημα με locked Python environment, source commit provenance, exact scientific checkpoints, manifest/checksum validation, deterministic job planning και frozen downstream evidence.

Η ύπαρξη reproducible assets δεν σημαίνει ότι κάθε run σε διαφορετικό hardware θα έχει ίδιο runtime. Για αυτό wall/process CPU time αντιμετωπίζεται ως secondary descriptive evidence, ενώ η primary fairness axis παραμένει ο αριθμός actual environment interactions.

## 6.13 Απάντηση στα ερευνητικά ερωτήματα σε ερμηνευτικό επίπεδο

**RQ1:** Στο συγκεκριμένο task και budget, οι Q-Learning, SARSA και Dyna-Q+ φτάνουν στην ίδια τελική ονομαστική επίδοση. Η Dyna-Q+ όμως αξιοποιεί αποτελεσματικότερα το interaction budget ως προς το time-average trajectory. Οι DQN/PPO είναι πιο αργές και πιο heterogeneous σε αυτή την κλίμακα.

**RQ2:** Η συνέχιση της μάθησης είναι ιδιαίτερα ωφέλιμη μετά από persistent action remapping για Q-Learning/SARSA και θετικά για Dyna-Q+, αλλά δεν αποτελεί καθολικά προστατευτικό mechanism. Η επίδραση είναι μικρή ή αβέβαιη στο action failure και μπορεί να γίνει αρνητική στην observation corruption.

**RQ3:** Η Q-Learning και η SARSA έχουν την πιο συνεπή stable recovery στα δύο persistent remaps. Η Dyna-Q+ συνδυάζει ισχυρό nominal learning και θετικό adaptation benefit με πιο αργή ή λιγότερο συνεπή recovery. DQN και PPO έχουν μεγαλύτερη right-censoring εντός του frozen horizon. Η ακριβής recovery incidence εξαρτάται από το προκαθορισμένο tolerance, επομένως κάθε claim πρέπει να δηλώνει τον operational ορισμό.

## 6.14 Κεντρικό συμπέρασμα της Συζήτησης

Η βασική επιστημονική εικόνα δεν είναι ότι μία μέθοδος «κερδίζει», αλλά ότι διαφορετικοί μηχανισμοί παράγουν διαφορετικά trade-offs μεταξύ γρήγορης nominal learning, aggregate adaptation benefit και stable recovery. Η Dyna-Q+ είναι ισχυρή στη sample efficiency, η Q-Learning και η SARSA είναι ιδιαίτερα συνεπείς στην recovery υπό persistent remapping, ενώ οι deep methods δεν αξιοποιούν το μικρό fixed budget με την ίδια συνέπεια. Ταυτόχρονα, η observation corruption δείχνει ότι η ίδια η δυνατότητα online learning μπορεί να γίνει πηγή επιδείνωσης.

Το αποτέλεσμα αυτό υποστηρίζει μια πιο ακριβή έννοια «ανθεκτικού πράκτορα»: όχι έναν πράκτορα που απλώς συνεχίζει να εκπαιδεύεται, αλλά ένα σύστημα του οποίου η συμπεριφορά πρέπει να αξιολογείται χωριστά ως προς resistance/loss, adaptation benefit, recovery incidence και recovery timing, υπό σαφώς ορισμένο information and change contract.