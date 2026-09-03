# Κεφάλαιο 4 — Αρχιτεκτονική και Υλοποίηση του Ερευνητικού Συστήματος

## 4.1 Στόχος της υλοποίησης

Η υλοποίηση της παρούσας εργασίας σχεδιάστηκε ώστε να υποστηρίζει ένα πλήρες ερευνητικό lifecycle: ορισμό πειραματικής συνταγής, deterministic σχεδιασμό εργασιών, εκπαίδευση και deployment, ακριβή checkpoints, matched branches, επικύρωση evidence, στατιστική ανάλυση, παραγωγή reproducible figures/tables και τελική επιθεώρηση μέσω desktop εφαρμογής. Η αρχιτεκτονική δεν αντιμετωπίζει το γραφικό περιβάλλον ως επιστημονικό κέντρο του συστήματος. Αντίθετα, η επιστημονική λογική βρίσκεται σε framework-neutral Python modules, ενώ η εφαρμογή PySide6 λειτουργεί ως thin presentation/control layer πάνω από αποθηκευμένη και επαληθευμένη κατάσταση.

Η βασική σχεδιαστική αρχή είναι ο διαχωρισμός μεταξύ **επιστημονικής αυθεντίας** και **παρουσίασης**. Οι αποφάσεις για RNG, training state, checkpoints, branch construction, estimands, root/layout reductions, recovery classification, intervals, validation και finalization ανήκουν αποκλειστικά στο backend. Το UI μπορεί να ζητήσει μια επιτρεπόμενη ενέργεια ή να προβάλλει ήδη αποθηκευμένη πληροφορία, αλλά δεν επιτρέπεται να ανακατασκευάζει επιστημονικές τιμές από raw data ούτε να αλλάζει την πορεία του πειράματος μέσω presentation state.

## 4.2 Δομή του κώδικα και επιστημονικός πυρήνας

Ο ενεργός κώδικας βρίσκεται κάτω από το `src/resilient_agents/`. Η δομή χωρίζει τον ελεγχόμενο κόσμο, τις μεθόδους, τα πειραματικά contracts, το Study lifecycle, την evidence/analysis αλυσίδα και το desktop interface σε ανεξάρτητα επίπεδα με σαφή όρια ευθύνης.

Ο πυρήνας υλοποιεί το project-owned Gymnasium GridWorld, τις tabular μεθόδους Q-Learning, SARSA και Dyna-Q+, καθώς και adapters για DQN/PPO μέσω Stable-Baselines3. Η κοινή διεπαφή δεν προσπαθεί να εξαλείψει τις method-native διαφορές. Αντίθετα, επιβάλλει όσα πρέπει να είναι κοινά για την επιστημονική σύγκριση — πραγματικές αλληλεπιδράσεις, observation/action semantics, checkpoint identity και evaluator boundary — και επιτρέπει σε κάθε μέθοδο να διατηρεί το state που απαιτεί η δική της δυναμική.

Ιδιαίτερη σημασία έχει ο διαχωρισμός ground truth και agent-visible information. Το περιβάλλον και ο evaluator γνωρίζουν, για παράδειγμα, αν εφαρμόστηκε action remap ή observation corruption, όμως ο agent δεν λαμβάνει αυτές τις flags όταν το protocol το απαγορεύει. Η πληροφορία που είναι χρήσιμη για validation και visualization δεν μετατρέπεται αυτόματα σε πληροφορία διαθέσιμη στη policy.

## 4.3 Study ως μονάδα εκτέλεσης και provenance

Η τελική εκτέλεση οργανώνεται γύρω από την έννοια του `Study`. Το Study δεν είναι απλώς ένας φάκελος αποτελεσμάτων, αλλά versioned πειραματική οντότητα με immutable recipe, deterministic plan, durable lifecycle state και καταγεγραμμένο provenance.

Η `StudyRecipe` κωδικοποιεί την επιστημονική πρόθεση: protocol identity, methods, roots, layouts, phases, conditions, budgets και authorization requirements. Από τη recipe ο planner παράγει deterministic job plan. Το plan περιγράφει την εξάρτηση των σταδίων και επιτρέπει στο σύστημα να γνωρίζει ποια jobs μπορούν να εκτελεστούν, ποια πρέπει να περιμένουν προηγούμενο stage και ποια αποτελούν validation/analysis/export handoff.

Το package `src/resilient_agents/study/` περιλαμβάνει, μεταξύ άλλων, μοντέλα lifecycle, planner, execution ports/default executors και εξειδικευμένη protocol-v2.1 Phase-B εκτέλεση. Η ύπαρξη explicit model/planner/lifecycle στρώματος επιτρέπει restart-safe λειτουργία: η πρόοδος δεν εξαρτάται από το αν ένα συγκεκριμένο UI process παραμένει ανοιχτό ούτε από transient in-memory state.

Το `StudyStore` λειτουργεί ως durable αποθήκη της κατάστασης του Study. Jobs, status transitions, artifact registrations και lineage παραμένουν διαθέσιμα μετά από restart. Η filesystem evidence παραμένει η κύρια αυθεντία, ενώ indexes ή βοηθητικές βάσεις αντιμετωπίζονται ως rebuildable caches και όχι ως μοναδική πηγή αλήθειας.

## 4.4 Deterministic planning και stage barriers

Το scientific workflow είναι πολυσταδιακό και έχει πραγματικές εξαρτήσεις. Μια Phase-B branch δεν μπορεί να εκτελεστεί πριν υπάρξει το σωστό Phase-A checkpoint. Η ανάλυση δεν μπορεί να προηγηθεί της validation/freeze του accepted evidence. Για αυτό, το Study plan περιλαμβάνει stage barriers.

Η τυπική ακολουθία είναι:

1. materialization της παγωμένης recipe,
2. παραγωγή deterministic job plan,
3. Phase-A ανεξάρτητη ονομαστική μάθηση,
4. δημιουργία exact checkpoints,
5. matched Phase-B FN/FD/AN/AD branches,
6. validation της evidence αλυσίδας,
7. analysis/export jobs,
8. downstream freeze και παραγωγή thesis assets.

Τα barriers μειώνουν τον κίνδυνο να χρησιμοποιηθεί προσωρινό ή μη επικυρωμένο artifact σε επόμενο επιστημονικό στάδιο. Η λογική είναι fail-closed: όταν ένα required artifact ή state δεν είναι έγκυρο, το downstream stage δεν «προσπαθεί να συνεχίσει» με μερική υπόθεση.

## 4.5 Checkpoints και ακριβής συνέχεια της μάθησης

Η Phase B απαιτεί πραγματική συνέχεια από το τέλος της Phase A. Για τον λόγο αυτό, το checkpoint δεν περιορίζεται σε ένα μικρό σύνολο weights ή Q-values όταν αυτά δεν αρκούν για να αναπαράγουν τη method-native κατάσταση.

Στις tabular μεθόδους διατηρείται η κατάλληλη κατάσταση τιμών και εξερεύνησης. Στη DQN η ακριβής συνέχεια απαιτεί, μεταξύ άλλων, policy/target network state, replay buffer, optimizer και exploration schedule. Στην PPO απαιτούνται optimizer/schedule/RNG και η κατάλληλη update-boundary κατάσταση. Στη Dyna-Q+ το learned model, η recency πληροφορία και το planning state αποτελούν μέρος της επιστημονικής συνέχειας.

Το checkpoint lineage καταγράφεται ρητά. Έτσι, κάθε Phase-B branch μπορεί να αναχθεί στο συγκεκριμένο Phase-A checkpoint από το οποίο προήλθε. Η matched σύγκριση Frozen/Adaptive δεν βασίζεται σε δύο ανεξάρτητα trainings που απλώς έχουν ίδιο seed, αλλά σε branches από κοινό επιστημονικό state.

## 4.6 RNG isolation και reproducibility

Η αναπαραγωγιμότητα ενισχύεται με ξεχωριστά RNG streams. Κάθε τελική root διαθέτει διακριτά seeds για initialization, exploration, scenario, environment, action disturbance και observation disturbance. Η επιλογή αυτή αποτρέπει την ακούσια επαναχρησιμοποίηση μιας τυχαίας ακολουθίας για δύο λογικά διαφορετικές πηγές τυχαιότητας.

Η deterministic συμπεριφορά δεν σημαίνει ότι το πείραμα είναι ντετερμινιστικό ως προς κάθε αποτέλεσμα. Σημαίνει ότι, για την ίδια recipe, το ίδιο root specification και το ίδιο source state, η ακολουθία τυχαιότητας μπορεί να αναπαραχθεί. Η διακύμανση μεταξύ roots αποτελεί μέρος του πειράματος και δεν «εξαλείφεται» από το σύστημα.

Οι scientific failures επίσης δεν αντικαθίστανται από νέες ευνοϊκότερες roots. Η ταυτότητα root είναι προκαθορισμένη και διατηρείται. Αυτό είναι κρίσιμο για να μην εισαχθεί outcome-driven seed selection.

## 4.7 Run bundles, manifests και ακεραιότητα

Κάθε ολοκληρωμένη επιστημονική μονάδα αποθηκεύεται ως run bundle με machine-readable metadata, επιστημονική ταυτότητα και checksums. Η finalization ακολουθεί controlled διαδικασία: τα απαιτούμενα artifacts πρέπει να υπάρχουν, οι hashes να συμφωνούν και το bundle να βρίσκεται σε συνεπή lifecycle state πριν χαρακτηριστεί finalized.

Τα manifests χρησιμοποιούνται για δύο λόγους. Πρώτον, επιτρέπουν να ελεγχθεί ότι ένα downstream analysis καταναλώνει ακριβώς το accepted evidence set. Δεύτερον, καθιστούν ανιχνεύσιμη οποιαδήποτε μεταγενέστερη αλλαγή αρχείου που θα αλλοίωνε την ακεραιότητα του πακέτου.

Στην τελική αλυσίδα, το T-611 πάγωσε το accepted evidence υπό συγκεκριμένο manifest SHA-256, το T-612 παρήγαγε deterministic analysis package και το T-613 παρήγαγε registered figures/tables με δικό τους asset manifest. Η συγγραφή δεν διαβάζει αυθαίρετα raw files για να ξαναϋπολογίσει τιμές: χρησιμοποιεί την ήδη επικυρωμένη downstream αλυσίδα.

## 4.8 Evidence-v2 validation και analysis layer

Το `src/resilient_agents/evidence_v2/` υλοποιεί τη protocol-v2.1 validation/analysis/export διαδρομή. Το validation ελέγχει όχι μόνο το σχήμα των αρχείων αλλά και την ταυτότητα του πειράματος: method/root/layout/condition consistency, checkpoint lineage, matched branch composition, temporal window records και unique scientific identities.

Για το RQ3 απαιτείται schema-v2 temporal evidence, επειδή ο υπολογισμός της ανάκαμψης βασίζεται σε διαδοχικά fixed interaction windows και right-censoring. Ο validator απορρίπτει ασύμβατη ή ελλιπή temporal evidence αντί να παράγει recovery result από μερικό input.

Το analysis layer εφαρμόζει την προκαθορισμένη equal-layout root reduction, τα pointwise Student-t intervals, τα root-paired contrasts και τις recovery summaries. Οι λειτουργίες αυτές δεν εκτελούνται στο UI. Η ίδια machine-readable analysis authority τροφοδοτεί τόσο τις τελικές T-613 εξαγωγές όσο και την read-only παρουσίαση αποτελεσμάτων.

## 4.9 Χειρισμός αποτυχίας και το T-610 recovery path

Η αρχιτεκτονική σχεδιάστηκε ώστε μια αποτυχία να μην καταστρέφει ή να ξαναγράφει την επιστημονική ιστορία. Αυτό φάνηκε στην πρώτη τελική προσπάθεια T-610. Η εκτέλεση σταμάτησε μετά από 216 jobs όταν η πρώτη SARSA Phase-B εργασία εντόπισε μη-quiescent learner state στο shared no-learning prefix.

Το σύστημα δεν παρέκαμψε το precondition ούτε τροποποίησε το checkpoint κατά την εκτέλεση. Η αποτυχία καταγράφηκε και η αρχική Study παρέμεινε immutable, ενεργή/μη finalized ιστορική προσπάθεια. Η αιτία εντοπίστηκε σε implementation omission: το generic Phase-A materialization path δεν εφάρμοζε το ήδη αποδεκτό deployment-start settlement που είχε οριστεί πριν από τα τελικά αποτελέσματα.

Η διόρθωση έγινε σε νέο source commit και η replacement Study απέκτησε ξεχωριστή execution identity `protocol-v2.1-final--t610-recovery-01`, ενώ η scientific recipe και το deterministic plan παρέμειναν αμετάβλητα. Δεν επαναχρησιμοποιήθηκε κανένα από τα 216 ολοκληρωμένα bundles της αποτυχημένης προσπάθειας. Η replacement execution ξεκίνησε από μηδενική κατάσταση και ολοκλήρωσε το πλήρες 603-job plan.

Η περίπτωση αυτή αποτελεί πρακτικό παράδειγμα της διάκρισης μεταξύ implementation recovery και scientific amendment. Αν η διόρθωση απαιτούσε αλλαγή hyperparameter, estimand, method ή condition με γνώση των αποτελεσμάτων, θα χρειαζόταν διαφορετική επιστημονική διακυβέρνηση. Εδώ εφαρμόστηκε ένας ήδη παγωμένος κανόνας που έλειπε από συγκεκριμένο execution boundary.

## 4.10 Desktop εφαρμογή PySide6

Η τελική εφαρμογή υλοποιείται με PySide6 / Qt 6 Widgets. Η επιλογή αυτή διατηρεί ολόκληρη τη στοίβα σε Python και επιτρέπει άμεση σύνδεση με το framework-neutral backend χωρίς HTTP service ή δεύτερο scientific middle layer. Το UI παραμένει research interface και όχι ανεξάρτητη πηγή επιστημονικής λογικής.

Η τελική πληροφοριακή αρχιτεκτονική είναι **Experiment / Run / Results / Evidence**. Η οργάνωση είναι experiment-first: ο χρήστης κατανοεί πρώτα τι συγκρίνεται και μετά βλέπει τα εσωτερικά execution/evidence mechanics.

### 4.10.1 Experiment

Η επιφάνεια Experiment παρουσιάζει την παγωμένη Thesis experiment ως read-only. Δείχνει τις πέντε fixed methods, τη Phase A, τη μετάβαση σε matched Phase B, τις disturbance families και τον ρόλο των Frozen/Adaptive regimes. Τεχνικά IDs, roots, layout hashes και checkpoint στοιχεία παραμένουν διαθέσιμα με progressive disclosure αντί να κυριαρχούν στην κύρια ροή.

Για DEVELOPMENT/Exploratory studies επιτρέπεται ξεχωριστή backend-constrained ροή Configure → Review → Create. Αυτές οι studies επισημαίνονται ρητά ως μη confirmatory και δεν μπορούν να χρησιμοποιήσουν final-reserve identities ως thesis evidence.

### 4.10.2 Run

Η επιφάνεια Run προβάλλει την τρέχουσα phase και το GridWorld. Στη Phase A κυριαρχεί ένα μεγάλο nominal GridWorld για την τρέχουσα μέθοδο. Στη Phase B, όταν υπάρχουν ακριβώς matched presentation events, εμφανίζονται ταυτόχρονα δύο panels: Frozen — learning off και Adaptive — learning continues.

Το UI δεν κατασκευάζει ψευδή αντιστοίχιση frames. Αν δεν υπάρχει exact matched pair για method/root/layout/condition/interaction, το δηλώνει αντί να συνδυάζει άσχετες μεταβάσεις. Τα live events είναι lossy και non-blocking: μπορούν να χαθούν frames χωρίς να επηρεάζεται το scientific execution.

### 4.10.3 Results

Η επιφάνεια Results οργανώνεται ρητά σε RQ1 Learning, RQ2 Resilience/Adaptation και RQ3 Recovery. Οι πίνακες και τα γραφήματα είναι projections ήδη stored/validated outputs. Το UI δεν εκτελεί root reductions, threshold selection ή statistical interval calculation.

Στο RQ3, ειδικά, η εφαρμογή διαχωρίζει recovered proportion, observed recovery time conditional on recovery και restricted delay. Μη ανάκαμψη διατηρεί `recovery_time=null`. Με αυτόν τον τρόπο η παρουσίαση δεν μετατρέπει το fixed horizon σε ψευδή παρατηρούμενο χρόνο.

### 4.10.4 Evidence

Η επιφάνεια Evidence απαντά πρώτα σε λειτουργικά ερωτήματα: ποια evidence packages υπάρχουν, ποια είναι validated/finalized και ποια exports είναι διαθέσιμα. Artifact IDs, paths, hashes, source job IDs και lineage εμφανίζονται ως technical detail. Η εφαρμογή δεν λειτουργεί ως αυθαίρετος filesystem browser.

## 4.11 Live visualization και επιστημονική παθητικότητα

Η live απεικόνιση σχεδιάστηκε με ρητό one-way boundary. Ο execution engine μπορεί να εκπέμπει presentation events. Το UI μπορεί να τα εμφανίζει, να τα ομαδοποιεί για οπτική χρήση και να απορρίπτει παλαιότερα frames όταν δεν προλαβαίνει να τα αποδώσει. Δεν επιτρέπεται όμως επιστροφή πληροφορίας από τη visualization state προς την policy ή το scheduler.

Η τρέχουσα intended action, η executed action, η reward, η delivered observation και η true evaluator state μπορούν να εμφανίζονται για inspection όταν επιτρέπεται, αλλά η ύπαρξή τους στην οθόνη δεν αλλάζει το agent-visible information contract. Η οπτικοποίηση είναι παρατηρητής, όχι συμμετέχων στο πείραμα.

Αυτό το όριο είναι επίσης σημαντικό για την απόδοση. Η scientific execution δεν πρέπει να περιμένει το frame rate του GUI. Αν το UI καθυστερεί, η απεικόνιση μπορεί να χάσει events, ενώ τα επιστημονικά logs και artifacts εξακολουθούν να καταγράφονται πλήρως από το backend.

## 4.12 Execution supervision και restart safety

Η εφαρμογή δεν εκτελεί βαριά scientific jobs στο Qt UI thread. Η επίβλεψη γίνεται μέσω non-blocking process supervision, ώστε το interface να παραμένει responsive και να μην συγχέεται η κατάσταση ενός GUI process με την κατάσταση ενός Study.

Η durable Study κατάσταση επιτρέπει resume/retry μόνο σύμφωνα με τις backend lifecycle rules. Ένα infrastructure failure δεν μετατρέπεται σε νέο scientific root ούτε δίνει δικαίωμα για αυθαίρετη επανεκκίνηση με άλλο seed. Αντίστοιχα, η απουσία του UI δεν σημαίνει ότι τα ήδη finalized artifacts χάνουν την αυθεντία τους.

## 4.13 Final-reserve firewall και authorization

Το protocol-v2.1 αποθηκεύτηκε με `final_reserve_access=false` και `execution_authorization=requires-explicit-t610-gate`. Η εφαρμογή δεν μπορούσε να παρακάμψει αυτή την κατάσταση ούτε να δημιουργήσει μόνη της authorization token.

Η τελική εκτέλεση ενεργοποιήθηκε μόνο μετά από ξεχωριστή ρητή authorization. Το token εφαρμόστηκε στο backend execution path χωρίς να μεταβάλει τα immutable protocol fields. Η σχεδίαση αυτή διαχωρίζει τη δυνατότητα μιας εφαρμογής να εμφανίζει ένα κουμπί από την επιστημονική άδεια να χρησιμοποιηθεί το final reserve.

## 4.14 Παραγωγή αποτελεσμάτων και thesis assets

Μετά την ολοκλήρωση της accepted execution, το T-611 δημιούργησε frozen evidence package. Το T-612 αναπαρήγαγε την canonical analysis και τα machine-readable exports από αυτό το package. Το T-613 παρήγαγε 31 figures, 12 table assets και 117 registered output variants σε reproducible μορφές, με SVG/PDF/300-DPI PNG για figures και canonical CSV/Markdown όπου απαιτείται για tables.

Η διαδρομή αυτή σημαίνει ότι τα figures της διπλωματικής δεν δημιουργούνται χειροκίνητα από screenshots ή με αντιγραφή αριθμών σε spreadsheet. Κάθε quantitative asset έχει source-artifact lineage και hash registration. Η μελλοντική τοποθέτηση στο Word έγγραφο είναι presentation εργασία· η αριθμητική του πηγή παραμένει το accepted analysis.

## 4.15 Έλεγχος ποιότητας και αναπαραγωγιμότητας της εφαρμογής

Η validation στρατηγική είναι risk-based. Χρησιμοποιούνται targeted tests για contracts, checkpoints, lifecycle, read models, UI boundary και critical scientific invariants, μαζί με canonical repository CI. Τα scientific experiment matrices δεν επαναλαμβάνονται ως unit-test matrices.

Για την desktop εφαρμογή, deterministic screenshot validation χρησιμοποιήθηκε για representative states σε 1366×768 και 1440×900, συμπεριλαμβανομένων Experiment, Run Phase A/B, RQ1/RQ2/RQ3, recovered/right-censored cases, Evidence και onboarding/lock states. Οι screenshots ελέγχουν presentation regressions, όχι scientific correctness των αριθμών· η correctness των scientific outputs ελέγχεται από το backend validation.

## 4.16 Συνολική αρχιτεκτονική ροή

Η τελική αρχιτεκτονική μπορεί να συνοψιστεί ως εξής:

**Frozen protocol/configuration → immutable Study recipe → deterministic plan → Phase-A execution → exact checkpoint → matched Phase-B branches → validated evidence → frozen evidence package → predeclared analysis → deterministic thesis assets → read-only Results/Evidence presentation.**

Η ροή αυτή επιτρέπει να απαντηθούν διαφορετικά ερωτήματα με διαφορετικά επίπεδα αυθεντίας. Ο πειραματικός σχεδιασμός καθορίζεται από το protocol. Η εκτέλεση και τα checkpoints από το backend. Η αποδοχή των δεδομένων από τους validators. Οι αριθμητικές ερμηνείες από το T-612 analysis. Τα figures/tables από το T-613. Το UI και η τελική διπλωματική παρουσιάζουν αυτά τα artifacts χωρίς να τα επαναϋπολογίζουν.

Η επιλογή αυτή αυξάνει το implementation overhead σε σχέση με ένα απλό script που εκπαιδεύει μοντέλα και τυπώνει μέσους όρους. Ωστόσο, είναι ουσιώδης για το συγκεκριμένο ερευνητικό ερώτημα, επειδή η αξιολόγηση ανθεκτικότητας βασίζεται σε matched states, persistent disturbances, right-censoring και αυστηρή provenance αλυσίδα. Η αρχιτεκτονική επομένως δεν αποτελεί απλώς software packaging της μελέτης· αποτελεί μηχανισμό προστασίας της επιστημονικής της ερμηνείας.