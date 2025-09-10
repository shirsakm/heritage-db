# Heritage DB

![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-green.svg) ![Last Commit](https://img.shields.io/github/last-commit/shirsakm/heritage-db)

An unofficial, user-friendly interface for viewing semester results at the Heritage Institute of Technology.

### **[✨ View the Live Demo ✨](https://shirsak.ftp.sh/)**

<img width="1366" height="736" alt="Heritage DB Home Page" src="https://github.com/user-attachments/assets/bcbb5f4f-7c1f-40b7-85e8-c77c0973a0ad" />

_The main page for selecting a batch._

<img width="1366" height="645" alt="Results View" src="https://github.com/user-attachments/assets/e716ac19-411a-4347-814f-81a635dc5816" />

_Clean, searchable, and filterable results for a selected batch._

## About The Project

Heritage DB is a web application that scrapes, aggregates, and presents publicly available semester results for students of the Heritage Institute of Technology. The goal is to provide a fast, clean, and user-friendly interface to view and search through grade data without the clutter of the official portal.

Data is sourced using **Selenium** to handle the JavaScript-rendered official website and is stored locally in **CSV** files. The front-end is a lightweight **Flask** application that serves the data through a simple web UI and an internal API.

### Motivation

I began this project out of personal curiosity and as a challenge to practice and showcase my skills in:
* **Web Scraping:** Using Selenium to automate browser interactions and extract data from a dynamic website.
* **Backend Development:** Building a web application and API with the lightweight Flask framework.
* **Data Handling:** Processing and structuring scraped data into a clean, usable format (CSV).
* **Full-Stack Integration:** Connecting a Python backend to a simple, effective front-end.

## Key Features

-   🌐 **Simple Web Interface:** A clean, responsive UI for browsing results by batch.
-   🔍 **Search & Filter:** Instantly search for students or filter results.
-   📊 **Ranked Results:** View students ranked by their SGPA and YGPA.
-   🐍 **Python Backend:** A robust Flask server powers the application.
-   🦊 **Selenium Scraping:** Automated data ingestion from the public results portal.
-   📁 **CSV Data Storage:** Simple, transparent, and portable data backend.

## Tech Stack

| Aspect   | Choice                        |
|----------|-------------------------------|
| Language | Python 3.12 (>=3.8 compatible)  |
| Web      | Flask                         |
| Scraping | Selenium (Firefox)            |
| Storage  | CSV                           |
| Config   | Simple Python modules         |

## Running Locally

### Prerequisites

* Python 3.12+ (expected to work on ≥3.8)
* Firefox browser installed
* `geckodriver` available on your system's PATH
    * **macOS:** `brew install geckodriver`
    * **Linux:** Download from Mozilla or use your distribution's package manager.
    * Verify with: `geckodriver --version`

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/shirsakm/heritage-db.git
    cd heritage-db
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    python app.py
    ```
The application will be available at `http://127.0.0.1:5000`.

## Repository Structure

```
.
├─ app.py             # Flask entrypoint
├─ config.py          # Configuration / constants
├─ requirements.txt   # Python dependencies
├─ src/               # Selenium scraping scripts / helpers
├─ data/              # Batch folders (e.g. 2022/, 2023/)
│  └─ <batch>/final.csv # Canonical dataset per batch
├─ models/            # Data model helpers / abstractions
├─ services/          # Service-layer logic (API/data access)
├─ utils/             # General utility functions
├─ templates/         # Jinja2 templates for HTML pages
└─ static/            # CSS / JS / other assets
```

## Data & API Notes

### Data Storage
The canonical data for each academic batch is stored in a `final.csv` file within its respective directory (e.g., `data/2024/final.csv`). For any data analysis or external use, reading these CSV files directly is the recommended approach.

### Internal API
The project includes a minimal internal API (e.g., routes under `/api/...`) that the front-end uses to fetch data dynamically.

**Please note:** This API is **unstable and not versioned**. It is intended solely for internal consumption. Response formats and endpoints may change without notice. Relying on it for third-party applications is not recommended.

## Roadmap (Aspirational)

- [ ] Lightweight batch regeneration tooling
- [ ] Basic aggregate statistics (averages, distributions)
- [ ] Trend analysis per student
- [ ] Optional JSON export (read-only)
- [ ] Analytics dashboards (charts / grade curves)

## Contribution Policy
This is a personal project, so I am not accepting pull requests at this time. However, if you find an issue or have a suggestion, please feel free to **[open an issue](https://github.com/shirsakm/heritage-db/issues)** for discussion.

## Privacy / Ethics
- This tool only uses publicly accessible academic result data. No private credentials are used or stored.
- If you have any concerns about the data, please open an issue for redactions or takedown requests.
- The project's approach will be re-evaluated if the source portal's policies change.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

```
MIT License © 2025 Shirsak Majumder
```

## Maintainer
Shirsak Majumder ([@shirsakm](https://github.com/shirsakm))
