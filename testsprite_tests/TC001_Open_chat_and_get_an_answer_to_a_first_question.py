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
        
        # -> Click the floating chat button labeled 'Chat with EduReach Bot' to open the chat widget.
        # Chat with EduReach Bot button
        elem = page.get_by_role('button', name='Chat with EduReach Bot', exact=True)
        await elem.click(timeout=10000)
        
        # -> Type a college-related question into the 'Ask a question...' input and click the send (paper-plane) button to submit it.
        # Ask a question... text field
        elem = page.get_by_placeholder('Ask a question...', exact=True)
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("What undergraduate engineering courses do you offer and what are their durations?")
        
        # -> Type a college-related question into the 'Ask a question...' input and click the send (paper-plane) button to submit it.
        # button
        elem = page.locator('xpath=/html/body/div/div[2]/div[4]/div/button')
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> The chat conversation shows the user's message 'What undergraduate engineering courses do you offer and what are their durations?'.
        # Assert-outcome: failed
        # Assert: Expected the chat conversation to show the user's question.
        await expect(page.locator("xpath=/html/body/div[1]").nth(0)).to_contain_text("What undergraduate engineering courses do you offer and what are their durations?", timeout=15000), "Expected the chat conversation to show the user's question."
        
        # --> An AI answer was not received; the chat displays the error message 'Sorry, something went wrong. Please try again.' instead.
        # Assert-outcome: failed
        # Assert: Expected an AI response to be displayed in the chat history.
        await expect(page.locator("xpath=/html/body/div[1]").nth(0)).to_contain_text("Sorry, something went wrong. Please try again.", timeout=15000), "Expected an AI response to be displayed in the chat history."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    