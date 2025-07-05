Below is an end‑to‑end design that gives **(a)** a clearly defined *file‑system & markdown structure* and **(b)** a precise, repeatable *algorithm* an AI (or human) reviewer can follow for every source file.  Copy this verbatim into your repository as `REVIEW_GUIDE.md` and point each reviewer to it.

---

## 1. Repository layout for reviews

```
/code/                       ⟵ original source (read‑only for reviewers)
/reviews/                    ⟵ everything produced by reviews
│
├── _MASTER.md               ⟵ single source‑of‑truth progress ledger
├── _TAGS.yml                ⟵ shared vocab: severities, categories … (optional)
├── _DEPENDENCIES.yml        ⟵ graph of file‑to‑file relationships
│
├── modules/                 ⟵ mirrors /code/ directory tree 1‑for‑1
│   └── <module‑name>/       
│       ├── README.md        ⟵ module‑level synthesis (created last)
│       └── <file>.md        ⟵ one review file per real code file
│
└── system/
    ├── HOTSPOTS.md          ⟵ auto/hand‑curated list of cross‑cutting issues
    └── METRICS_SUMMARY.md   ⟵ repo‑wide score roll‑ups
```

### 1.1  `_MASTER.md`  (progress ledger)

A markdown table (one row per code file) tracked under version‑control.

| File Path         | Lang | LOC | Reviewed ? | Review Date | Reviewer | Security | Perf | Maint | Consistency | Best Pract. | Code Smell | Open Issues | Dep. Count |
| ----------------- | ---- | --- | ---------- | ----------- | -------- | -------- | ---- | ----- | ----------- | ----------- | ---------- | ----------- | ---------- |
| `src/api/user.js` | JS   | 428 | ✅          | 2025‑07‑05  | `AI‑A`   | 3        | 4    | 4     | 5           | 4           | 3          | 5           | 7          |

*Scores are 1‑5 (5 = excellent). “Open Issues” is a count of unresolved items in that file.*

### 1.2  Review file template  (`/reviews/modules/<module>/<file>.md`)

```markdown
---
file: src/api/user.js
language: JavaScript
loc: 428
reviewer: AI‑A
date: 2025‑07‑05
status: complete           # draft | complete | needs‑follow‑up
metrics:
  security:        {score: 3, open_issues: 2}
  performance:     {score: 4, open_issues: 1}
  maintainability: {score: 4, open_issues: 0}
  consistency:     {score: 5, open_issues: 0}
  best_practices:  {score: 4, open_issues: 1}
  code_smell:      {score: 3, open_issues: 1}
dependencies:
  - src/common/crypto.js         # imported by this file
  - src/models/userModel.js
reverse_dependencies: []         # to be auto‑populated later
---

# 1. Summary  
*Brief, high‑level statement of what the file does and overall health.*

# 2. Detailed findings  

| # | Category | Severity | Location | Description | Recommendation |
|---|----------|----------|----------|-------------|----------------|
| 1 | Security | **High** | L67‑82   | Unsanitised input in JWT decode | Validate & escape input or use vetted library … |
| 2 | Perf | **Med** | L120 | N+1 DB queries inside loop | Batch queries … |

# 3. Positive observations  
*E.g., good test coverage, clear naming …*

# 4. Context & links  
- Related ADRs: ADR‑12‑Auth‑Strategy  
- Unit tests: `tests/api/user.test.js`  
- Design docs: `/docs/auth.md`

# 5. Checklist (pass / fail)  
- [x] Lints clean  
- [ ] Threat model updated  
- [x] Logging at appropriate levels  

```

### 1.3  `_DEPENDENCIES.yml`

```yaml
src/api/user.js:
  outbound:
    - src/common/crypto.js
    - src/models/userModel.js
  inbound:        # filled by script after all files reviewed
    - src/server.js
```

### 1.4  `system/HOTSPOTS.md`

*Automatically or manually gather issues that involve **multiple files** (e.g., shared secret management, cross‑module circular deps).  Link to individual findings by `file#line`.*

---

## 2. End‑to‑end workflow

### Phase 0 – Setup (one‑time)

1. **Clone** the code repository into `/code`.
2. **Inventory** every code file (include language & LOC).
3. Generate skeletons:

   * `_MASTER.md` pre‑populated with one row per file (Reviewed ? = ❌).
   * Empty review markdown stub for each file under `/reviews/modules/...`.
   * Initial empty `_DEPENDENCIES.yml`.

*(A helper script can automate 2‑3.)*

### Phase 1 – Per‑file review loop

> **Input**: Path to *one* unreviewed file (`FILE`).
> **Output**: Updated review markdown, `_MASTER.md`, `_DEPENDENCIES.yml`.

| Step | Action                                                                                                                       | Notes                                                                                                  |
| ---- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 1    | *Lock file* in `_MASTER.md` (mark “🔒 in‑progress”).                                                                         | Prevent duplicate work.                                                                                |
| 2    | **Load context**: code of `FILE`, its tests, design docs, lint results.                                                      |                                                                                                        |
| 3    | **Static analysis** (security linters, complexity, style) & quick runtime probe if feasible.                                 | Retain artefacts in a `/reports/<file>/` folder if big.                                                |
| 4    | **Assess six categories** in order:<br>Security → Performance → Maintainability → Consistency → Best Practices → Code Smell. | For each:<br>• list specific findings with severity (High/Med/Low) and line refs;<br>• give 1‑5 score. |
| 5    | **Identify dependencies**:<br>• Imports / includes / external calls.<br>• Capture in `dependencies:` list.                   | Regex parse or language‑aware parser.                                                                  |
| 6    | **Populate review markdown** (use template §1.2).                                                                            | Replace placeholders, keep sections even if empty.                                                     |
| 7    | **Update `_MASTER.md`**:<br>• Reviewed ? = ✅.<br>• Fill scores & issue counts.<br>• Clear lock.                              | Keep row order constant for diff readability.                                                          |
| 8    | **Append to `_DEPENDENCIES.yml`** outbound links discovered.                                                                 | Merging if key already exists.                                                                         |
| 9    | **Commit** all changes (`git commit -m "Reviewed FILE"`).                                                                    | CI can run link‑checker on commit.                                                                     |

> *At this moment the file is **done** and can contribute to system‑level views.*

### Phase 2 – System‑level aggregation (runs periodically)

| Step | Action                                                                                                                      | Produced artefact         |
| ---- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| A    | Compute reverse dependencies using `_DEPENDENCIES.yml`; write them back in each file’s `reverse_dependencies` list.         | Updated review md files.  |
| B    | Re‑compute repo KPI scores (averages, std‑dev); write `system/METRICS_SUMMARY.md`.                                          | Overall health dashboard. |
| C    | Detect patterns: same issue ID in ≥ 2 files, circular dependencies, duplicated secrets, etc.  List in `system/HOTSPOTS.md`. | Cross‑cutting insights.   |

*(These can be scripted to run in CI on every review commit.)*

---

## 3. Precise algorithm for the reviewer AI (copy/paste into prompt)

> **ROLE**: *You are the File Reviewer AI.*
> **OBJECTIVE**: Analyse **exactly one** source file and populate its review markdown while updating the master ledger.
> **INPUTS**:
>
> * `FILE_PATH` – absolute path inside `/code/…`
> * `REPO_ROOT/reviews` – writable review workspace
> * `METRICS` – fixed list: `Security, Performance, Maintainability, Consistency, Best_Practices, Code_Smell`
>   **OUTPUTS** (all in markdown):
> * `/reviews/modules/.../<FILE_NAME>.md` – filled template
> * Updated row in `/reviews/_MASTER.md`
> * Added outbound deps in `/reviews/_DEPENDENCIES.yml`

### Algorithm

```
1. Open /reviews/_MASTER.md; mark FILE_PATH row “🔒 in‑progress”.
2. Read source code; detect language & LOC.
3. Run static tools:
     • Linter / formatter
     • Security scanner (e.g., Bandit, ESLint‑security)
     • Complexity metrics
4. For each METRIC in order:
     a. Scan code manually + tool results.
     b. Record findings (line numbers, description, recommendation, severity).
     c. Assign 1‑5 score & count open issues.
5. Parse imports / includes; list unique outbound dependencies.
6. Fill review markdown template sections (#1–#5).
7. Re‑open /reviews/_MASTER.md; overwrite row:
     Reviewed? ✅, Review_Date=TODAY, Reviewer=AI‑ID,
     fill metric scores & issue counts, Dep.Count = len(outbound deps).
8. Update /reviews/_DEPENDENCIES.yml:
     Append/merge:
       FILE_PATH:
         outbound: [deps…]
9. Save all files. Remove “🔒”.
10. End with message: “Review of FILE_PATH complete.”  (No extra commentary.)
```

---

## 4. Scoring rubric (1–5)

| Score | Description                                      |
| ----- | ------------------------------------------------ |
| 5     | Exemplary – no actionable findings.              |
| 4     | Minor nits only; no medium/high severity issues. |
| 3     | At least one medium severity or several lows.    |
| 2     | High severity issue(s) but fixable locally.      |
| 1     | Critical flaws; rewrite advised.                 |

*(Same rubric applied for every metric.)*

---

## 5. Naming & cross‑reference conventions

* **Issue IDs**: `FILE:ISSUE#:CATEGORY` (e.g., `src/api/user.js:1:Security`) – unique in repo.
* **Module README** files created **after** all contained files are reviewed, summarising patterns & open items.
* **Linking**: Use relative paths so browsing on GitHub renders correctly.

---

### Why this works

* **Deterministic**: Every action & file path is spelled out.
* **Composable**: Per‑file reviews are stand‑alone yet machine‑mergeable for system views.
* **Low‑friction tooling**: Pure Markdown/YAML; no DB required.
* **CI‑friendly**: Scripts can validate schema, render dashboards, and fail builds on high‑severity issues.

Hand this guide to any reviewing engine (AI or human) and it will know **exactly** where to write, what to fill, and how to keep the overall review corpus coherent and inspectable.
