# Heritage DB
> Semester marks at a glance — a lightweight Flask site with Selenium-sourced, CSV-backed grade data (plus an internal Flask API).

Heritage DB is a personal (non-official) hobby project that aggregates publicly viewable semester marks for students of Heritage Institute of Technology. Data is scraped (Firefox + Selenium) and exposed through:
- A Flask web interface for browsing.
- A minimal INTERNAL API (not guaranteed stable; intended for templates / internal tooling, not public consumption).

> DISCLAIMER: This is NOT an official HIT resource. Data is provided as-is for personal / educational exploration. If you believe any data should not be published, please open an issue.

---

## Status
Personal / experimental project. Manually updated per semester/batch.

## Key Points
- 🧪 Hobby project (not accepting external contributions)
- 🐍 Python 3.12 (expected to work on ≥3.8)
- 🌐 Flask web UI + internal API endpoints
- 🦊 Selenium (Firefox / geckodriver) for scraping
- 📁 One directory per batch: `data/<batch>/final.csv` (e.g. `data/2022/final.csv`)
- 🔒 Public portal only (no credentialed access)
- 📊 Future: analytics & student-oriented insights

## Tech Stack
| Aspect    | Choice                       |
|-----------|------------------------------|
| Language  | Python 3.12 (≥3.8 compatible)|
| Web       | Flask                        |
| Scraping  | Selenium (Firefox)           |
| Storage   | CSV (per batch directory)    |
| Config    | Simple Python modules        |

## Repository Structure
```
.
├─ app.py                # Flask entrypoint (run with `python app.py`)
├─ config.py             # Configuration / constants
├─ debug_csv.py          # Helper / debugging for CSV inspection
├─ requirements.txt      # Python dependencies
├─ favicon.ico
├─ src/                  # Selenium scraping scripts / helpers
├─ data/                 # Batch folders (e.g. 2022/, 2023/, each with final.csv)
│  └─ <batch>/final.csv  # Canonical dataset per batch
├─ models/               # Data model helpers / abstractions (if any)
├─ services/             # Service-layer logic (API/data access utilities)
├─ utils/                # General utility functions
├─ templates/            # Jinja2 templates for HTML pages
├─ static/               # CSS / JS / assets
└─ README.md
```

### Data Layout
Batch-oriented storage:
```
data/
  2022/
    final.csv
  2023/
    final.csv
  ...
```
Each `final.csv` is the current canonical snapshot for that batch.

### Example Row (illustrative)
```csv
roll,name,semester,subject_code,subject_name,grade
IT22001,Jane Doe,5,CS302,Algorithms,B+
```
(Real columns may differ or expand.)

---

## Internal API
A lightweight set of Flask routes (e.g. `/api/...`) is present for internal template consumption or experimentation.

Characteristics:
- Not versioned.
- Response formats may change without notice.
- Intended for in-app usage (AJAX, charts, or future analytics).
- No authentication layer (because underlying data is already public).

If you rely on it externally, you accept breakage risk.  
(Inspect `app.py`, `services/`, or `models/` for current endpoints.)

---

## Running Locally

### Prerequisites
- Python 3.12 (works on ≥3.8)
- Firefox installed
- `geckodriver` on PATH  
  - macOS: `brew install geckodriver`  
  - Linux: download from Mozilla or use distro packages  
  - Verify: `geckodriver --version`

### Installation
```bash
git clone https://github.com/shirsakm/heritage-db.git
cd heritage-db
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
App URL: http://127.0.0.1:5000 (port fixed)

### Scraping Workflow
Currently manual / maintainer-driven:
1. Use scripts in `src/` to fetch public semester results.
2. Normalize / merge into `data/<batch>/final.csv`.
3. Commit updated CSV.

No single “all batches” command yet; internal tooling may evolve.

---

## No Public Stable API
While internal endpoints exist, there is no formally supported public API. For data needs, read the CSV files directly.

---

## Roadmap (Aspirational)
- [ ] Lightweight batch regeneration tooling
- [ ] Search & filter (roll, subject, semester)
- [ ] Basic aggregate statistics (averages, distributions)
- [ ] Trend analysis per student
- [ ] Optional JSON export (read-only)
- [ ] Analytics dashboards (charts / grade curves)

## Future Ideas
- Difficulty / variance metrics per subject
- Grade distribution heatmaps
- CLI: validate / diff between semester snapshots

---

## Privacy / Ethics
- Uses only publicly accessible academic result data.
- No credential-based scraping.
- Open an issue for concerns, redactions, or takedown requests.
- If policies change, approach will be reevaluated.

---

## Contribution Policy
Not accepting pull requests.  
If you find an issue or have a question, please open an issue for discussion.

Suggested issue template (informal):
```
Title: <concise summary>
Details: what you observed / expected
Scope: batch / file / route (if relevant)
```

---

## Badges (Enable After MIT License Added)
```
![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Last Commit](https://img.shields.io/github/last-commit/shirsakm/heritage-db)
```

---

## License
Licensed under the MIT License (see [LICENSE](LICENSE)).

```
MIT License © 2025 Shirsak Majumder
```

---

## Maintainer
Shirsak Majumder ([@shirsakm](https://github.com/shirsakm))

---

## Known Limitations
- Manual data ingestion process
- No pagination or large-file optimization yet
- Internal API unstable for third-party use
- Dependent on upstream portal structure (scraper breakage risk)

---

## Quick TL;DR
```bash
git clone https://github.com/shirsakm/heritage-db
cd heritage-db
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
# Data in data/<batch>/final.csv
```