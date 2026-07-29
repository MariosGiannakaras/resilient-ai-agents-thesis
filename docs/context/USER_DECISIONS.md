# User Decisions

## Application and operation

- Η εφαρμογή θα χρησιμοποιείται κυρίως τοπικά.
- Υπάρχει ένας χρήστης.
- Δεν απαιτούνται authentication, accounts, roles ή multi-user behavior.
- Δεν απαιτείται δημόσιο deployment, cloud infrastructure, mobile app ή online live demo.
- Το dashboard πρέπει να επιτρέπει χρήση χωρίς συνεχή χειροκίνητη εκτέλεση scripts/console commands.
- Η εφαρμογή θα παρουσιαστεί ως μέρος της εργασίας και θα παρέχει screenshots/visual evidence.
- Η εμφάνιση πρέπει να είναι σύγχρονη, αλλά είναι κατώτερη προτεραιότητα από science/correctness/reproducibility.

## Priority order

1. Επιστημονική εγκυρότητα.
2. Ορθότητα υλοποίησης.
3. Αναπαραγωγιμότητα.
4. Αξιοπιστία.
5. Χρηστικότητα.
6. Καθαρή οπτικοποίηση.
7. Animations και αισθητικές λεπτομέρειες.

## Research and runs

- Θα υπάρχουν διαφορετικά runs και settings ανά μοντέλο.
- Θα χρησιμοποιούνται πολλαπλά seeds και ανεξάρτητες επαναλήψεις· ο αριθμός δεν έχει οριστικοποιηθεί.
- Θα υπάρχουν pilot, exploratory και final runs.
- Θα καταγράφονται failures, cancellations, interruptions και incomplete runs.
- Θα υποστηρίζονται pause, resume, stop, cancel και restart όπου είναι τεχνικά εφικτό.
- Θα μπορεί να επανεκτελείται συγκεκριμένο run.
- Θα αποθηκεύονται οι πραγματικές παράμετροι κάθε run.
- Τα τελικά figures/tables θα παράγονται από πραγματικά δεδομένα, όχι mock values.
- Η επιλογή μοντέλων, hyperparameters, ranges, seeds και repetitions θα γίνει μετά από βιβλιογραφία, GridWorld review, pilots και resource assessment.

## Architecture

- Ο ερευνητικός πυρήνας θα είναι ανεξάρτητος από το UI.
- Το dashboard δεν θα ξεκινήσει πριν επαληθευτεί ο πυρήνας.
- Δεν θα υιοθετηθεί περίπλοκη υποδομή χωρίς πραγματική ανάγκη.
- Δεν έχει κλειδωθεί τεχνολογικό stack.

## Thesis

- Η συγγραφή θα γίνει στα ελληνικά.
- Το τελικό παραδοτέο θα είναι Microsoft Word.
- Θα ερευνηθούν οι επίσημες οδηγίες του Τμήματος και πρόσφατες εγκεκριμένες εργασίες.
- Οι επίσημες οδηγίες υπερισχύουν των παραδειγμάτων παλιών εργασιών.
- Δεν υπάρχει γνωστή προθεσμία.
- Η συγγραφή θα προχωρά παράλληλα, αλλά conclusions/results μόνο από πραγματικά δεδομένα.
- Απαγορεύεται η επινόηση πηγών, DOI, measurements, results και conclusions.

## Repository and privacy

- Το repository είναι ιδιωτικό και ανήκει στον προσωπικό GitHub λογαριασμό.
- Η επίσημη αίτηση αποθηκεύεται αυτούσια παρότι περιέχει προσωπικά στοιχεία.
- Η πραγματική βιβλιογραφία μπορεί να αποθηκευτεί στο ιδιωτικό repository.
- Τα raw chat exports χρησιμοποιούνται μόνο για extraction και δεν γίνονται commit.
- Όλο το project context πρέπει να βρίσκεται σε version-controlled αρχεία ώστε το Codex να μην χρειάζεται πρόσβαση στα chats.

## Hardware

- Έχει αναφερθεί περίπου AMD Ryzen 5 2600X και MSI Radeon RX 570 8 GB.
- Το πραγματικό inventory θα επιβεβαιωθεί από το σύστημα.
- Δεν θα υποτεθεί NVIDIA/CUDA ή απεριόριστο compute.
- Προτιμάται CPU-compatible path όταν η AMD GPU δεν έχει τεκμηριωμένη υποστήριξη/ωφέλεια.

## Optional AI in the dashboard

- Επιτρέπεται μόνο αν προσφέρει πραγματική αξία, όπως descriptive summary, anomaly flagging ή run triage.
- Δεν δημιουργεί/αλλάζει δεδομένα, δεν αντικαθιστά statistics και δεν παράγει ανεξέλεγκτο τελικό επιστημονικό κείμενο.
- Αν δεν υπάρχει σαφές benefit, δεν ενσωματώνεται.
