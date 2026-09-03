# Κεφάλαιο 2 — Θεωρητικό Υπόβαθρο και Σχετική Βιβλιογραφία

> **Σημείωση drafting:** οι παραπομπές της μορφής `[@SRC-…]` είναι σταθερά citation-ready source IDs. Στο T-711 μετατρέπονται μηχανικά σε τελική IEEE αρίθμηση χωρίς αλλαγή του νοήματος ή της πηγής.

## 2.1 Πράκτορες και διαδοχική λήψη αποφάσεων

Η ενισχυτική μάθηση (Reinforcement Learning, RL) μελετά προβλήματα στα οποία ένας πράκτορας αλληλεπιδρά διαδοχικά με ένα περιβάλλον, επιλέγει ενέργειες και λαμβάνει παρατηρήσεις και ανταμοιβές. Σε αντίθεση με supervised learning, η επιθυμητή συμπεριφορά δεν παρέχεται ως σύνολο σωστών labels για κάθε κατάσταση. Ο πράκτορας πρέπει να μάθει μια πολιτική που μεγιστοποιεί τη μελλοντική απόδοση μέσω της ίδιας της αλληλεπίδρασης [@SRC-701E163AC8].

Η διαδοχικότητα είναι κρίσιμη: μια ενέργεια δεν αξιολογείται μόνο από την άμεση ανταμοιβή της, αλλά και από το πώς επηρεάζει τις μελλοντικές καταστάσεις και ευκαιρίες. Για αυτό η λήψη αποφάσεων σε RL συνδέεται με την αναμενόμενη σωρευτική επιστροφή και με την ισορροπία μεταξύ exploitation της ήδη αποκτημένης γνώσης και exploration για συλλογή νέας εμπειρίας [@SRC-701E163AC8].

Η παρούσα εργασία εστιάζει σε ένα επιπλέον πρόβλημα: τι συμβαίνει όταν η σχέση μεταξύ καταστάσεων, ενεργειών, παρατηρήσεων και ανταμοιβών δεν παραμένει σταθερή μετά την αρχική μάθηση. Σε stationary setting η εμπειρία του παρελθόντος μπορεί να παραμένει έγκυρη. Σε non-stationary setting, ορισμένες εκτιμήσεις, πολιτικές ή learned models μπορεί να γίνουν stale και ο πράκτορας πρέπει είτε να διατηρήσει επαρκή απόδοση χωρίς αλλαγή είτε να προσαρμοστεί στη νέα συνθήκη.

## 2.2 Markov Decision Processes και Reinforcement Learning

Το κλασικό μαθηματικό πλαίσιο του RL είναι το Markov Decision Process (MDP). Ένα MDP περιγράφεται από σύνολο καταστάσεων \(\mathcal{S}\), σύνολο ενεργειών \(\mathcal{A}\), δυναμική μετάβασης, συνάρτηση ανταμοιβής και συντελεστή προεξόφλησης \(\gamma\). Η Markov ιδιότητα εκφράζει ότι, δεδομένης της τρέχουσας κατάστασης και ενέργειας, η κατανομή της επόμενης κατάστασης δεν χρειάζεται ολόκληρο το ιστορικό για να οριστεί [@SRC-701E163AC8].

Μια policy \(\pi(a\mid s)\) ορίζει πώς επιλέγεται ενέργεια σε μια κατάσταση. Η state-value function \(V^\pi(s)\) περιγράφει την αναμενόμενη discounted return από μια κατάσταση ακολουθώντας την policy, ενώ η action-value function \(Q^\pi(s,a)\) περιγράφει την αντίστοιχη αναμενόμενη return όταν πρώτα επιλεγεί η ενέργεια \(a\) [@SRC-701E163AC8].

Στα temporal-difference methods, οι value estimates ενημερώνονται από bootstrapped targets που συνδυάζουν την άμεση ανταμοιβή με εκτίμηση μελλοντικής αξίας. Η δυνατότητα online ενημέρωσης χωρίς πλήρες μοντέλο του περιβάλλοντος καθιστά τις TD μεθόδους φυσικές baselines για μελέτη adaptation.

Η κλασική θεωρία συνήθως προϋποθέτει stationary dynamics ή άλλες συνθήκες που δεν ταυτίζονται με persistent αλλαγή κατά τη deployment φάση. Επομένως, η επιτυχής συμπεριφορά ενός αλγορίθμου σε stationary learning δεν συνεπάγεται αυτομάτως αποτελεσματική tracking συμπεριφορά μετά από environmental change.

## 2.3 Q-Learning και SARSA

Η Q-Learning και η SARSA είναι δύο κλασικές tabular TD-control μέθοδοι που διαφέρουν κυρίως στον one-step update target [@SRC-701E163AC8; @SRC-D52DF7B9A4].

Στη Q-Learning, η ενημέρωση μπορεί να γραφτεί ως:

\[
Q(s_t,a_t) \leftarrow Q(s_t,a_t) + \alpha\left[r_{t+1}+\gamma \max_a Q(s_{t+1},a)-Q(s_t,a_t)\right].
\]

Ο target χρησιμοποιεί greedy μέγιστο στην επόμενη κατάσταση. Για αυτό η Q-Learning χαρακτηρίζεται off-policy: η behavior policy που παράγει εμπειρία μπορεί να είναι exploratory, ενώ ο update target αναφέρεται σε greedy action value.

Στη SARSA, ο target χρησιμοποιεί την επόμενη ενέργεια που επιλέγεται από την τρέχουσα behavior policy:

\[
Q(s_t,a_t) \leftarrow Q(s_t,a_t) + \alpha\left[r_{t+1}+\gamma Q(s_{t+1},a_{t+1})-Q(s_t,a_t)\right].
\]

Η SARSA είναι επομένως on-policy. Υπό exploratory behavior, η διαφορά αυτή μπορεί να επηρεάσει τη συμπεριφορά που μαθαίνεται, επειδή η SARSA ενσωματώνει στον target τις συνέπειες των ενεργειών που πραγματικά επιλέγονται από την exploratory policy [@SRC-701E163AC8; @SRC-D52DF7B9A4].

Στην παρούσα εργασία η Q-Learning και η SARSA επιλέγονται ως ερμηνεύσιμο off-policy/on-policy tabular contrast υπό ίδιο state/action representation και ίδιο information contract. Η επιλογή τους δεν προϋποθέτει ότι κάποια από τις δύο είναι θεωρητικά «πιο ανθεκτική». Η ανθεκτικότητα και η recovery παραμένουν εμπειρικά outcomes.

## 2.4 Deep Q-Network

Η Deep Q-Network (DQN) επεκτείνει τη value-based λογική σε νευρωνική προσέγγιση της action-value function και αποτελεί βασικό σημείο αναφοράς του deep RL [@SRC-32A0866AF8]. Η DQN χρησιμοποιεί experience replay ώστε οι μεταβάσεις να αποθηκεύονται και να επαναχρησιμοποιούνται για updates, και target network ώστε οι bootstrapped targets να μεταβάλλονται πιο ελεγχόμενα.

Το replay δεν είναι ουδέτερη λεπτομέρεια αποθήκευσης. Το μέγεθος του buffer, η συχνότητα sampling και ο λόγος πραγματικής εμπειρίας προς replay updates μπορούν να επηρεάσουν ουσιαστικά τη συμπεριφορά μάθησης [@SRC-CBA29E303A]. Αυτό έχει ιδιαίτερη σημασία σε non-stationary settings, επειδή ένα replay buffer μπορεί να περιλαμβάνει τόσο πρόσφατη post-change εμπειρία όσο και stale pre-change transitions.

Στην παρούσα εργασία δεν εφαρμόζεται ειδικό replay reset ή reweighting μετά τη μεταβολή. Η Adaptive DQN branch συνεχίζει τη φυσική training διαδικασία της frozen configuration. Η επιλογή αυτή επιτρέπει να μετρηθεί η συμπεριφορά του standard mechanism χωρίς να προστεθεί ξεχωριστή continual-learning intervention.

## 2.5 Proximal Policy Optimization

Η Proximal Policy Optimization (PPO) είναι on-policy policy-gradient μέθοδος. Η βασική της ιδέα είναι η βελτιστοποίηση clipped surrogate objective ώστε να περιορίζονται υπερβολικά μεγάλες policy updates μεταξύ διαδοχικών iterations [@SRC-CD5F67F3E6].

Σε αντίθεση με value-based tabular methods, η PPO μαθαίνει απευθείας parametrized policy και value function. Η observed performance εξαρτάται όχι μόνο από το high-level clipped objective αλλά και από implementation details όπως rollout length, minibatch size, αριθμό epochs, advantage estimation, optimizer settings και network architecture [@SRC-5D0E7E5BD7].

Αυτό είναι σημαντικό για την ερμηνεία της παρούσας σύγκρισης. Η PPO δεν αντιμετωπίζεται ως «robust» επειδή περιορίζει το μέγεθος policy updates. Το clipping αφορά optimization stability και δεν αποτελεί εγγύηση απέναντι σε αλλαγή transition/action semantics. Η actual resilience μετράται από το ίδιο frozen protocol που εφαρμόζεται στις υπόλοιπες μεθόδους.

## 2.6 Dyna και Dyna-Q+

Η Dyna αρχιτεκτονική συνδυάζει άμεση μάθηση από πραγματική εμπειρία με μάθηση μοντέλου και πρόσθετα planning updates πάνω σε model-generated experience [@SRC-701E163AC8]. Μια πραγματική μετάβαση μπορεί να ενημερώσει τόσο τις action-value estimates όσο και ένα empirical model, το οποίο στη συνέχεια επιτρέπει επιπλέον backups χωρίς νέες πραγματικές αλληλεπιδράσεις.

Σε changing environment, η model-based προσέγγιση δημιουργεί και μια ειδική ευπάθεια: αν η δυναμική αλλάξει, μέρος του learned model μπορεί να παραμείνει stale μέχρι να ξαναπαρατηρηθούν τα επηρεασμένα state-action pairs. Planning πάνω σε stale model μπορεί προσωρινά να ενισχύσει παλιές εκτιμήσεις [@SRC-701E163AC8].

Η Dyna-Q+ εισάγει directed re-exploration με recency-based bonus για state-action pairs που δεν έχουν δοκιμαστεί πρόσφατα. Η λογική είναι ότι οι συνέπειες μιας παλιάς action μπορεί να έχουν αλλάξει, επομένως η συστηματική επανεξέταση παλιών ενεργειών μπορεί να βοηθήσει στην ανακάλυψη αλλαγής [@SRC-701E163AC8]. Το exploration bonus έχει όμως κόστος: η δοκιμή παλιών ή αβέβαιων ενεργειών μπορεί να μειώσει προσωρινά την άμεση ανταμοιβή.

Η παρούσα μελέτη διατηρεί τη Dyna-Q+ στην τελική πεντάδα ως planning/re-exploration comparator. Η ύπαρξη learned model δεν αντιμετωπίζεται ως θεωρητική εγγύηση adaptation superiority.

## 2.7 Non-stationarity και δυναμικές μεταβολές

Σε non-stationary RL, η κατανομή καταστάσεων, rewards, transitions ή άλλων περιβαλλοντικών παραμέτρων μπορεί να μεταβάλλεται κατά τη διάρκεια training/deployment. Η αλλαγή μπορεί να είναι abrupt ή gradual, observed ή latent, προσωρινή ή persistent. Οι διαφορετικές μορφές non-stationarity δημιουργούν διαφορετικές απαιτήσεις adaptation και δεν είναι επιστημονικά σωστό να αντιμετωπίζονται ως μία ενιαία disturbance category [@SRC-660560956D].

Η continual-RL βιβλιογραφία τονίζει την ανάγκη να διατηρείται ισορροπία ανάμεσα στη retention παλαιάς γνώσης και στην plasticity για νέα γνώση. Deep agents μπορούν να εμφανίσουν interference, primacy effects ή loss of plasticity κατά την παρατεταμένη μάθηση [@SRC-4C34DF3E17; @SRC-46CF36BC1E]. Αυτά τα ευρήματα δεν προβλέπουν συγκεκριμένη αποτυχία των DQN/PPO στο παρόν GridWorld, αλλά αιτιολογούν γιατί η απλή συνέχιση gradient-based training δεν πρέπει να θεωρείται αυτόματα επαρκής adaptation strategy.

Το πρόσφατο ICLR 2025 work για online RL σε non-stationary context-driven environments εξετάζει catastrophic forgetting και stability/plasticity σε continual deployment [@SRC-6F4F8BE003]. Η εργασία δίνει στην policy ρητό exogenous context και συνεπώς λειτουργεί σε διαφορετικό information regime από το παρόν hidden action-remap setting. Η διάκριση observed versus hidden context είναι κεντρική για τη σωστή μεταφορά συμπερασμάτων μεταξύ μελετών.

## 2.8 Action uncertainty, observation uncertainty και hidden change

Η παρούσα διπλωματική διαχωρίζει τρεις μορφές disturbance.

Η **persistent action remapping** αλλάζει τη σημασιολογία της ενέργειας χωρίς να αλλάζει το ονομαστικό action set. Ο agent εξακολουθεί να επιλέγει, για παράδειγμα, `right`, αλλά το περιβάλλον μπορεί να εκτελεί τη συνέπεια που προηγουμένως αντιστοιχούσε στο `down`. Η αλλαγή δεν ανακοινώνεται με explicit change indicator.

Η **action failure** εισάγει stochastic actuation uncertainty. Η intended action μπορεί να αποτύχει με προκαθορισμένη πιθανότητα. Σε αυτή την περίπτωση η underlying mapping δεν αντικαθίσταται από νέο μόνιμο regime με τον ίδιο τρόπο όπως στο action remap.

Η **observation corruption** εισάγει information/perception uncertainty. Ο agent μπορεί να λάβει observation που δεν αντιστοιχεί στην evaluator true state. Η condition αυτή είναι conceptually διαφορετική από transition/action uncertainty, επειδή το learning update μπορεί να βασίζεται σε αλλοιωμένο input.

Οι conditions δεν συνδυάζονται σε ενιαίο uncertainty score. Η ίδια η τελική εμπειρική ανάλυση δείχνει ότι η online adaptation έχει διαφορετική επίδραση στις τρεις families.

## 2.9 Ανθεκτικότητα, προσαρμογή και ανάκαμψη

Η έννοια της ανθεκτικότητας σε sequential decision systems μπορεί να αναλυθεί σε διαφορετικές συνιστώσες αντί να αντιμετωπιστεί ως ένας αδιαφανής αριθμός. Για την παρούσα εργασία είναι χρήσιμη η διάκριση ανάμεσα σε:

- **resistance/degradation:** πόσο μειώνεται η επίδοση όταν εμφανίζεται disturbance,
- **adaptation benefit:** κατά πόσο η συνέχιση της μάθησης μειώνει αυτή την απώλεια σε σχέση με frozen deployment,
- **recovery:** αν και πότε η adaptive disturbed trajectory επιστρέφει σε προκαθορισμένη γειτονιά της adaptive nominal reference.

Η διάκριση αυτή είναι project-specific operationalization και δεν παρουσιάζεται ως universal standard. Το four-branch FN/FD/AN/AD design είναι επίσης πειραματική κατασκευή της παρούσας εργασίας, σχεδιασμένη ώστε να απομονώνει το όφελος adaptation από nominal drift και από τη βασική επίδραση της disturbance.

Η recovery απαιτεί ξεχωριστή αντιμετώπιση επειδή περιλαμβάνει event-like timing και πιθανότητα μη ανάκαμψης. Αν ένας agent δεν ανακάμψει μέσα στο observation horizon, η τιμή αυτή πρέπει να παραμείνει right-censored και να μη μετατραπεί σε ψευδή observed time ίσο με το horizon.

## 2.10 Continual adaptation, replay και model organization

Η ordinary continued training δεν είναι η μόνη δυνατή προσέγγιση σε changing environments. Η ευρύτερη βιβλιογραφία περιλαμβάνει changepoint detection, context inference, memory/replay management, meta-learning, specialized continual-learning regularization και uncertainty-aware planning [@SRC-660560956D].

Το ICLR 2025 context-driven work δείχνει ένα παράδειγμα όπου retained past experience χρησιμοποιείται για να περιοριστούν destructive policy changes σε παλιότερα contexts, αντί να χρησιμοποιείται απλώς ως stale on-policy training data [@SRC-6F4F8BE003]. Η σχεδίαση αυτή αντιμετωπίζει ρητά το stability/plasticity trade-off, αλλά απαιτεί observed context information που δεν υπάρχει στην παρούσα μελέτη.

Στη model-based πλευρά, η εργασία *Partial Models for Building Adaptive Model-Based Reinforcement Learning Agents* δείχνει ότι ένα μονολιθικό learned model και ένα ενιαίο replay/history mechanism μπορούν να δυσκολέψουν local adaptation όταν τμήμα του environment distribution αλλάξει [@SRC-D38364B32C]. Οι συγγραφείς αναδεικνύουν ένα interference-versus-forgetting trade-off: μεγάλο history μπορεί να κρατά stale transitions, ενώ πολύ περιορισμένο history μπορεί να ξεχνά παλιά αλλά ακόμη έγκυρη γνώση. Η partial-model παρέμβασή τους βελτιώνει adaptation σε συγκεκριμένα deep Dyna-Q/PlaNet/Dreamer setups, αλλά δεν μπορεί να μεταφερθεί απευθείας στην tabular Dyna-Q+ της παρούσας εργασίας.

Οι δύο πρόσφατες εργασίες χρησιμοποιούνται συνεπώς για να τοποθετήσουν τα αποτελέσματα μέσα σε ευρύτερη continual-adaptation συζήτηση, όχι για να δημιουργήσουν εκ των υστέρων causal explanation της observed συμπεριφοράς.

## 2.11 Empirical RL design και δίκαιη σύγκριση

Η αξιόπιστη σύγκριση RL methods είναι ιδιαίτερα ευαίσθητη σε random variation, hyperparameter choices, environment selection και reporting choices [@SRC-4ED8B918E3; @SRC-8D4F62D85D]. Για αυτό μια σύγκριση πέντε ετερογενών methods δεν μπορεί να βασιστεί απλώς στο «ίδιο πλήθος επεισοδίων» ή σε ένα seed.

Η βιβλιογραφία empirical RL design υποστηρίζει την ανάγκη για πολλαπλές ανεξάρτητες runs/roots, δίκαιη tuning opportunity, σαφές common experience budget και αναφορά uncertainty [@SRC-4ED8B918E3; @SRC-8D4F62D85D]. Η παρούσα εργασία εφαρμόζει αυτές τις αρχές με actual-environment interactions ως κύριο budget, 12 independent roots και frozen tuning/configuration πριν από confirmatory outcomes.

Ιδιαίτερη προσοχή απαιτούν και τα time limits. Ένα administrative episode cutoff δεν είναι κατ' ανάγκη terminal state του underlying continuing problem. Η βιβλιογραφία time-limit handling δείχνει ότι η λανθασμένη αντιμετώπιση truncation ως πραγματικού terminal μπορεί να αλλάξει τα learning targets [@SRC-69D02D7E25]. Για αυτό το project διατηρεί explicit διάκριση `terminated`/`truncated` και bootstrapping semantics σύμφωνα με το frozen task contract.

## 2.12 Σχετικές εμπειρικές προσεγγίσεις και θέση της μελέτης

Η υπάρχουσα βιβλιογραφία καλύπτει πολλές διαφορετικές όψεις του προβλήματος: standard TD control, deep value learning, policy optimization, model-based planning, continual RL, plasticity/forgetting, replay management και local adaptation. Ωστόσο, οι μελέτες διαφέρουν σε environments, information assumptions, budgets και στόχους, οπότε οι αποτελεσματικές συγκρίσεις απαιτούν ρητή αναφορά των transfer boundaries.

Η παρούσα εργασία δεν επιχειρεί να αναπαράγει ένα μεγάλο continual-RL benchmark ούτε να καλύψει όλες τις algorithm families. Επιλέγει πέντε μηχανιστικά διαφορετικές και υλοποιήσιμες methods ώστε να εξεταστούν κάτω από **ένα κοινό, αυστηρά ελεγχόμενο protocol**:

- off-policy tabular TD control,
- on-policy tabular TD control,
- deep value learning με replay,
- on-policy policy-gradient optimization,
- learned-model planning με directed re-exploration.

Η προσέγγιση αυτή επιτρέπει να διαχωριστούν τρία ερωτήματα που συχνά συμπλέκονται: πόσο αποτελεσματικά μαθαίνει ένας agent nominally, αν continued learning μειώνει aggregate disturbance loss και αν η policy επανέρχεται σταθερά κοντά στην matched nominal adaptive trajectory.

## 2.13 Ερευνητικό κενό και θέση της παρούσας εργασίας

Το ερευνητικό κενό που αντιμετωπίζει η εργασία δεν είναι η απουσία αλγορίθμων για non-stationary RL. Η βιβλιογραφία διαθέτει πολλές specialized λύσεις. Το ερώτημα της παρούσας μελέτης είναι πιο συγκεκριμένο: **πώς συμπεριφέρονται διαφορετικοί standard RL mechanisms όταν αξιολογούνται υπό κοινό information contract, κοινό actual-interaction budget και matched hidden-change deployment, με χωριστή μέτρηση adaptation benefit και recovery;**

Η εργασία τοποθετείται ανάμεσα σε δύο άκρα. Από τη μία, stationary benchmark comparisons δεν εξετάζουν ρητά τη post-change behavior. Από την άλλη, specialized continual-RL systems συχνά εισάγουν additional context, detectors, memory rules ή architectural priors. Η παρούσα μελέτη κρατά τους πέντε methods κοντά στη standard operation τους και μεταβάλλει ελεγχόμενα το environment contract μετά από exact scientific checkpoint.

Με αυτόν τον τρόπο, τα τελικά αποτελέσματα μπορούν να διαβαστούν ως controlled baseline για resilience/adaptation mechanisms και όχι ως ανταγωνισμός όλων των σύγχρονων continual-RL τεχνικών. Η θέση αυτή καθορίζει και την ερμηνεία των επόμενων κεφαλαίων: η εργασία αξιολογεί συγκεκριμένα mechanisms υπό συγκεκριμένο contract και διατηρεί ρητά τα όρια μεταφοράς σε broader settings.