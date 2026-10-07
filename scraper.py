from playwright.sync_api import sync_playwright
import sqlite3
from platformdirs import user_data_dir
import os
import keyring

APP_DIR = user_data_dir("GradePath", "yourname")
os.makedirs(APP_DIR, exist_ok=True)
DB_FILE = os.path.join(APP_DIR, "grades.db")

class LoginFailedError(Exception):
    pass

def _init_db():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS grades(
        class_id INTEGER PRIMARY KEY, 
        name TEXT, 
        period INTEGER, 
        grade REAL)
    """)

    cur.execute("CREATE TABLE IF NOT EXISTS accounts(username TEXT PRIMARY KEY)")
    con.commit()
    con.close()

def save_account(username):
    con = sqlite3.connect(DB_FILE)
    con.execute("INSERT OR REPLACE INTO accounts(username) VALUES (?)", (username,))
    con.commit()
    con.close()


def login(page, username, password): # page after login https://homeaccesscenter.stjohns.k12.fl.us/HomeAccess/Home/WeekView
    page.fill("#LogOnDetails_UserName", username)
    page.fill("#LogOnDetails_Password", password)
    page.click("#login")
    if page.url != "https://homeaccesscenter.stjohns.k12.fl.us/HomeAccess/Home/WeekView":
        raise LoginFailedError("Invalid Login")

    
def scrape(page, con):
    frame = page.frame_locator("#sg-legacy-iframe")
    els = frame.locator(".sg-header-heading")

    count = els.count()

    pending = None

    for i in range(count):
        text = els.nth(i).inner_text()

        if " - " in text:
            class_id_text, rest = text.split(" - ", 1)
            period_text, class_name = rest.split(" ", 1)
            class_id = float(class_id_text)
            period = float(period_text)
            pending = (class_id, period, class_name)

        elif "Average" in text and pending:
            grade = float(text.split()[1])
            class_id, period, class_name = pending
            cur = con.cursor()
            cur.execute("""
                INSERT OR IGNORE INTO grades (class_id, name, period, grade)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(class_id) DO UPDATE SET
                    grade = excluded.grade
            """, (class_id, class_name, period, grade))
            con.commit()
            pending = None
        else:
            class_id, period, class_name = pending
            cur = con.cursor()
            cur.execute("INSERT OR IGNORE INTO grades VALUES (?, ?, ?, 0.0)", (class_id, class_name, period))
            con.commit()
            pending = None

def verify_login(username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            login(page, username, password)

        finally:
            browser.close()

def login_and_scrape(username, password):
    _init_db()
    con = sqlite3.connect(DB_FILE)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://homeaccesscenter.stjohns.k12.fl.us/HomeAccess/Account/LogOn")

        try:
            login(page, username, password)
            page.goto("https://homeaccesscenter.stjohns.k12.fl.us/HomeAccess/Classes/Classwork")
            scrape(page, con)

        finally:
            browser.close()

def get_saved_login():
    con = sqlite3.connect(DB_FILE)
    try: 
        row = con.execute("SELECT username FROM accounts LIMIT 1").fetchone()
        if row is None:
            return None

        user = row[0]
        pw = keyring.get_password("GradePath", user)
        if pw is None:
            con.execute("DELETE FROM accounts WHERE username = ?", (user,))
            con.commit()
            return None

        return user, pw
    finally:
        con.close()