import json
import os

import streamlit as st
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Rough cost estimate for mistral-small. Adjust if pricing changes.
COST_PER_1K_TOKENS = 0.0001


def screen(resume, job):
    """Return the structured screening result and the tokens used."""
    response = client.chat.complete(
        model="mistral-small-latest",
        temperature=0.2,
        max_tokens=400,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert technical recruiter screening a resume against a job description. "
                    "Compare the resume skills and experience with the job requirements step by step, "
                    "then reply with ONE JSON object and nothing else. "
                    'Keys: "match_score" (integer 0 to 100), '
                    '"matched_skills" (list of strings), '
                    '"missing_skills" (list of strings), '
                    '"experience_fit" (one of "poor", "fair", "good", "excellent"), '
                    '"recommendation" (one of "reject", "hold", "shortlist", "strong shortlist"). '
                    'Example: resume has Python and SQL but job needs Python, SQL, Docker -> '
                    '{"match_score": 70, "matched_skills": ["Python", "SQL"], '
                    '"missing_skills": ["Docker"], "experience_fit": "good", "recommendation": "shortlist"}.'
                ),
            },
            {
                "role": "user",
                "content": f"JOB DESCRIPTION:\n{job}\n\nRESUME:\n{resume}",
            },
        ],
    )

    raw = response.choices[0].message.content
    if raw is None:
        raise ValueError("The model returned no screening result.")

    data = json.loads(raw)
    for key in ("match_score", "matched_skills", "missing_skills", "experience_fit", "recommendation"):
        if key not in data:
            raise ValueError(f"Missing key in screening result: {key}")

    data["match_score"] = max(0, min(100, int(data["match_score"])))
    tokens = response.usage.total_tokens if response.usage else 0
    return data, tokens


def write_feedback(resume, job, result):
    """Return a short candidate feedback paragraph and the tokens used."""
    response = client.chat.complete(
        model="mistral-small-latest",
        temperature=0.5,
        max_tokens=200,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a recruiter writing feedback to a candidate. "
                    "Write a short paragraph (under 100 words) that names their strengths "
                    "and the main gaps versus the job. Be constructive and specific. "
                    "Use only details from the resume, job, and screening result."
                ),
            },
            {
                "role": "user",
                "content": f"Job: {job}\nResume: {resume}\nScreening: {result}",
            },
        ],
    )

    text = response.choices[0].message.content
    if not text:
        raise ValueError("The model returned no feedback.")

    tokens = response.usage.total_tokens if response.usage else 0
    return text.strip(), tokens


st.set_page_config(page_title="Smart Resume Screener", page_icon="📄", layout="wide")

st.title("Smart Resume Screener")
st.write("Screen a resume against a job description and get a fit score.")

resume_text = st.text_area("Resume text", height=250)
job_text = st.text_area("Job description", height=250)

if st.button("Screen"):
    if not resume_text.strip():
        st.warning("Please enter a resume.")
    elif not job_text.strip():
        st.warning("Please enter a job description.")
    else:
        try:
            with st.spinner("Screening resume..."):
                result, screen_tokens = screen(resume_text, job_text)

            st.metric("Match Score", result["match_score"])

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Matched skills")
                for skill in result["matched_skills"]:
                    st.write(f"- {skill}")
            with col2:
                st.subheader("Missing skills")
                for skill in result["missing_skills"]:
                    st.write(f"- {skill}")

            st.write("**Experience fit:**", result["experience_fit"].title())
            recommendation = result["recommendation"]
            if recommendation in ("strong shortlist", "shortlist"):
                st.success(f"Recommendation: {recommendation}")
            elif recommendation == "hold":
                st.info(f"Recommendation: {recommendation}")
            else:
                st.warning(f"Recommendation: {recommendation}")

            with st.spinner("Writing feedback..."):
                feedback, feedback_tokens = write_feedback(resume_text, job_text, result)

            st.subheader("Candidate feedback")
            st.text_area("Edit before sending", value=feedback, height=150)

            total_tokens = screen_tokens + feedback_tokens
            cost = total_tokens / 1000 * COST_PER_1K_TOKENS
            st.caption(f"Tokens used: {total_tokens} | Estimated cost: ${cost:.6f}")

            with st.expander("Raw screening JSON"):
                st.json(result)
        except json.JSONDecodeError:
            st.error("The model did not return valid JSON. Please try again.")
        except Exception as error:
            st.error(f"Something went wrong: {error}")
