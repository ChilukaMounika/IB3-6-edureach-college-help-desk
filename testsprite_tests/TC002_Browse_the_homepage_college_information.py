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
        
        # -> Scroll through the homepage to view college information sections from top to bottom and confirm the "About EduReach College" section is present.
        await page.mouse.wheel(0, 300)
        
        # -> Scroll to the bottom of the homepage and confirm the 'Programs Offered' section and the introductory 'About EduReach College' text are visible.
        await page.mouse.wheel(0, 300)
        
        # -> Open the EduReach College homepage in a new tab and wait for it to finish loading so the page content can be rechecked.
        # Open URL in new tab
        page = await context.new_page()
        await page.goto("http://localhost:5173/")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Switch to the tab that displays the EduReach College homepage so the page content can be rechecked and scrolling resumed.
        # Switch to tab 5525
        page = context.pages[-1]  # switch to most recently active tab
        
        # -> Scroll the EduReach College homepage down through the content and verify that the 'Programs Offered' and 'About EduReach College' sections are visible.
        await page.mouse.wheel(0, 300)
        
        # --> Assertions to verify final state
        
        # --> Verify the college information sections are displayed
        await page.locator("xpath=/html/body/div/nav/div/div[1]/a[2]").nth(0).scroll_into_view_if_needed()
        # Assert: The 'About' navigation link is visible, indicating college information is reachable.
        await expect(page.locator("xpath=/html/body/div/nav/div/div[1]/a[2]").nth(0)).to_be_visible(timeout=15000), "The 'About' navigation link is visible, indicating college information is reachable."
        # Assert: The Programs section displays the ₹7.2 LPA package value.
        await expect(page.locator("xpath=/html/body/div/div[1]/section[4]/div/div[2]/div[2]/div/div/div/span[2]").nth(0)).to_have_text("\u20b97.2 LPA", timeout=15000), "The Programs section displays the \u20b97.2 LPA package value."
        # Assert: The Programs section displays the ₹8.8 LPA package value.
        await expect(page.locator("xpath=/html/body/div/div[1]/section[4]/div/div[2]/div[4]/div/div/div/span[2]").nth(0)).to_have_text("\u20b98.8 LPA", timeout=15000), "The Programs section displays the \u20b98.8 LPA package value."
        # Assert: A program entry shows '60 seats', confirming the Programs Offered content is visible.
        await expect(page.locator("xpath=/html/body/div/div[1]/section[4]/div/div[3]/div[2]/div[2]/span[1]").nth(0)).to_have_text("60\n seats", timeout=15000), "A program entry shows '60 seats', confirming the Programs Offered content is visible."
        current_url = await page.evaluate("() => window.location.href")
        # Assert: page loaded with a URL (final outcome verified by the AI judge during the run)
        assert current_url, 'Page should have loaded with a URL'
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    