import json
import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from mistralai.client import Mistral

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

mistral_client = Mistral(api_key=MISTRAL_API_KEY) if MISTRAL_API_KEY else None
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

MISTRAL_MODEL = "mistral-small-latest"
JUDGE_MODEL = "openai/gpt-oss-20b"

JUDGE_PROMPT = (
    "You are a strict evaluator judging an answer to a general knowledge question. "
    "Check factual correctness first, then completeness and clarity. "
    "Be honest: a wrong or made-up fact must lower the score hard, even if the answer sounds confident. "
    "Reply with ONE JSON object and nothing else. Keys: "
    '"score" (integer 0 to 10), '
    '"verdict" (one of "poor", "fair", "good", "excellent"), '
    '"strengths" (list of short strings), '
    '"weaknesses" (list of short strings), '
    '"summary" (one or two sentences). '
    "Example: "
    '{"score": 6, "verdict": "fair", "strengths": ["Names the right city"], '
    '"weaknesses": ["Does not explain why"], "summary": "Correct but very brief."}'
)


def ask_mistral(question):
    """Send the question to Mistral and return the answer text."""
    response = mistral_client.chat.complete(
        model=MISTRAL_MODEL,
        temperature=0.6,
        messages=[{"role": "user", "content": question}],
    )
    answer = response.choices[0].message.content
    if not answer:
        raise ValueError("Mistral returned an empty answer.")
    return answer.strip()


def evaluate_answer(question, answer):
    """Ask Groq to judge the answer and return the raw evaluation text."""
    response = groq_client.chat.completions.create(
        model=JUDGE_MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {
                "role": "user",
                "content": f"Question: {question}\n\nAnswer to evaluate:\n{answer}",
            },
        ],
    )
    raw = response.choices[0].message.content
    if not raw:
        raise ValueError("Groq returned an empty evaluation.")
    return raw.strip()


def parse_evaluation(raw):
    """Turn the judge output into a dict with a safe score and clean lists."""
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("The judge did not return a JSON object.")

    data = json.loads(text[start : end + 1])

    for key in ("score", "verdict", "strengths", "weaknesses", "summary"):
        if key not in data:
            raise ValueError(f"Missing key in evaluation: {key}")

    data["score"] = max(0, min(10, int(data["score"])))
    data["verdict"] = str(data["verdict"]).strip().lower()
    data["strengths"] = [str(item) for item in data["strengths"]]
    data["weaknesses"] = [str(item) for item in data["weaknesses"]]
    data["summary"] = str(data["summary"]).strip()
    return data


st.set_page_config(page_title="General Knowledge Answer Evaluator", layout="centered")

st.title("General Knowledge Answer Evaluator")
st.caption("Mistral answers your question, Groq judges the answer.")

question = st.text_area(
    "Enter your question",
    height=120,
    placeholder="Type your question here...",
)

if st.button("Generate & Evaluate"):
    if not question.strip():
        st.warning("Please enter a question first.")
    elif mistral_client is None or groq_client is None:
        st.error("Missing API keys. Add MISTRAL_API_KEY and GROQ_API_KEY to Day23/.env.")
    else:
        try:
            with st.spinner("Mistral is answering..."):
                answer = ask_mistral(question.strip())

            st.subheader("Mistral's Answer")
            st.write(answer)

            with st.spinner("Groq is evaluating the answer..."):
                raw = evaluate_answer(question.strip(), answer)

            st.subheader("Groq's Evaluation")
            try:
                evaluation = parse_evaluation(raw)
            except ValueError:
                st.warning("Could not read the evaluation as JSON. Showing the raw output instead.")
                st.write(raw)
            else:
                st.metric("Score", f"{evaluation['score']} / 10")
                st.write(f"**Verdict:** {evaluation['verdict'].title()}")

                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Strengths**")
                    if evaluation["strengths"]:
                        for item in evaluation["strengths"]:
                            st.write(f"- {item}")
                    else:
                        st.write("- None listed")
                with col2:
                    st.write("**Weaknesses**")
                    if evaluation["weaknesses"]:
                        for item in evaluation["weaknesses"]:
                            st.write(f"- {item}")
                    else:
                        st.write("- None listed")

                st.write(f"**Summary:** {evaluation['summary']}")

                with st.expander("Raw judge JSON"):
                    st.json(evaluation)
        except Exception as error:
            st.error(f"Something went wrong: {error}")
