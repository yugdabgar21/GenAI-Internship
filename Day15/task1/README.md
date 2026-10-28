# Day 15 Task 1: Company knowledge assistant

A Streamlit app that answers employee questions from company policy PDFs and cites the source file.

## What it does

1. Upload one or more PDFs in the sidebar.
2. The app extracts the text page by page, splits it into overlapping chunks, and stores each chunk in a persistent ChromaDB collection. Every chunk keeps its source file name and page number as metadata.
3. Ask a question in the chat box. The app retrieves the closest chunks and sends them to Mistral as context.
4. The answer shows the source file and page, for example `Retrieved from: hr_policies.pdf (pages 1, 2)`.
5. If the answer is not in the documents, the bot says it does not know.
6. Each answer shows the best distance score. A lower distance means a closer match.

## Files

- `hr_policy_bot.py`: the app
- `hr_policies.pdf`: sample handbook with HR, leave, benefits, travel, conduct, IT, and exit policies
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
streamlit run hr_policy_bot.py
```

Then upload `hr_policies.pdf` in the sidebar and ask a question.

## Sample questions

- How many annual leave days do I get?
- What is the health insurance cover?
- What is the notice period?
- Can I work from home?
- How do I claim a travel expense?

## Notes

- The database lives in `chroma_db/` and is reused on later runs, so PDFs are not processed again.
- Files that are already indexed are skipped. Use the **Reset database** button to clear the store and re-index changed documents.
- The confidence value is the ChromaDB distance of the best chunk. It is a relative score, not a percentage.
- The sample PDF is a demo document, not legal advice.

## Deploy on Streamlit Community Cloud

1. Push this folder to GitHub.
2. Create a new app and point it at `Day15/task1/hr_policy_bot.py`.
3. Add `MISTRAL_API_KEY` under app secrets.
