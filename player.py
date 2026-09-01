from playwright.sync_api import sync_playwright
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("HAC_USERNAME")
password = os.getenv("HAC_PASSWORD")

DB_FILE = os.path.join(os.path.dirname(__file__), "grades.db")

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
    con.commit()
    con.close()

def scraper():
    con = sqlite3.connect(DB_FILE)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto("https://homeaccesscenter.stjohns.k12.fl.us/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess")
        page.fill("#LogOnDetails_UserName", username)
        page.fill("#LogOnDetails_Password", password)
        page.click("#login")

        page.goto("https://homeaccesscenter.stjohns.k12.fl.us/HomeAccess/Classes/Classwork")

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
                class_id, class_name, period = pending
                cur = con.cursor()
                cur.execute("""
                    INSERT OR IGNORE INTO grades (class_id, name, period, grade)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(class_id) DO UPDATE SET
                        grade = excluded.grade
                """, (class_id, period, class_name, grade))
                con.commit()
                pending = None
            else:
                class_id, class_name, period = pending
                cur = con.cursor()
                cur.execute("INSERT OR IGNORE INTO grades VALUES (?, ?, ?, 0.0)", (class_id, period, class_name))
                con.commit()
                pending = None

        browser.close()

if __name__ == "__main__":
    _init_db()

    scraper()