# Κεφάλαιο 7 — Συμπεράσματα και Μελλοντική Εργασία

## 7.1 Συνολική αποτίμηση

Η παρούσα διπλωματική μελέτησε συγκριτικά πέντε μεθόδους ενισχυτικής μάθησης — Q-Learning, SARSA, DQN, PPO και Dyna-Q+ — σε ελεγχόμενο GridWorld με κοινό interaction budget, κοινό information contract και matched post-change deployment. Η μελέτη διαχώρισε ρητά τρεις έννοιες που συχνά συγχέονται: την ονομαστική ικανότητα μάθησης πριν από μεταβολή, το aggregate όφελος της συνεχιζόμενης προσαρμογής μετά από disturbance και τη χρονική ανάκαμψη μετά από persistent αλλαγή.

Η συνεισφορά της εργασίας δεν βρίσκεται σε έναν νέο αλγόριθμο. Βρίσκεται στον ελεγχόμενο συγκριτικό σχεδιασμό, στην ακριβή συνέχεια από Phase-A checkpoints προς matched FN/FD/AN/AD branches, στον διαχωρισμό Frozen και Adaptive deployment regimes, στην προκαθορισμένη αντιμετώπιση right-censoring για recovery και στη reproducible αλυσίδα από frozen protocol μέχρι machine-readable analysis και thesis assets.

## 7.2 Απάντηση στο RQ1 — Ονομαστική μάθηση

Το πρώτο ερευνητικό ερώτημα αφορούσε τη σχετική ονομαστική επίδοση και learning efficiency των πέντε μεθόδων κάτω από κοινό budget πραγματικών αλληλεπιδράσεων.

Η Q-Learning, η SARSA και η Dyna-Q+ κατέληξαν στην ίδια τελική mean return, -0,100, στο probe των 8.192 interactions. Η Dyna-Q+ όμως είχε σαφώς υψηλότερη time-average επίδοση (-0,485) από SARSA (-1,611) και Q-Learning (-1,628), γεγονός που δείχνει ταχύτερη αξιοποίηση του διαθέσιμου interaction budget. Οι DQN και PPO είχαν χαμηλότερη τελική mean return (-1,862) και χαμηλότερες time-average τιμές, μαζί με μεγαλύτερη μεταξύ-root μεταβλητότητα.

Η απάντηση στο RQ1 είναι επομένως διπλή. Ως προς το τελικό nominal level, οι τρεις tabular/planning μέθοδοι δεν διαχωρίστηκαν. Ως προς τη learning efficiency, η Dyna-Q+ είχε το ισχυρότερο αποτέλεσμα. Το εύρημα παραμένει περιορισμένο στο συγκεκριμένο controlled task, budget και frozen configuration set.

## 7.3 Απάντηση στο RQ2 — Ανθεκτικότητα και προσαρμογή

Το δεύτερο ερευνητικό ερώτημα εξέτασε αν η online συνέχιση της μάθησης μειώνει τη disturbance-associated απώλεια σε σχέση με frozen deployment.

Στα δύο persistent action remaps, η Q-Learning και η SARSA εμφάνισαν μεγάλο και συνεπές θετικό adaptation benefit. Η Dyna-Q+ παρουσίασε επίσης θετικό benefit, αλλά μικρότερο σε βασικές συγκρίσεις. Η DQN είχε μικρότερο ή αβέβαιο benefit και η PPO περίπου μηδενικό aggregate benefit στα remaps.

Η εικόνα άλλαξε στις stochastic uncertainty conditions. Στην action failure 15% δεν παρατηρήθηκε καθαρό aggregate πλεονέκτημα της online adaptation. Στην observation corruption 5%, η Q-Learning και η SARSA είχαν αρνητικό adaptation benefit, δηλαδή η συνέχιση της μάθησης συνδέθηκε με μεγαλύτερη σχετική disturbance-associated απώλεια στο συγκεκριμένο estimand.

Η απάντηση στο RQ2 είναι ότι η προσαρμογή είναι **condition-dependent**. Η δυνατότητα ενός agent να συνεχίζει να ενημερώνεται δεν αποτελεί από μόνη της εγγύηση ανθεκτικότητας. Είναι ιδιαίτερα ωφέλιμη όταν πρέπει να μάθει μια νέα persistent σχέση μεταξύ ενεργειών και συνεπειών, αλλά μπορεί να μην προσφέρει όφελος ή ακόμη και να επιδεινώσει την επίδοση όταν το learning signal αλλοιώνεται από θόρυβο παρατήρησης.

## 7.4 Απάντηση στο RQ3 — Ανάκαμψη

Το τρίτο ερευνητικό ερώτημα αφορούσε τη stable recovery μετά από persistent action remapping, με primary tolerance 0,10, passive windows 32 interactions και απαίτηση δύο συνεχόμενων qualifying windows.

Η Q-Learning και η SARSA ανακτήθηκαν και στις 12 roots και στα δύο action remaps. Στο cycle remap, η Q-Learning είχε χαμηλότερο restricted delay από τη SARSA, ενώ στο swap οι δύο μέθοδοι δεν διαχωρίστηκαν καθαρά. Η Dyna-Q+ ανακτήθηκε σε 12/12 roots στο cycle αλλά σε 8/12 στο swap. Η DQN είχε 2/12 και 8/12 recoveries αντίστοιχα, ενώ η PPO 1/12 και 4/12.

Το RQ3 δείχνει ότι aggregate adaptation benefit και recovery speed δεν είναι ισοδύναμες έννοιες. Μια μέθοδος μπορεί να μειώνει αισθητά τη συνολική post-change απώλεια αλλά να χρειάζεται περισσότερο χρόνο για να πλησιάσει σταθερά την Adaptive-Nominal reference trajectory ή να μην ανακτά σε όλες τις roots μέσα στον fixed horizon.

Η sensitivity analysis επιβεβαίωσε επίσης ότι η ακριβής recovery incidence εξαρτάται από την ανοχή. Η Q-Learning και η SARSA παρέμειναν οι πιο συνεπείς μέθοδοι, αλλά DQN, Dyna-Q+ και PPO παρουσίασαν μεγάλες μεταβολές μεταξύ tolerance 0,05, 0,10 και 0,20. Επομένως, η recovery πρέπει πάντοτε να αναφέρεται μαζί με τον operational ορισμό της.

## 7.5 Κύρια συνεισφορά της εργασίας

Η εργασία καταλήγει σε πέντε κύριες συνεισφορές.

Πρώτον, υλοποιεί ένα ελεγχόμενο multi-method πειραματικό πλαίσιο όπου η συγκρισιμότητα βασίζεται σε κοινές πραγματικές αλληλεπιδράσεις με το περιβάλλον και όχι σε τεχνητή εξίσωση method-native updates.

Δεύτερον, εισάγει και εφαρμόζει matched four-branch σχεδιασμό FN/FD/AN/AD από exact scientific checkpoints. Ο σχεδιασμός επιτρέπει να διαχωριστεί η disturbance-associated loss από την επίδραση της online learning και να υπολογιστεί ρητά το adaptation benefit.

Τρίτον, αντιμετωπίζει την ανάκαμψη ως ξεχωριστό temporal construct. Η χρήση fixed interaction windows, stable two-window criterion, explicit right-censoring και restricted-horizon comparison αποτρέπει την αντικατάσταση μη παρατηρημένης ανάκαμψης με τεχνητό χρόνο ίσο με το horizon.

Τέταρτον, διατηρεί πλήρη reproducibility/provenance αλυσίδα: frozen recipe, deterministic job plan, exact checkpoints, run-bundle manifests, frozen evidence, deterministic analysis και registered thesis assets. Η αποτυχημένη πρώτη T-610 εκτέλεση διατηρήθηκε ως ξεχωριστή ιστορική προσπάθεια και δεν αναμίχθηκε με το accepted evidence.

Πέμπτον, η τελική desktop εφαρμογή προσφέρει experiment-first inspection του workflow και των αποτελεσμάτων χωρίς να μεταφέρει επιστημονικούς υπολογισμούς στο UI. Έτσι, η οπτικοποίηση και η χρηστικότητα δεν αλλοιώνουν τα estimands ή την evidence authority.

## 7.6 Τι δεν υποστηρίζει η εργασία

Η μελέτη δεν υποστηρίζει ότι υπάρχει καθολικά καλύτερος αλγόριθμος reinforcement learning για dynamic environments. Δεν υποστηρίζει ότι η Dyna-Q+ είναι γενικά ανώτερη επειδή είχε καλύτερη sample efficiency ούτε ότι Q-Learning/SARSA είναι γενικά πιο resilient επειδή είχαν πιο συνεπή recovery στο συγκεκριμένο testbed.

Δεν υποστηρίζει επίσης ότι το PPO clipping αποτελεί environmental robustness mechanism ή ότι ένα learned model εγγυάται ταχεία adaptation. Οι παρατηρούμενες διαφορές αφορούν τις frozen configurations και το συγκεκριμένο πειραματικό contract.

Η μελέτη δεν αξιολογεί explicit change detection, context inference, meta-learning, specialized continual-learning regularization, safe RL constraints ή large-scale world models. Αυτές οι τεχνικές αποτελούν διαφορετικές ερευνητικές παρεμβάσεις και δεν πρέπει να θεωρούνται «απούσες βελτιώσεις» που θα μπορούσαν να προστεθούν χωρίς αλλαγή του ερευνητικού ερωτήματος.

## 7.7 Μελλοντική εργασία

### 7.7.1 Διεύρυνση περιβαλλόντων και κλίμακας

Η πιο άμεση επέκταση είναι η αξιολόγηση σε περισσότερες οικογένειες περιβαλλόντων. Μεγαλύτερα GridWorlds, stochastic transition structures, continuous-control tasks ή πραγματικότερα navigation/control προβλήματα θα επέτρεπαν να εξεταστεί αν τα observed trade-offs παραμένουν όταν αυξάνεται η dimensionality και η δυσκολία representation.

Η διεύρυνση πρέπει να γίνει χωρίς να χαθεί το current scientific contract. Νέα environments θα πρέπει να διατηρούν σαφή agent-visible information boundary, reproducible disturbance definitions και ανεξάρτητη randomization unit.

### 7.7.2 Διαφορετικά budgets και learning timescales

Οι DQN και PPO δεν έφτασαν το τελικό nominal level των tabular methods εντός των 8.192 interactions. Μελλοντική μελέτη μπορεί να εξετάσει πολλαπλά προκαθορισμένα interaction budgets ώστε να διαχωριστεί η επίδραση της sample efficiency από την asymptotic capability.

Η επέκταση αυτή δεν πρέπει να γίνει με post-hoc αύξηση budget μόνο για μεθόδους που είχαν χαμηλή απόδοση. Απαιτεί νέο fair experimental design και εκ νέου freeze πριν από confirmatory outcomes.

### 7.7.3 Ρητή ανίχνευση αλλαγής και context inference

Η παρούσα εργασία μελετά hidden change χωρίς explicit detector. Μελλοντική εργασία μπορεί να συγκρίνει την ordinary method-native adaptation με agents που ανιχνεύουν changepoints ή εκτιμούν latent context.

Μια τέτοια σύγκριση θα μπορούσε να εξετάσει το κόστος detection latency, false alarms και context misclassification, καθώς και αν η ρητή αλλαγή καθεστώτος βελτιώνει recovery χωρίς να επιδεινώνει nominal performance.

### 7.7.4 Specialized continual-learning mechanisms

Η continual-RL βιβλιογραφία περιλαμβάνει μηχανισμούς για retention, stability/plasticity και recurring contexts. Μελλοντικό protocol θα μπορούσε να προσθέσει τέτοιες μεθόδους ως ξεχωριστή algorithm/intervention family, αντί να τις συγχέει με το simple «learning continues» του παρόντος Adaptive regime.

Ιδιαίτερο ενδιαφέρον έχει η σύγκριση ordinary replay με memory mechanisms που διαχωρίζουν current-regime optimization από retention constraints, καθώς και η επίδραση explicit context availability.

### 7.7.5 Modular model-based adaptation

Τα αποτελέσματα της Dyna-Q+ δείχνουν ότι planning και directed exploration δεν αρκούν για να εγγυηθούν την ταχύτερη recovery σε κάθε change. Μελλοντική εργασία μπορεί να εξετάσει modular ή partial model architectures, selective model invalidation και local model updating.

Η επέκταση αυτή θα πρέπει να διαχωρίζει καθαρά το model-organization intervention από το βασικό Dyna mechanism και να μην αποδίδει αποτελέσματα ενός deep partial-model system στην tabular Dyna-Q+ χωρίς άμεση πειραματική σύγκριση.

### 7.7.6 Διαχείριση replay υπό non-stationarity

Για DQN-like methods μπορεί να μελετηθεί ξεχωριστά η επίδραση replay retention, replay reweighting, context-aware sampling ή bounded forgetting μετά από change. Το βασικό trade-off είναι ότι πολύ stale memory μπορεί να εμποδίσει local adaptation, ενώ υπερβολική απόρριψη ιστορικής εμπειρίας μπορεί να προκαλέσει forgetting έγκυρης γνώσης.

Κάθε τέτοια παρέμβαση πρέπει να οριστεί ως νέα μέθοδος ή deployment policy και όχι ως «τεχνική λεπτομέρεια checkpoint».

### 7.7.7 Πλουσιότερη μελέτη recovery

Η παρούσα μελέτη χρησιμοποιεί 32-interaction windows και fixed horizon 256. Μελλοντική εργασία μπορεί να εξετάσει διαφορετικές προκαθορισμένες temporal resolutions, longer horizons ή event-time models που χειρίζονται censoring πιο άμεσα.

Απαιτείται προσοχή ώστε η μεγαλύτερη temporal ανάλυση να μην οδηγήσει σε post-hoc επιλογή window/tolerance που ευνοεί συγκεκριμένη μέθοδο. Η sensitivity analysis πρέπει να παραμένει προδηλωμένη.

### 7.7.8 Περισσότερες ανεξάρτητες roots και ιεραρχική ανάλυση

Το n=12 ήταν το frozen independent-root count της παρούσας μελέτης. Μελλοντικό μεγαλύτερο experiment θα μπορούσε να χρησιμοποιήσει περισσότερες roots ώστε να μειώσει την uncertainty των direct contrasts, ιδιαίτερα για methods με υψηλή variance.

Με περισσότερα environments/layout families θα μπορούσε επίσης να εξεταστεί hierarchical analysis που διαχωρίζει variation μεταξύ seeds, layouts και environment families χωρίς να αντιμετωπίζει nested observations ως ψευδώς ανεξάρτητα samples.

### 7.7.9 Safety και constraint-aware adaptation

Η ανθεκτικότητα και η ασφάλεια δεν είναι ταυτόσημες έννοιες. Η παρούσα εργασία δεν περιλαμβάνει safety constraints. Ένα μελλοντικό ξεχωριστό research track μπορεί να εξετάσει αν ένας agent προσαρμόζεται μετά από change χωρίς να παραβιάζει constraints κατά τη μεταβατική περίοδο.

Αυτό απαιτεί διαφορετικά estimands — όπως constraint violations, risk exposure ή safe recovery — και δεν πρέπει να προστεθεί εκ των υστέρων στο υπάρχον resilience score, το οποίο ούτως ή άλλως δεν είναι composite.

## 7.8 Τελικό συμπέρασμα

Η ελεγχόμενη σύγκριση δείχνει ότι η ανθεκτικότητα σε περιβάλλοντα που μεταβάλλονται δεν μπορεί να περιγραφεί μόνο από το αν ένας agent «συνεχίζει να μαθαίνει». Στο συγκεκριμένο testbed, η Dyna-Q+ αξιοποίησε αποτελεσματικότερα το nominal interaction budget, ενώ Q-Learning και SARSA παρουσίασαν την πιο συνεπή stable recovery μετά από persistent action remapping. Η online adaptation παρείχε μεγάλο όφελος σε ορισμένες μεταβολές αλλά όχι σε όλες, και στην observation corruption μπορούσε να συνδεθεί με χειρότερη aggregate συμπεριφορά.

Το κεντρικό συμπέρασμα είναι επομένως ότι η αξιολόγηση resilient AI agents απαιτεί ταυτόχρονη αλλά διακριτή μέτρηση της αρχικής ικανότητας μάθησης, της απώλειας υπό change, του οφέλους προσαρμογής και της ίδιας της χρονικής ανάκαμψης. Η μεθοδολογία της εργασίας επιχειρεί να παρέχει ακριβώς αυτή τη διάκριση, διατηρώντας παράλληλα το πείραμα αναπαραγώγιμο, ελέγξιμο και επιστημονικά περιορισμένο στα δεδομένα που πραγματικά παρήχθησαν.