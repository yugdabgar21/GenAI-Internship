# Day 23: General Knowledge Answer Evaluator

A small Streamlit app. You ask a general knowledge question. Mistral writes the answer. Groq then acts as a strict judge and scores the answer.

## How it works

1. You type a question such as "What is the capital of Australia?".
2. Mistral (`mistral-small-latest`) writes the answer.
3. Groq (`openai/gpt-oss-20b`) reads the question and the answer and returns:
   - a score from 0 to 10
   - a verdict: poor, fair, good, or excellent
   - a short list of strengths
   - a short list of weaknesses
   - a one or two sentence summary
4. The page shows the answer followed by the evaluation.

## Files

- `evaluator_app.py`: the app. It contains the two API calls and the JSON parser.
- `requirements.txt`: the Python packages you need.
- `.env.example`: the two keys the app expects.

## Setup

Install the packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file in this folder:

```
MISTRAL_API_KEY=your_mistral_key_here
GROQ_API_KEY=your_groq_key_here
```

If a key is missing, the page shows an error message instead of crashing.

## Run

```bash
streamlit run evaluator_app.py
```

Open the local URL that Streamlit prints, usually http://localhost:8501.

## Test inputs

Copy one of these into the question box and click Generate & Evaluate:

- What is the capital of Australia?
- Who wrote the novel "Nineteen Eighty-Four"?
- Why is the sky blue?

## Notes

- The judge is asked to reply with only a JSON object. If it returns plain text instead, the page shows the raw text with a warning, so nothing breaks.
- Scores are the judge's opinion. Ask the same question twice and the score can move by a point.
- `.env` holds real API keys. It is ignored by git. Keep it that way.
