# Project Context

## Status taxonomy

- **CONFIRMED:** προκύπτει από επίσημη αίτηση ή ρητή τρέχουσα οδηγία χρήστη.
- **RESEARCH_REQUIRED:** πρέπει να αξιολογηθεί εκ νέου με σύγχρονη έρευνα πριν γίνει πρόταση ή απόφαση.
- **PROPOSED:** τεκμηριωμένη πρόταση που δεν έχει εγκριθεί ακόμη.
- **OPEN:** λείπει κρίσιμη πληροφορία ή απόφαση.
- **UNVERIFIED:** έχει αναφερθεί αλλά δεν έχει ελεγχθεί σε πρωτογενή πηγή, κώδικα ή πραγματικό σύστημα.
- **HISTORICAL_CONTEXT_ONLY:** εμφανίστηκε σε παλιά συνομιλία και διατηρείται μόνο για ιστορική κατανόηση· δεν είναι candidate ή preference από μόνο του.

## Τι είναι το project

Το project είναι η πλήρης ερευνητική, πειραματική, τεχνική και συγγραφική υποδομή της διπλωματικής εργασίας:

> **Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα**

Ακαδημαϊκό πλαίσιο - **CONFIRMED**:

- Πανεπιστήμιο Δυτικής Αττικής.
- Σχολή Μηχανικών.
- Τμήμα Μηχανικών Πληροφορικής και Υπολογιστών.
- Διπλωματική εργασία του Τμήματος, σύμφωνα με την επίσημη αίτηση.
- Συγγραφή στα ελληνικά και τελικό παραδοτέο Microsoft Word.

Το όνομα του επιβλέποντα, οι ειδικές απαιτήσεις του και η προθεσμία παραμένουν **OPEN**.

## Επίσημος ακαδημαϊκός σκοπός

Η επίσημη αίτηση ορίζει ως σκοπό τη μελέτη και συγκριτική αξιολόγηση ανθεκτικών πρακτόρων AI σε περιβάλλοντα αβεβαιότητας και δυναμικών μεταβολών. Μέσω απλού προσομοιωμένου περιβάλλοντος πρέπει να συγκριθούν αλγόριθμοι λήψης αποφάσεων ως προς την ικανότητά τους να προσαρμόζονται σε απρόβλεπτες αλλαγές. Η αίτηση δίνει ως παραδείγματα:

- θόρυβο δεδομένων,
- μεταβολή κανόνων,
- αποτυχίες εκτέλεσης ενεργειών.

Η αξιολόγηση πρέπει να εξετάζει την ανθεκτικότητα και την ταχύτητα ανάκαμψης.

## Βιβλιογραφία και επιστημονικό evidence

Η βιβλιογραφία δεν διαχειρίζεται πλέον πρωτογενώς σε αυτό το repository.

Το ιδιωτικό `MariosGiannakaras/ThesisBibliography` είναι η ανεξάρτητη canonical πηγή αλήθειας για source discovery, metadata, originals, Markdown/OCR, επιστημονική ανάλυση, verified evidence, inclusion/exclusion decisions και controlled thesis export.

Η πρώτη πλήρης επιστημονική διαλογή έχει ολοκληρωθεί εκεί για **486/486 ενεργές πηγές**. Το canonical status καταγράφει **104 επιλεγμένες/επαληθευμένες πηγές**, **381 απορρίψεις**, **1 theory-only/non-citation source**, **0 εκκρεμείς αποφάσεις** και **104/104 verified evidence sets**.

Το παρόν repository καταναλώνει μόνο το verified generated package στο `research/bibliography/`, δεμένο με ακριβές `SOURCE_COMMIT`. Δεν αντιγράφει όλο το bibliography repository, PDFs ή raw conversion material και δεν συγχωνεύει τα histories.

Η σύνδεση είναι pull-based και μέσω Pull Request. Η δεσμευτική αρχιτεκτονική βρίσκεται στα `docs/context/BIBLIOGRAPHY_INTEGRATION.md` και `bibliography/README.md`.

Τα source-derived scientific δεδομένα και citation-ready evidence παραμένουν στην αυθεντική γλώσσα της πηγής. Μετάφραση για το ελληνικό τελικό κείμενο γίνεται μόνο στο writing stage και δεν αντικαθιστά το original-language evidence record.

Οι literature refresh gates παραμένουν ενεργοί πριν από protocol freeze, βασικά writing gates και τελική υποβολή. Οι νέες αναζητήσεις και επαληθεύσεις γίνονται στο `ThesisBibliography` και εισάγονται εδώ μόνο μετά από νέο verified export.

## Ρόλος του GridWorld

Το GridWorld είναι η τρέχουσα επιβεβαιωμένη κατεύθυνση για το απλό ελεγχόμενο περιβάλλον. Η τελική υλοποίηση δεν έχει επιλεγεί.

Η επιλογή θα γίνει από μηδενική βάση μεταξύ:

1. σύγχρονης βιβλιοθήκης/framework που θα υιοθετηθεί ή προσαρμοστεί,
2. μικρού custom implementation,
3. συνδυασμού βιβλιοθήκης και project-specific wrappers/extensions.

Δεν υπάρχει απαίτηση ανάκτησης παλιού user-owned code. Οποιοδήποτε τρίτο repository ή package πρέπει να βρεθεί μέσω νέας έρευνας και να περάσει license, maintenance, API, determinism, testability και suitability audit πριν ληφθεί ή ενσωματωθεί.

Το τελικό περιβάλλον πρέπει να επιτρέπει:

- σαφείς states, actions, goals, obstacles, rewards και termination semantics,
- παραμετροποιημένες μορφές uncertainty/change,
- seeded και επαναλήψιμα experiments,
- trace/metric/artifact production,
- εκτέλεση ανεξάρτητα από το dashboard.

## Ρόλος των μοντέλων

Τα μοντέλα/αλγόριθμοι είναι οι συγκρινόμενοι πράκτορες ή baselines. **Δεν υπάρχει shortlist από τις παλιές συνομιλίες.** Η επιλογή θα γίνει από το verified bibliography evidence, το τελικό GridWorld/observability framing, το hardware/software inventory, feasibility prototypes και pilots.

Το `MODEL_CANDIDATES.md` είναι διαδικασία επιλογής και evidence matrix, όχι κατάλογος προεπιλεγμένων μοντέλων.

## Ρόλος των experiments

Τα experiments είναι το κύριο μέσο παραγωγής επιστημονικών ευρημάτων. Πρέπει να:

- χρησιμοποιούν προκαθορισμένο protocol,
- περιλαμβάνουν πολλαπλά seeds/repetitions,
- διαχωρίζουν pilot, exploratory και final runs,
- αποθηκεύουν πλήρες run provenance,
- καταγράφουν failures/cancellations/exclusions,
- επιτρέπουν δίκαιη στατιστική σύγκριση,
- παράγουν πραγματικά figures και tables.

Κανένας ιστορικός αριθμός runs, seeds, budget ή hyperparameter δεν μεταφέρεται ως default ή candidate χωρίς νέα αιτιολόγηση.

## Ρόλος του dashboard

Το dashboard είναι υποστηρικτικό εργαλείο για έναν τοπικό χρήστη. Πρέπει να μειώνει την ανάγκη χειροκίνητων scripts/console commands και να προσφέρει configuration, run control, πραγματικά status/progress/logs/metrics, GridWorld visualization, history/comparison, exports και screenshots.

Δεν είναι το κύριο research contribution και δεν προηγείται του core.

## Ρόλος της συγγραφής

Η συγγραφή εξελίσσεται παράλληλα με την υλοποίηση, αλλά κάθε κεφάλαιο διαχωρίζει verified facts/citations, proposed methodology, frozen protocol, πραγματικά results, interpretation και limitations. Τα τελικά συμπεράσματα γράφονται μόνο από το frozen final result set.

Οι βιβλιογραφικοί ισχυρισμοί συνδέονται με canonical `SRC-XXXXXXXXXX` identifiers που υπάρχουν στο imported manifest και με verified evidence από το αντίστοιχο `SOURCE_COMMIT`.

## Σύνδεση εφαρμογής, αποτελεσμάτων και κειμένου

```text
Official topic + verified bibliography + system inventory
          ↓
Research questions / hypotheses
          ↓
GridWorld build/reuse decision + model/metric selection
          ↓
Versioned experiment protocol
          ↓
Independent core + validated pilots
          ↓
Immutable raw results + provenance
          ↓
Processing scripts → figures/tables
          ↓
Dashboard exploration + thesis evidence
          ↓
Greek Microsoft Word thesis
```

## Τι λείπει

- Πραγματικό automated hardware/software inventory και capability benchmark.
- Νέα GridWorld landscape review και build/reuse/integration απόφαση, χρησιμοποιώντας το verified bibliography evidence ως βάση.
- Επιβλέπων και ειδικές ακαδημαϊκές οδηγίες.
- Τελικά research questions/hypotheses.
- Final environment variants, models, metrics και statistical protocol.
- Τρέχον επίσημο Word template/submission package.
- Πρώτος συγχρονισμός του verified `ThesisBibliography` package στο `research/bibliography/` μετά την ενεργοποίηση του read-only sync credential.
