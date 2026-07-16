# Complete Setup Guide: Finance Policy RAG Agent

Follow these step-by-step instructions to get your own version of the Finance Policy RAG Agent up and running in n8n.

## Phase 1: Obtain API Keys

You will need free API keys for the AI models and the vector database.

### 1. Google Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Sign in with your Google account.
3. Click **Get API key** in the left sidebar.
4. Create an API key and copy it to a secure location.

### 2. Pinecone API Key (Vector Database)
1. Go to [Pinecone](https://www.pinecone.io/) and create a free account.
2. In your Pinecone dashboard, click **Create Index**.
3. Name your index (e.g., `finance-kb`).
4. Set the **Dimensions** to `768` (this matches the output size of the `gemini-embedding-2` model).
5. Set the **Metric** to `cosine`.
6. Click **Create Index**.
7. Once created, copy the **Host URL** for your index.
8. Go to the **API Keys** section and copy your API Key.

### 3. Telegram Bot Token
1. Open the Telegram app and search for the **BotFather**.
2. Send the message `/newbot`.
3. Follow the prompts to name your bot and give it a username.
4. The BotFather will give you a **HTTP API Token**. Save this.

---

## Phase 2: Import Workflows into n8n

### 1. Start n8n
If you are running n8n locally via npx, open your terminal and run:
```bash
npx n8n
```
Open your browser to the URL provided (usually `http://localhost:5678`).

### 2. Import the Ingestion Workflow
1. In the n8n UI, go to **Workflows** and click **Add Workflow**.
2. Click the **...** (three dots) in the top right corner and select **Import from File**.
3. Select the `ingestion_workflow.json` file from this repository.
4. Double-click the **Gemini Embed Chunk** node and update the `key` query parameter with your Gemini API Key.
5. Double-click the **Upsert to Pinecone** node and update the `URL` and `Api-Key` header with your Pinecone details.
6. Click **Execute Workflow** to chunk the finance policy text and upload it to Pinecone. You only need to run this once!

### 3. Import the Retrieval Agent Workflow
1. Go back to **Workflows** and click **Add Workflow** again.
2. Import the `Finance RAG — Retrieval Agent.json` file.
3. You will see several nodes that require credentials.

---

## Phase 3: Configure Credentials

### 1. Telegram Trigger & Reply Nodes
1. Double click the **Telegram Trigger** node.
2. Create a new credential for **Telegram API**.
3. Paste the Bot Token you got from the BotFather.
4. Do the same for the **Telegram Reply** nodes at the end of the workflow.

### 2. Pinecone & Gemini API Keys
1. Double click the **Embed Question** node and paste your Gemini API key in the `key` query parameter.
2. Double click the **Query Pinecone** node and paste your Pinecone Host URL and Pinecone API Key.
3. Double click the **Generate Answer** node and paste your Gemini API key in the `key` query parameter.

### 3. Google Sheets (Audit Log)
1. Double click the **Log to Google Sheets** node.
2. Create a new **Google Sheets OAuth2 API** credential and sign in with your Google Account.
3. Create a blank Google Sheet in your Google Drive and name it `Finance Policy Audit Log`.
4. Create a sheet inside it named `Audit Log`.
5. Enter the Document ID from the URL of your Google Sheet into the node.

### 4. Gmail (Escalation Alerts)
1. Double click the **Gmail Escalation Alert** node.
2. Create a new **Gmail OAuth2** credential and sign in.
3. Update the `To Email` parameter to point to the email address of your finance team (or your own email for testing).

---

## Phase 4: Test and Activate!

1. At the bottom of the n8n UI, click **Test Workflow**.
2. Open Telegram and send a message to your bot. For example: *"How many days do I have to process a reimbursement?"*
3. Watch the nodes turn green as the workflow processes your request, searches the vector database, and generates an answer!
4. Check your Telegram app to see the reply.
5. Check your Google Sheet to see the logged audit trail.
6. Once everything is working, toggle the **Active** switch in the top right corner of the workflow to leave the bot running 24/7!

> **Note on Webhooks:** If you are running n8n locally, you will need a tunnel (like Cloudflare or ngrok) so Telegram can send webhooks to your local machine. If you restart your tunnel, remember to update the webhook URL in n8n.
