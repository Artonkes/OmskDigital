import pytest
from playwright.sync_api import sync_playwright

def SearchCollege():
    try:
        with sync_playwright() as s:
            browser = s.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            page = context.new_page()
            page.goto(url="https://omsk.postupi.online/specialnost-spo/09.02.07/ssuzy/")

            college = page.query_selector_all(".list-cover")
            for i in college:
                pass

    except None:
        pass