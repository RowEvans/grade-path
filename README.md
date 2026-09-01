# grade-path

A small desktop app that scrapes grades from St. Johns County's Home Access Center and displays them in a native Qt UI, as a personal project due to the end of GradeWay.

## How it works

1. **`scraper.py`** — logs into Home Access Center with Playwright, scrapes each class's name, period, and current average from the Classwork page, and saves it into a local SQLite database (`grades.db`).
2. **`main.py`** — a PySide6 (Qt for Python) desktop app that reads `grades.db` and displays your classes in a scrollable, color-coded card list (green/blue/orange/red badges based on grade thresholds), with a header and bottom nav bar.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

2. Create a `.env` file in the project root with your Home Access Center credentials:
   ```
   HAC_USERNAME=your_username
   HAC_PASSWORD=your_password
   ```

## Usage

**Scrape your latest grades:**
```bash
python3 scraper.py
```
This logs into Home Access Center, pulls your current grades, and writes/updates them in `grades.db`.

**View your grades:**
```bash
python3 main.py
```
Opens the desktop app showing your classes and grades.

## Project structure

```
.
├── main.py           # PySide6 desktop UI for viewing grades
├── player.py         # Playwright scraper that populates grades.db
├── grades.db          # SQLite database of scraped grades
├── requirements.txt   # Python dependencies
└── .gitignore
```

## Notes

- `grades.db` and `.env` hold personal data/credentials — keep `.env` out of version control (already in `.gitignore`).
- The scraper is tailored to St. Johns County's Home Access Center HTML structure and may break if the district changes its site.