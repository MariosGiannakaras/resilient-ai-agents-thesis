# Execution and Review Workflow

## Purpose

Keep the thesis process simple, controlled and largely automatic. The user sets goals and provides real-world feedback; technical GitHub work is handled by Codex, automated checks and ChatGPT review.

## Roles

### User

- Defines the desired outcome and reports what is observed in the running system.
- Provides supervisor instructions, deadlines and non-public source material when needed.
- Does not need to approve branches, commit names, tests, pull requests or merges.
- Is consulted only for genuinely academic, product or personal choices that cannot be resolved objectively from evidence.

### ChatGPT reviewer/orchestrator

- Converts the agreed goal into a bounded task.
- Reviews research quality, repository changes, naming, comments, tests, experiment evidence and results.
- Decides whether technical changes are ready, need correction or should be rejected.
- Handles GitHub review and merge decisions without transferring routine Git work to the user.
- Stops and asks the user only when a decision changes thesis direction, scope or supervisor-facing content.

### Codex executor

- Performs only the assigned bounded task.
- Creates the branch, implementation, tests, documentation, commits and Pull Request.
- Uses clear names and explains what changed, why it changed and how it was validated.
- Does not self-approve, silently broaden scope, change a frozen protocol or treat its own output as final evidence.

### GitHub automation

- Runs repeatable checks on every relevant Pull Request.
- Executes tests, static checks, schema/config validation and reproducibility checks appropriate to the current stack.
- Stores the review history and blocks merge when required checks fail.
- Expands only when the implementation stack is selected; no production CI platform is required.

## Normal flow

1. Discuss and agree on one practical outcome.
2. ChatGPT performs the necessary analysis and prepares a bounded task.
3. Codex works on a dedicated branch and opens a Pull Request.
4. GitHub runs automated checks and Codex review.
5. ChatGPT inspects the diff, evidence and review comments.
6. Codex or ChatGPT addresses defects; checks run again.
7. ChatGPT merges when the technical and scientific checks are satisfactory.
8. The user receives a brief report of what changed, what was verified and what happens next.

The user is not asked to perform routine GitHub approval or merge work.

## Bibliography upload flow

When the user supplies a batch of PDFs, Markdown exports, NotebookLM source lists or related thesis material, treat it immediately as one bounded source-intake task without asking for a separate routine GitHub approval.

ChatGPT/Codex must:

1. inspect the real content rather than trust filenames,
2. resolve canonical metadata and source versions,
3. detect duplicates and contradictory records,
4. rename and classify files using `bibliography/README.md`,
5. preserve original PDFs and complete Markdown separately,
6. create structured notes and useful thematic excerpts,
7. identify missing coverage such as unsupported models, metrics or uncertainty types,
8. update source provenance, evidence matrices and relevant documentation,
9. run checks and merge after review.

The user is contacted only when lawful acquisition, private access, an unreadable file or a genuine research-direction choice requires input.

## Git conventions

### Branches

Use one clear prefix:

- `research/` for literature, candidate evaluation and experiment design,
- `feat/` for functionality,
- `fix/` for defects,
- `test/` for test-only work,
- `docs/` for documentation,
- `chore/` for bounded repository maintenance.

Branch names use lowercase kebab-case and describe one outcome.

### Commits

Prefer small logical commits with a conventional title such as `feat:`, `fix:`, `test:`, `docs:` or `research:`. The body records:

- **What:** concrete changes,
- **Why:** reason and affected requirement,
- **Validation:** tests, checks or evidence,
- **Not changed:** important exclusions when ambiguity is possible.

### Pull Requests

Every substantial PR states:

- goal and scope,
- what changed and why,
- validation and CI status,
- scientific/protocol impact,
- screenshots or artifacts where relevant,
- risks, limitations and deferred work.

## Naming and comments

- Names must be stable, descriptive and consistent with the selected language/framework conventions.
- Avoid temporary names such as `test2`, `final_new`, `model_best` or unexplained abbreviations.
- Experiment/run naming is defined by the approved schema and must expose run type, configuration identity and version without relying on folder order.
- Comments explain non-obvious reasoning, scientific constraints, invariants or workarounds. They must not merely restate the code.
- Public interfaces, configs, metrics and non-trivial scripts receive concise documentation.

## Review and merge gates

A change is merged only when applicable conditions are satisfied:

- scope matches the assigned task,
- names and structure are coherent,
- relevant tests exist and pass,
- automated review findings are addressed or explicitly rejected with reason,
- documentation and changelog/decision files are updated when needed,
- no fabricated data, logs, results or progress exist,
- experiment/protocol changes are explicit and traceable,
- generated artifacts point to real inputs and code.

Passing tests alone is not approval; the tests themselves are reviewed for meaningful coverage.

## Practical thesis workflow

The project follows a simple sequence:

1. Find and evaluate related research, algorithms, repositories and theses.
2. Build a small working research core and an early visual/debug UI.
3. Add only useful settings, logs, charts, history, comparison and exports.
4. Validate the system, run pilots, freeze the final protocol and execute final experiments.
5. Collect results, screenshots, figures, tables, videos and structured notes while work is performed.
6. Write the thesis from verified bibliography and frozen evidence.
7. Create the PowerPoint, slide visuals, key points and presentation script from the same approved evidence.

Each phase should leave behind usable code, documentation, writing notes and possible presentation material so the final writing and slides are not a separate last-minute project.
