# Day 12, Task 2: Smart Resume Screener

A Streamlit app that scores a resume against a job description and writes short candidate feedback.

## What it does

1. Takes resume text and a job description.
2. Calls Mistral at a low temperature (0.2) with a JSON response format. The model compares skills and experience, then returns a match score, matched skills, missing skills, experience fit, and a recommendation.
3. Calls Mistral again at temperature 0.5 to write a short feedback paragraph.
4. Shows the match score as a metric, matched and missing skills in two columns, and a recommendation badge.
5. Shows token usage and a rough cost estimate.

## Files

- `resume_screener.py`: the app
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
streamlit run resume_screener.py
```

## Deploy on Streamlit Community Cloud

1. Push the repo to GitHub.
2. Create a new app and point it at `Day12/task2/resume_screener.py`.
3. Add `MISTRAL_API_KEY` under app secrets.

## Example

Job description: Python developer with SQL, Docker, and 2 years of experience.

Resume: Python and SQL projects, one year of experience.

Output:

- Match Score: 70
- Matched skills: Python, SQL
- Missing skills: Docker
- Experience fit: fair
- Recommendation: hold
- Feedback: a short paragraph naming the strong Python and SQL work and the missing Docker and experience gap
