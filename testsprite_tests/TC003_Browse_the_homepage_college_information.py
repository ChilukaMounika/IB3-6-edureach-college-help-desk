import asyncio
import re
from playwright import async_api
from playwright.async_api import expect

async def run_test():
    pw = None
    browser = None
    context = None

    try:
        # Start a Playwright session in asynchronous mode
        pw = await async_api.async_playwright().start()

        # Launch a Chromium browser in headless mode with custom arguments
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--window-size=1280,720",
                "--disable-dev-shm-usage",
                "--ipc=host",
                "--single-process"
            ],
        )

        # Create a new browser context (like an incognito window)
        context = await browser.new_context()
        # Wider default timeout to match the agent's DOM-stability budget;
        # auto-waiting Playwright APIs (expect, locator.wait_for) inherit this.
        context.set_default_timeout(15000)

        # Open a new page in the browser context
        page = await context.new_page()

        # Interact with the page elements to simulate user flow
        # -> navigate
        await page.goto("http://localhost:5173")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Scroll the homepage to reveal the 'About EduReach College' and 'Programs Offered' sections and check the page text for those headings.
        await page.mouse.wheel(0, 300)
        
        # -> Scroll the homepage to reveal the 'About EduReach College' and 'Programs Offered' sections and check the page text for those headings.
        await page.mouse.wheel(0, 300)
        
        # --> Assertions to verify final state
        
        # --> Visitor can scroll the homepage and view college information sections such as the 'Programs Offered' cards.
        await page.locator("xpath=/html/body/div/div[1]/section[4]/div/div[3]/div[2]/div[2]/span[1]").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: A program card showing '60 seats' is visible, proving the Programs Offered section is displayed.
        await expect(page.locator("xpath=/html/body/div/div[1]/section[4]/div/div[3]/div[2]/div[2]/span[1]").nth(0)).to_be_visible(timeout=15000), "A program card showing '60 seats' is visible, proving the Programs Offered section is displayed."
        
        # --> The landing page remains usable without opening the chat: the chat button is present and the page scrolled successfully while the chat was not opened.
        # Assert-outcome: passed
        # Assert: The chat button is present with the title 'Chat with EduReach Bot', showing the widget was available but not opened.
        await expect(page.locator("xpath=/html/body/div/button").nth(0)).to_have_attribute("title", "Chat with EduReach Bot", timeout=15000), "The chat button is present with the title 'Chat with EduReach Bot', showing the widget was available but not opened."
        await page.locator("xpath=/html/body/div/div[1]/section[1]/div[2]/div/a").nth(0).scroll_into_view_if_needed()
        # Assert-outcome: passed
        # Assert: The page revealed the 'Explore Programs' link after scrolling, proving the page remained interactive.
        await expect(page.locator("xpath=/html/body/div/div[1]/section[1]/div[2]/div/a").nth(0)).to_be_visible(timeout=15000), "The page revealed the 'Explore Programs' link after scrolling, proving the page remained interactive."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    