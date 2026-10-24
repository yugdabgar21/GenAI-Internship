# Day 12, Task 3: AI Content Studio

A Streamlit app that generates marketing content with a live streaming output.

## What it does

1. Takes a topic, a content type, and a tone.
2. Calls Mistral at temperature 0.8 and streams the reply into the page with `st.write_stream`, so the text appears as it is written.
3. Shows the word count and a token and cost estimate after generation.
4. Regenerate makes a fresh version of the same request.
5. Generates three variations side by side for A/B testing when the checkbox is on.
6. Keeps a history of generated pieces in `st.session_state`.

## Files

- `content_studio.py`: the app
- `requirements.txt`: dependencies
- `.env`: holds `MISTRAL_API_KEY` (not committed)
- `.gitignore`: keeps secrets and caches out of git

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
streamlit run content_studio.py
```

## Deploy on Streamlit Community Cloud

1. Push the repo to GitHub.
2. Create a new app and point it at `Day12/task3/content_studio.py`.
3. Add `MISTRAL_API_KEY` under app secrets.

## Example

Input:

- Topic: Launch of our new eco-friendly water bottle
- Content type: LinkedIn post
- Tone: persuasive

Output: a short LinkedIn post that streams in live, followed by the word count, an estimated token count, and a rough cost.
