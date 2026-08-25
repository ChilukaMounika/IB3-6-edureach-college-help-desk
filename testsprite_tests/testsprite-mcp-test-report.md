# TestSprite AI Testing Report(MCP)

---

## 1️⃣ Document Metadata
- **Project Name:** edureach-agentic-colleage-chatbot
- **Date:** 2026-08-03
- **Prepared by:** TestSprite AI Team

---

## 2️⃣ Requirement Validation Summary

### Feature: Landing Page

#### Test TC002 Browse the homepage college information
- **Test Code:** [TC002_Browse_the_homepage_college_information.py](./TC002_Browse_the_homepage_college_information.py)
- **Status:** ✅ Passed
- **Analysis / Findings:** The user can successfully browse through the homepage and view the expected college information sections.

#### Test TC004 Open the chat drawer from the homepage
- **Test Code:** [TC004_Open_the_chat_drawer_from_the_homepage.py](./TC004_Open_the_chat_drawer_from_the_homepage.py)
- **Status:** ✅ Passed
- **Analysis / Findings:** The chat drawer can be toggled open successfully by clicking the floating chat button on the homepage.

#### Test TC005 Read the homepage content while using the chat widget
- **Test Code:** [TC005_Read_the_homepage_content_while_using_the_chat_widget.py](./TC005_Read_the_homepage_content_while_using_the_chat_widget.py)
- **Status:** ⚠️ BLOCKED
- **Analysis / Findings:** Blocked due to local server tunneling instability causing an ERR_EMPTY_RESPONSE. Cannot verify reading background content while the widget is active.

### Feature: College Chatbot

#### Test TC001 Send a college question and receive a response
- **Test Code:** [TC001_Send_a_college_question_and_receive_a_response.py](./TC001_Send_a_college_question_and_receive_a_response.py)
- **Status:** ⚠️ BLOCKED
- **Analysis / Findings:** Blocked due to the local server tunnel dropping connection. Cannot verify the AI question and response cycle.

#### Test TC003 Continue the same chat with a follow-up question
- **Test Code:** [TC003_Continue_the_same_chat_with_a_follow_up_question.py](./TC003_Continue_the_same_chat_with_a_follow_up_question.py)
- **Status:** ⚠️ BLOCKED
- **Analysis / Findings:** Blocked because the chat widget couldn't be accessed after connection loss.

#### Test TC006 View the chat typing and response states
- **Test Code:** [TC006_View_the_chat_typing_and_response_states.py](./TC006_View_the_chat_typing_and_response_states.py)
- **Status:** ⚠️ BLOCKED
- **Analysis / Findings:** Blocked. Connection issues prevented interacting with the bot to observe the loading and typing indicators.

#### Test TC007 Prevent sending an empty chat message
- **Test Code:** [TC007_Prevent_sending_an_empty_chat_message.py](./TC007_Prevent_sending_an_empty_chat_message.py)
- **Status:** ⚠️ BLOCKED
- **Analysis / Findings:** Blocked. Could not verify whether empty messages are correctly rejected by the UI.

#### Test TC008 Recover from a failed chat request without losing the conversation
- **Test Code:** [TC008_Recover_from_a_failed_chat_request_without_losing_the_conversation.py](./TC008_Recover_from_a_failed_chat_request_without_losing_the_conversation.py)
- **Status:** ⚠️ BLOCKED
- **Analysis / Findings:** Blocked due to network unreachable state. Cannot verify error recovery flows.

---

## 3️⃣ Coverage & Matching Metrics

- **25.00%** of tests passed

| Requirement        | Total Tests | ✅ Passed | ❌ Failed / Blocked |
|--------------------|-------------|-----------|--------------------|
| Landing Page       | 3           | 2         | 1                  |
| College Chatbot    | 5           | 0         | 5                  |
| **Total**          | **8**       | **2**     | **6**              |

---

## 4️⃣ Key Gaps / Risks
1. **Infrastructure Instability during Testing**: The primary risk identified during this test suite execution is the instability of the local server/tunnel connection (ERR_EMPTY_RESPONSE). 75% of tests were blocked because the application server became unreachable mid-test.
2. **Chatbot Unverified**: Because of the connection issues, the core chat features (sending messages, receiving AI responses, empty message prevention) remain largely unverified. A stable test environment is required to validate these critical flows.
