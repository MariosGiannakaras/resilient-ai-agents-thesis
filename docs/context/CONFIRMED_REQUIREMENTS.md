# Confirmed Requirements

Το παρόν αρχείο περιλαμβάνει μόνο απαιτήσεις που επιβεβαιώνονται από τη νεότερη ρητή οδηγία του χρήστη, την επίσημη αίτηση ή επαληθευμένη επίσημη οδηγία. Οι υποψήφιες τεχνικές ή ερευνητικές επιλογές βρίσκονται στα αντίστοιχα candidate files.

**Status values:** `CONFIRMED`, `PARTIALLY_CONFIRMED`, `BLOCKED_BY_DECISION`, `DEFERRED`.

## Academic

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-ACA-001 | Η εργασία είναι διπλωματική του Τμήματος Μηχανικών Πληροφορικής και Υπολογιστών, Σχολή Μηχανικών, Πανεπιστήμιο Δυτικής Αττικής. | Επίσημη αίτηση. | CONFIRMED | Τα στοιχεία εμφανίζονται συνεπώς σε README, metadata και τελικό Word. |
| REQ-ACA-002 | Ο επίσημος ελληνικός τίτλος είναι «Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα». | Επίσημη αίτηση. | CONFIRMED | Χρήση ακριβούς τίτλου μέχρι επίσημη τροποποίηση. |
| REQ-ACA-003 | Ο επίσημος αγγλικός τίτλος είναι “Comparison and Evaluation of Resilient AI Agents in Uncertain Environments”. | Επίσημη αίτηση. | CONFIRMED | Χρήση ακριβούς τίτλου μέχρι επίσημη τροποποίηση. |
| REQ-ACA-004 | Ο επιβλέπων και τυχόν ειδικές απαιτήσεις του πρέπει να καταγραφούν πριν παγώσει η μεθοδολογία. | Λείπει από τα διαθέσιμα στοιχεία. | BLOCKED_BY_DECISION | Ενημερωμένα context files και decision entry. |
| REQ-ACA-005 | Οι ισχύουσες επίσημες οδηγίες του Τμήματος υπερισχύουν παραδειγμάτων από παλιές εργασίες. | Ρητή απόφαση χρήστη. | CONFIRMED | Formatting checklist συνδεδεμένο με επαληθευμένες επίσημες πηγές. |

## Research

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-RES-001 | Η έρευνα συγκρίνει και αξιολογεί ανθεκτικούς πράκτορες/αλγορίθμους λήψης αποφάσεων σε περιβάλλοντα αβεβαιότητας και δυναμικών μεταβολών. | Επίσημη αίτηση. | CONFIRMED | Research questions και experiment matrix συνδέονται άμεσα με αυτή την αποστολή. |
| REQ-RES-002 | Η μελέτη πρέπει να χρησιμοποιεί απλό προσομοιωμένο περιβάλλον, με το GridWorld ως τρέχουσα επιβεβαιωμένη κατεύθυνση. | Επίσημη αίτηση και νεότερες αποφάσεις. | CONFIRMED | Υπάρχει versioned, validated GridWorld specification. |
| REQ-RES-003 | Η αξιολόγηση πρέπει να εξετάζει προσαρμογή σε απρόβλεπτες αλλαγές, ανθεκτικότητα και ταχύτητα ανάκαμψης. | Επίσημη αίτηση. | CONFIRMED | Τουλάχιστον μία έγκυρη operational definition και metric για degradation/recovery. |
| REQ-RES-004 | Οι μορφές αβεβαιότητας πρέπει να οριστούν ρητά, να παραμετροποιούνται και να ελέγχονται πειραματικά. | Αναγκαιότητα δίκαιης αξιολόγησης· επίσημα παραδείγματα: noise, rule changes, action failures. | CONFIRMED | Κάθε disturbance έχει schema, severity levels, seed behavior και validation tests. |
| REQ-RES-005 | Η τελική λίστα μοντέλων επιλέγεται από μηδενική βάση μετά από αίτηση, fresh literature review, τελική GridWorld κατηγορία, system inventory, feasibility prototypes και pilots. | Ρητή τρέχουσα απόφαση χρήστη. | CONFIRMED | Decision log με verified sources και inclusion/exclusion rationale. |
| REQ-RES-006 | Το dashboard είναι υποστηρικτικό εργαλείο και όχι υποκατάστατο της ερευνητικής συνεισφοράς. | Ρητή απόφαση χρήστη. | CONFIRMED | Το contribution statement βασίζεται σε environment/protocol/results, όχι μόνο UI. |
| REQ-RES-007 | Οι παλιές συνομιλίες δεν αποτελούν model/metric/GridWorld/stack shortlist· όλες οι επιλογές γίνονται εκ νέου. | Ρητή τρέχουσα διευκρίνιση χρήστη. | CONFIRMED | Candidate/decision files βασίζονται σε fresh evidence και όχι σε historical mentions. |
| REQ-RES-008 | Το GridWorld implementation επιλέγεται μετά από σύγχρονη research comparison reuse/adapt/custom· δεν απαιτείται legacy code. | Ρητή τρέχουσα διευκρίνιση χρήστη. | CONFIRMED | Landscape review, prototype και ADR πριν download/integration. |

## Experimental

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-EXP-001 | Δεν επιτρέπεται σύγκριση μοντέλων από μία μόνο εκτέλεση. | Ρητή απόφαση χρήστη. | CONFIRMED | Κάθε final condition έχει πολλαπλά προδηλωμένα seeds/repetitions. |
| REQ-EXP-002 | Πρέπει να υπάρχουν διακριτά pilot, exploratory και final runs. | Ρητή απόφαση χρήστη. | CONFIRMED | Run metadata περιέχει `run_type`; final set είναι frozen. |
| REQ-EXP-003 | Διαφορετικά μοντέλα μπορούν να έχουν διαφορετικές κατάλληλες ρυθμίσεις, αλλά η αξιολόγηση πρέπει να παραμένει δίκαιη και τεκμηριωμένη. | Ρητή απόφαση χρήστη. | CONFIRMED | Tuning policy, common evaluation protocol και budget accounting καταγράφονται πριν final runs. |
| REQ-EXP-004 | Πρέπει να καταγράφονται failed, cancelled, interrupted, incomplete και excluded runs. | Ρητή απόφαση χρήστη. | CONFIRMED | Κανένα run δεν εξαφανίζεται από το registry· υπάρχει reason field. |
| REQ-EXP-005 | Πρέπει να αποθηκεύονται οι πραγματικά resolved παράμετροι κάθε run. | Ρητή απόφαση χρήστη. | CONFIRMED | Run manifest αποθηκεύεται κατά την έναρξη και κλειδώνει κατά την ολοκλήρωση. |
| REQ-EXP-006 | Τα final figures και tables παράγονται από πραγματικά αποθηκευμένα δεδομένα. | Ρητή απόφαση χρήστη. | CONFIRMED | Κάθε artifact έχει provenance manifest και reproducible generation command. |
| REQ-EXP-007 | Seeds, repetitions, ranges, stopping criteria και budgets επιλέγονται βάσει βιβλιογραφίας, pilots και πραγματικών resources. | Ρητή απόφαση χρήστη. | CONFIRMED | Pre-final protocol decision entry και budget estimate. |
| REQ-EXP-008 | Πρέπει να υπάρχει σαφές statistical analysis plan πριν εξεταστούν τα final αποτελέσματα. | Αποφυγή cherry-picking και post-hoc bias. | CONFIRMED | Frozen analysis config/plan με estimands, intervals, effect sizes και exclusions. |

## Functional application

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-APP-001 | Η εφαρμογή λειτουργεί τοπικά για έναν χρήστη. | Ρητή απόφαση χρήστη. | CONFIRMED | Core και dashboard εκκινούν τοπικά χωρίς account service. |
| REQ-APP-002 | Δεν απαιτούνται authentication, roles, multi-user ή public deployment. | Ρητή απόφαση χρήστη. | CONFIRMED | Δεν υπάρχουν auth flows ή cloud-only dependencies. |
| REQ-APP-003 | Ο χρήστης πρέπει να μπορεί να δημιουργεί και να επανεκτελεί runs χωρίς συνεχή χειροκίνητη χρήση console/scripts. | Ρητή απόφαση χρήστη. | CONFIRMED | UI workflow δημιουργεί validated config και εκκινεί πραγματικό runner. |
| REQ-APP-004 | Πρέπει να υποστηρίζονται pause, resume, stop, cancel και restart όπου είναι τεχνικά εφικτό. | Ρητή απόφαση χρήστη. | PARTIALLY_CONFIRMED | Capability matrix ανά runner/model· unsupported operations εμφανίζονται ρητά. |
| REQ-APP-005 | Η εφαρμογή πρέπει να εμφανίζει πραγματικό status, progress, logs, warnings, errors και metrics. | Ρητή απαίτηση και scientific integrity. | CONFIRMED | Κάθε UI state προέρχεται από backend state/event, όχι timer simulation. |
| REQ-APP-006 | Πρέπει να υπάρχουν run history, comparison, result exploration και export. | Ρητή απαίτηση χρήστη. | CONFIRMED | End-to-end workflow από run registry σε comparison/export. |
| REQ-APP-007 | Πρέπει να παρέχεται live GridWorld visualization όπου δεν επηρεάζει την πειραματική εκτέλεση. | Ρητή απαίτηση dashboard. | CONFIRMED | Visualization καταναλώνει trace/events και μπορεί να απενεργοποιηθεί. |
| REQ-APP-008 | CPU/RAM και, όπου υποστηρίζεται, GPU/VRAM usage πρέπει να εμφανίζονται ως πραγματικές μετρήσεις. | Ρητή απαίτηση dashboard. | CONFIRMED | Metrics source και unsupported states είναι εμφανή. |

## Architecture and technical

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-ARCH-001 | Ο ερευνητικός πυρήνας λειτουργεί ανεξάρτητα από το UI. | Ρητή απόφαση χρήστη. | CONFIRMED | CLI/API smoke test ολοκληρώνει run με το dashboard κλειστό. |
| REQ-ARCH-002 | Το dashboard δεν υλοποιείται πριν επαληθευτεί ο core. | Ρητή προτεραιότητα χρήστη. | CONFIRMED | Roadmap gate απαιτεί core tests και pilot evidence. |
| REQ-ARCH-003 | Η αποθήκευση των runs/results δεν εξαρτάται από lifecycle του UI. | Reliability/reproducibility. | CONFIRMED | UI crash/close δεν καταστρέφει manifest και partial outputs. |
| REQ-ARCH-004 | Αποφεύγονται microservices, Kubernetes, cloud και πολύπλοκο authentication χωρίς πραγματική ανάγκη. | Τοπικό single-user scope. | CONFIRMED | Architecture decision καταγράφει την απλούστερη επαρκή λύση. |
| REQ-ARCH-005 | Δεν επιλέγεται final stack πριν compatibility/prototyping review. | Ιστορικά αντικρουόμενα stacks. | CONFIRMED | ADR με alternatives, constraints και proof-of-concept evidence. |
| REQ-TECH-001 | Δεν υποτίθεται NVIDIA/CUDA ή usable GPU acceleration πριν από αυτόματο inventory και capability benchmark. | Ρητή τρέχουσα απόφαση χρήστη. | CONFIRMED | Capability report πριν από compute-dependent επιλογές. |
| REQ-TECH-002 | Το Codex συλλέγει αυτόματα CPU, RAM, GPU/VRAM, OS, drivers, runtimes και storage από το πραγματικό σύστημα πριν compute-dependent αποφάσεις. | Ρητή τρέχουσα απόφαση χρήστη. | CONFIRMED | Versioned system inventory και benchmark report χωρίς manual user transcription. |

## UI/UX

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-UI-001 | Η εμφάνιση πρέπει να είναι σύγχρονη και καθαρή. | Ρητή προτίμηση χρήστη. | CONFIRMED | Συνεπές design system και readable research views. |
| REQ-UI-002 | Η αισθητική δεν υπερισχύει correctness, reliability ή usability. | Ρητή σειρά προτεραιοτήτων. | CONFIRMED | No animation blocks execution or hides scientific state. |
| REQ-UI-003 | Δεν επιτρέπονται fake progress bars, mock final metrics, εικονικά logs ή backend-inconsistent states. | Ρητή απαγόρευση. | CONFIRMED | UI integration tests against real runner states. |
| REQ-UI-004 | Screenshots της εφαρμογής πρέπει να είναι κατάλληλα για παρουσίαση και διπλωματική. | Ρητή χρήση εφαρμογής. | CONFIRMED | Exportable, legible views με stable labels και timestamps/IDs όπου χρειάζεται. |

## Repository and provenance

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-REPO-001 | Το repository είναι ιδιωτικό και αποτελεί τη μόνιμη source of truth. | Ρητή απόφαση χρήστη. | CONFIRMED | Context/decisions/configs/results metadata version-controlled. |
| REQ-REPO-002 | Η επίσημη αίτηση αποθηκεύεται αυτούσια στο private repository. | Ρητή απόφαση χρήστη. | CONFIRMED | SHA-256 ισούται με το uploaded original. |
| REQ-REPO-003 | Τα raw chat exports δεν γίνονται commit. | Ρητή απόφαση χρήστη. | CONFIRMED | Secret/content scan δεν βρίσκει transcript archive/names. |
| REQ-REPO-004 | Δεν αποθηκεύονται secrets, tokens, passwords, credentials, virtual environments, caches ή άχρηστα build artifacts. | Security requirement. | CONFIRMED | `.gitignore`, review και automated secret scanning πριν release. |
| REQ-REPO-005 | Μεγάλα binaries/datasets/checkpoints αξιολογούνται πριν Git/LFS commit. | Repository maintainability. | CONFIRMED | Size/retention/LFS decision για κάθε artifact class. |
| REQ-PROV-001 | Κάθε αποτέλεσμα συνδέεται με run ID, source files, config, processing code και Git commit. | Ρητή provenance απαίτηση. | CONFIRMED | Machine-readable provenance manifest ανά artifact. |
| REQ-PROV-002 | Τα raw results είναι immutable. | Ρητή reproducibility αρχή. | CONFIRMED | Checksums και append-only policy· corrections ως νέα version. |

## Tests

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-TEST-001 | Το GridWorld χρειάζεται deterministic unit tests για transitions, rewards, termination και disturbance behavior. | Scientific validity. | CONFIRMED | Reference cases και property/invariant tests περνούν. |
| REQ-TEST-002 | Κάθε model adapter χρειάζεται contract tests. | Fair common interface. | CONFIRMED | Reset/act/train/evaluate/checkpoint contracts verified. |
| REQ-TEST-003 | Το experiment runner χρειάζεται integration tests για lifecycle, persistence, recovery και failure capture. | Reliability requirement. | CONFIRMED | Simulated interruption/restart tests preserve valid state. |
| REQ-TEST-004 | Processing/aggregation code χρειάζεται tests με known synthetic fixtures. | Statistical correctness. | CONFIRMED | Hand-calculated expected metrics match implementation. |
| REQ-TEST-005 | Reproducibility smoke tests πρέπει να διακρίνουν deterministic replay από statistical repeatability. | Honest reproducibility. | CONFIRMED | Documented test modes and tolerances. |

## Thesis and deliverables

| ID | Requirement | Source / rationale | Status | Acceptance criterion |
|---|---|---|---|---|
| REQ-THESIS-001 | Η διπλωματική γράφεται στα ελληνικά. | Ρητή απόφαση χρήστη. | CONFIRMED | Main text in Greek with consistent bilingual terminology. |
| REQ-THESIS-002 | Το τελικό παραδοτέο είναι Microsoft Word. | Ρητή απόφαση χρήστη. | CONFIRMED | Validated `.docx` with styles, fields and cross-references. |
| REQ-THESIS-003 | Η συγγραφή προχωρά παράλληλα, αλλά final results/conclusions βασίζονται αποκλειστικά σε πραγματικά frozen data. | Ρητή απόφαση χρήστη. | CONFIRMED | Claims map to run/artifact IDs. |
| REQ-THESIS-004 | Απαγορεύονται επινοημένες πηγές, DOI, μετρήσεις, αποτελέσματα και συμπεράσματα. | Academic integrity. | CONFIRMED | Citation audit and result provenance audit pass. |
| REQ-THESIS-005 | Figures και tables παράγονται αυτόματα από πραγματικά δεδομένα. | Ρητή απόφαση χρήστη. | CONFIRMED | Rebuild command reproduces thesis artifacts. |
| REQ-THESIS-006 | Απαιτούνται ελληνική περίληψη/λέξεις-κλειδιά και αγγλικό abstract/keywords σύμφωνα με την επαληθευμένη οδηγία του Τμήματος. | Επίσημη οδηγία Τμήματος. | CONFIRMED | Και οι δύο ενότητες εμφανίζονται στο τελικό document. |
| REQ-DELIV-001 | Το τελικό repository περιλαμβάνει code, configs, tests, literature, thesis material, raw/processed results, figures/tables/exports και reproduction scripts. | Ρητή απαίτηση χρήστη. | DEFERRED | Final repository checklist ολοκληρωμένο. |
