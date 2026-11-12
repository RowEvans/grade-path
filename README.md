# grade-path

A small desktop app that scrapes grades from St. Johns County's Home Access Center and displays them in a native Qt UI. A personal project, built because GradeWay stopped working.

## Features

- Log in once with your Home Access Center username and password
- Your password is stored in your operating system's credential store (via `keyring`), not in a file
- A refresh button pulls your latest grades in the background, so the UI never freezes
- Classes show as a scrollable list of color-coded cards (green, blue, orange, or red based on the grade)
- If your saved login stops working, the app sends you back to the login page

## How it works

1. **`login_page.py`**: the login screen and the "Logging in..." loading screen.
2. **`scraper.py`**: uses Playwright to log in to Home Access Center, reads each class's ID, period, name, and current average from the Classwork page, and saves it to a local SQLite database (`grades.db`). It also saves your username in the database and reads your password back from `keyring`.
3. **`main.py`**: the PySide6 (Qt for Python) app. It shows the login page on first launch, then the grades view once you are logged in. Logging in and scraping run on background threads.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

2. Run the app:

   ```bash
   python main.py
   ```

3. Enter your Home Access Center username and password on the login page. Your grades load right after you log in.

A prebuilt Windows version is also published on the [Releases](https://github.com/RowEvans/grade-path/releases) page.

## Usage

- Press the refresh button in the header to fetch your latest grades.
- Your login is remembered between launches. To use a different account, remove the saved `GradePath` entry from your system's credential manager.

## Project structure

```
.
├── assets/            # Icons and images (nav icons, refresh icon, loading gif, etc.)
├── login_page.py      # Login and loading screens
├── main.py            # App entry point and grades UI
├── scraper.py         # Playwright scraper, SQLite storage, saved-login handling
├── grades.db          # SQLite database of scraped grades
├── requirements.txt   # Python dependencies
└── .gitignore
```

## Tech stack

- Python
- PySide6 (Qt for Python)
- Playwright
- SQLite
- keyring
- platformdirs

## Notes

- The scraper is tailored to St. Johns County's Home Access Center HTML structure and may break if the district changes its site.
- Your credentials are only ever sent to Home Access Center.