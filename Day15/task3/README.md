# Day 15 Task 3: Study buddy

A Streamlit app that lets a student chat with a textbook chapter or research paper, generate a quiz, and get a summary.

## What it does

1. Upload a textbook chapter or research paper PDF in the sidebar.
2. The app reads the PDF page by page, splits it into overlapping chunks, and stores each chunk in a persistent ChromaDB collection. Every chunk keeps its source file name and page number.
3. Three tabs:
   - **Ask**: chat with the document. Answers come only from the content and show the source page.
   - **Quiz**: pick easy, medium, or hard, then generate 5 quiz questions. Answers are hidden in a collapsible box.
   - **Summarize**: generate a short bullet summary of the whole document.
4. Chat history stays in `st.session_state`.
5. Long documents are sampled across all chunks for quiz and summary, so the app stays within the model context limit.

## Files

- `study_buddy.py`: the app
- `ml_chapter.pdf`: sample chapter "Introduction to Machine Learning" with supervised and unsupervised learning, training, evaluation, applications, and key terms
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
streamlit run study_buddy.py
```

Then upload `ml_chapter.pdf` in the sidebar and try the tabs.

## Sample questions

- What is the difference between supervised and unsupervised learning?
- What is overfitting?
- How is F1 score calculated?
- What split is common for training, validation, and test data?
- What is the bias-variance tradeoff?

## Notes

- The database lives in `chroma_db/` and is reused on later runs, so the PDF is not processed again.
- Files that are already indexed are skipped. Use the **Reset database** button to clear the store and re-index changed documents.
- The sample chapter is a demo document, not a course replacement.

## Deploy on Streamlit Community Cloud

1. Push this folder to GitHub.
2. Create a new app and point it at `Day15/task3/study_buddy.py`.
3. Add `MISTRAL_API_KEY` under app secrets.
