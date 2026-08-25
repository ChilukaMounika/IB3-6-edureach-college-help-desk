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
        
        # -> Open the chat by clicking the 'Chat with EduReach Bot' button (the floating chat button).
        # Chat with EduReach Bot button
        elem = page.get_by_role('button', name='Chat with EduReach Bot', exact=True)
        await elem.click(timeout=10000)
        
        # -> Type a college question into the 'Ask a question...' field and click the send (paper-plane) button to submit the message.
        # Ask a question... text field
        elem = page.get_by_placeholder('Ask a question...', exact=True)
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("What courses do you offer for AI and Data Science, and what are the admission requirements?")
        
        # -> Type a college question into the 'Ask a question...' field and click the send (paper-plane) button to submit the message.
        # button
        elem = page.locator('xpath=/html/body/div/div[2]/div[4]/div/button')
        await elem.click(timeout=10000)
        
        # --> Assertions to verify final state
        
        # --> Verify an assistant response is displayed
        # Assert: Expected assistant response to include an answer to the user's question about AI & Data Science programs and admission requirements.
        await expect(page.locator("xpath=/html/body/div[1]/div[2]/div[2]/div[1]/div[1]").nth(0)).to_contain_text("We offer an AI & Data Science B.Tech program", timeout=15000), "Expected assistant response to include an answer to the user's question about AI & Data Science programs and admission requirements."
        
        # --> Verify the conversation history remains visible
        await page.locator("xpath=/html/body/div[1]/div[2]/div[1]/div[1]/div[1]").nth(0).scroll_into_view_if_needed()
        # Assert: Expected the conversation panel to remain visible.
        await expect(page.locator("xpath=/html/body/div[1]/div[2]/div[1]/div[1]/div[1]").nth(0)).to_be_visible(timeout=15000), "Expected the conversation panel to remain visible."
        await page.locator("xpath=/html/body/div[1]/div[2]/div[3]/div/input").nth(0).scroll_into_view_if_needed()
        # Assert: Expected the message input field to remain visible.
        await expect(page.locator("xpath=/html/body/div[1]/div[2]/div[3]/div/input").nth(0)).to_be_visible(timeout=15000), "Expected the message input field to remain visible."
        await page.locator("xpath=/html/body/div[1]/div[2]/div[3]/div/button").nth(0).scroll_into_view_if_needed()
        # Assert: Expected the send button to remain visible.
        await expect(page.locator("xpath=/html/body/div[1]/div[2]/div[3]/div/button").nth(0)).to_be_visible(timeout=15000), "Expected the send button to remain visible."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    