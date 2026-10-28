# Day 15 Task 2: Customer support doc bot

A Streamlit app that answers customer questions from a product manual and falls back to a support email when the answer is not in the docs.

## What it does

1. Upload the product manual PDF in the sidebar.
2. The app reads the PDF page by page, splits it into overlapping chunks, and stores each chunk in a persistent ChromaDB collection. Every chunk keeps its source file name and page number.
3. The customer asks a question in the chat box. The app retrieves the closest sections and sends them to Mistral as context.
4. The answer shows the source file and page, plus the matching manual section in a collapsible box.
5. If the answer is not in the manual, the bot says it could not find the answer and asks the customer to contact support@company.com.
6. The chat history stays in `st.session_state`, so the conversation looks like a normal support chat.
7. Each answer has a thumbs up and thumbs down button. The last answer also suggests 3 related questions you can click to ask.

## Files

- `customer_support_bot.py`: the app
- `skyhawk_pro_manual.pdf`: sample drone manual with setup, flight modes, camera, app, maintenance, troubleshooting, safety, and warranty
- `requirements.txt`: dependencies
- `.env.example`: copy this to `.env` and add your key
- `.gitignore`: keeps secrets and the local database out of git

## Run locally

```bash
pip install -r requirements.txt
```

Create a `.env` file in this folder:

```
MISTRAL_API_KEY=your_key_here
```

Start the app:

```bash
streamlit run customer_support_bot.py
```

Then upload `skyhawk_pro_manual.pdf` in the sidebar and ask a question.

## Sample questions

- How long does the battery take to charge?
- How do I start Return to Home?
- What is the maximum video resolution?
- What should I do if the drone loses connection?
- Can I fly in the rain?
- How long is the warranty?

## Notes

- The database lives in `chroma_db/` and is reused on later runs, so the manual is not processed again.
- Files that are already indexed are skipped. Use the **Reset database** button to clear the store and re-index changed documents.
- The sample manual is a demo document, not safety or legal advice.

## Deploy on Streamlit Community Cloud

1. Push this folder to GitHub.
2. Create a new app and point it at `Day15/task2/customer_support_bot.py`.
3. Add `MISTRAL_API_KEY` under app secrets.
