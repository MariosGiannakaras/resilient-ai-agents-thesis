# Project Context

## Status taxonomy

- **CONFIRMED:** προκύπτει από επίσημη αίτηση ή ρητή νεότερη απόφαση χρήστη.
- **HISTORICAL:** εμφανίστηκε σε παλιές συνομιλίες αλλά δεν αποτελεί τρέχουσα δέσμευση.
- **PROPOSED:** υποψήφια επιλογή προς έρευνα και απόφαση.
- **OPEN:** λείπει κρίσιμη πληροφορία ή απόφαση.
- **UNVERIFIED:** έχει αναφερθεί αλλά δεν έχει ελεγχθεί στην πρωτογενή πηγή ή στον κώδικα.

## Τι είναι το project

Το project είναι η πλήρης ερευνητική, πειραματική, τεχνική και συγγραφική υποδομή της διπλωματικής εργασίας:

> **Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα**

Ακαδημαϊκό πλαίσιο — **CONFIRMED**:

- Πανεπιστήμιο Δυτικής Αττικής.
- Σχολή Μηχανικών.
- Τμήμα Μηχανικών Πληροφορικής και Υπολογιστών.
- Προπτυχιακή διπλωματική εργασία του Τμήματος, όπως καταγράφεται στην επίσημη αίτηση. Η ακριβής διοικητική ονομασία του προγράμματος/κύκλου σπουδών θα επαληθευτεί από τα ισχύοντα στοιχεία του Τμήματος.
- Συγγραφή στα ελληνικά και τελικό παραδοτέο Microsoft Word.

Το όνομα του επιβλέποντα, οι ειδικές απαιτήσεις του και η προθεσμία παραμένουν **OPEN**.

## Επίσημος ακαδημαϊκός σκοπός

Η επίσημη αίτηση ορίζει ως σκοπό τη μελέτη και συγκριτική αξιολόγηση ανθεκτικών πρακτόρων AI σε περιβάλλοντα αβεβαιότητας και δυναμικών μεταβολών. Μέσω απλού προσομοιωμένου περιβάλλοντος πρέπει να συγκριθούν αλγόριθμοι λήψης αποφάσεων ως προς την ικανότητά τους να προσαρμόζονται σε απρόβλεπτες αλλαγές, όπως:

- θόρυβος δεδομένων,
- μεταβολή κανόνων,
- αποτυχίες εκτέλεσης ενεργειών.

Η αξιολόγηση πρέπει να εξετάζει την ανθεκτικότητα και την ταχύτητα ανάκαμψης.

## Ρόλος του GridWorld

Το GridWorld είναι το ελεγχόμενο προσομοιωμένο περιβάλλον στο οποίο:

- ορίζονται σαφείς καταστάσεις, ενέργειες, στόχος, εμπόδια, ανταμοιβές και τερματισμοί,
- εισάγονται μετρήσιμες μορφές αβεβαιότητας ή αλλαγές,
- εκτελούνται επαναλήψιμα πειράματα,
- απομονώνεται η επίδραση κάθε disturbance factor,
- παράγονται traces, metrics και artifacts.

Η τελική προδιαγραφή δεν έχει οριστικοποιηθεί. Οι παλιές συνομιλίες περιέχουν διαφορετικές εκδοχές, οι οποίες καταγράφονται ως candidates στο `docs/research/GRIDWORLD_SPEC.md`, όχι ως επιβεβαιωμένοι κανόνες.

## Ρόλος των μοντέλων

Τα μοντέλα/αλγόριθμοι είναι οι συγκρινόμενοι πράκτορες ή baselines. Δεν υπάρχει τελική επιβεβαιωμένη λίστα. Ιστορικά αναφέρθηκαν:

- random και deterministic/planning baselines,
- tabular RL όπως Q-learning και SARSA,
- Dyna-style ή model-based planning,
- MCTS,
- PPO και memory-enabled agents,
- world-model approaches,
- oracle/full-state upper bounds,
- ReAct/LLM-based agents.

Η τελική επιλογή πρέπει να προκύψει από το επίσημο θέμα, την πραγματική βιβλιογραφία, την τελική προδιαγραφή περιβάλλοντος, pilot experiments και το πραγματικό hardware.

## Ρόλος των experiments

Τα experiments είναι το κύριο μέσο παραγωγής επιστημονικών ευρημάτων. Πρέπει να:

- χρησιμοποιούν προκαθορισμένο protocol,
- περιλαμβάνουν πολλαπλά seeds/repetitions,
- διαχωρίζουν pilot, exploratory και final runs,
- αποθηκεύουν πλήρες run provenance,
- καταγράφουν failures/cancellations/exclusions,
- επιτρέπουν δίκαιη στατιστική σύγκριση,
- παράγουν πραγματικά figures και tables.

Τα ιστορικά hard-coded budgets ή seed counts δεν είναι επιβεβαιωμένα.

## Ρόλος του dashboard

Το dashboard είναι υποστηρικτικό εργαλείο για έναν τοπικό χρήστη. Πρέπει να μειώνει την ανάγκη χειροκίνητων scripts/console commands και να προσφέρει:

- διαμόρφωση και εκκίνηση runs,
- παρακολούθηση πραγματικού status/progress/logs/metrics,
- live οπτικοποίηση GridWorld όπου είναι χρήσιμη,
- run history, comparison και results exploration,
- εξαγωγή figures/tables/data,
- screenshots για παρουσίαση και διπλωματική.

Δεν είναι το κύριο ερευνητικό contribution και δεν προηγείται του core.

## Ρόλος της συγγραφής

Η συγγραφή εξελίσσεται παράλληλα με την υλοποίηση, αλλά κάθε κεφάλαιο διαχωρίζει:

- verified facts και citations,
- proposed methodology,
- finalized protocol,
- πραγματικά αποτελέσματα,
- interpretation και limitations.

Τα τελικά συμπεράσματα γράφονται μόνο από το frozen final result set.

## Σύνδεση εφαρμογής, αποτελεσμάτων και κειμένου

```text
Official topic + literature
          ↓
Research questions / hypotheses
          ↓
GridWorld + model + metric specification
          ↓
Versioned experiment protocol
          ↓
Independent core + validated runs
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

- Πραγματική βιβλιογραφία.
- Ακριβές existing GridWorld repository/path και αξιολόγηση κώδικα.
- Επιβεβαιωμένο hardware/software inventory.
- Επιβλέπων και ειδικές ακαδημαϊκές οδηγίες.
- Τελικές research questions/hypotheses.
- Final environment variants, models, metrics και statistical protocol.
- Τρέχον επίσημο Word template/submission package.
