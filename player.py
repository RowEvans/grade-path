from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://homeaccesscenter.stjohns.k12.fl.us/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess")
    page.fill("#LogOnDetails_UserName", "s576094")
    page.fill("#LogOnDetails_Password", "8dean2more!")
    page.click("#login")

    page.goto("https://homeaccesscenter.stjohns.k12.fl.us/HomeAccess/Classes/Classwork")

    frame = page.frame_locator("#sg-legacy-iframe")
    els = frame.locator(".sg-header-heading.sg-right")

    count = els.count()
    for i in range(count):
        print(els.nth(i).inner_text())

    browser.close()