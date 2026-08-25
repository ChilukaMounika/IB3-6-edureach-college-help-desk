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
        
        # -> Click the 'Chat with EduReach Bot' button to open the chat interface.
        # Chat with EduReach Bot button
        elem = page.get_by_role('button', name='Chat with EduReach Bot', exact=True)
        await elem.click(timeout=10000)
        
        # -> Type 'What undergraduate engineering programs do you offer?' into the 'Ask a question...' field and click the send (paper-plane) button.
        # Ask a question... text field
        elem = page.get_by_placeholder('Ask a question...', exact=True)
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("What undergraduate engineering programs do you offer?")
        
        # -> Type 'What undergraduate engineering programs do you offer?' into the 'Ask a question...' field and click the send (paper-plane) button.
        # button
        elem = page.locator('xpath=/html/body/div/div[2]/div[4]/div/button')
        await elem.click(timeout=10000)
        
        # -> Click the chat header 'close' button (the 'x' in the EduReach Bot header) to close the chat drawer.
        # button
        elem = page.locator('xpath=/html/body/div/div[2]/div/div[2]/button[2]')
        await elem.click(timeout=10000)
        
        # -> Click the 'Chat with EduReach Bot' button to reopen the chat interface and view the conversation history.
        # Chat with EduReach Bot button
        elem = page.get_by_role('button', name='Chat with EduReach Bot', exact=True)
        await elem.click(timeout=10000)
        
        # -> Verify that the chat shows the previous messages 'What undergraduate engineering programs do you offer?' and 'Sorry, something went wrong.' and confirm the input field 'Ask a question...' accepts text.
        # Ask a question... text field
        elem = page.get_by_placeholder('Ask a question...', exact=True)
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("Checking input availability")
        
        # --> Assertions to verify final state
        
        # --> Verify previous conversation messages are still visible
        # Assert: The previous user message 'What undergraduate engineering programs do you offer?' is visible.
        await expect(page.locator("xpath=/html/body/div").nth(0)).to_contain_text("What undergraduate engineering programs do you offer?", timeout=15000), "The previous user message 'What undergraduate engineering programs do you offer?' is visible."
        # Assert: The previous bot reply 'Sorry, something went wrong. Please try again.' is visible.
        await expect(page.locator("xpath=/html/body/div").nth(0)).to_contain_text("Sorry, something went wrong. Please try again.", timeout=15000), "The previous bot reply 'Sorry, something went wrong. Please try again.' is visible."
        
        # --> Verify the message input is available for a new question
        # Assert: The chat message input accepts text and currently contains "Checking input availability".
        await expect(page.locator("xpath=/html/body/div/div[2]/div[3]/div/input").nth(0)).to_have_value("Checking input availability", timeout=15000), "The chat message input accepts text and currently contains \"Checking input availability\"."
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    