import json
import os

import streamlit as st
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

TONES = ["apologetic", "professional", "friendly"]

# Rough cost estimate for mistral-small. Adjust if pricing changes.
COST_PER_1K_TOKENS = 0.0001


def analyze(message):
    """Return the structured analysis and the tokens used."""
    response = client.chat.complete(
        model="mistral-small-latest",
        temperature=0.2,
        max_tokens=200,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You triage customer support messages. "
                    "Think step by step about the emotion, topic, and severity, "
                    "then reply with ONE JSON object and nothing else. "
                    'Keys: "sentiment" (positive, negative, neutral, mixed), '
                    '"category" (billing, technical, account, shipping, general), '
                    '"urgency" (integer 1 to 5), '
                    '"key_issue" (short phrase, max 8 words). '
                    'Examples: "I was charged twice" -> '
                    '{"sentiment": "negative", "category": "billing", "urgency": 4, "key_issue": "double charged"}. '
                    '"The app crashes when I upload a photo" -> '
                    '{"sentiment": "negative", "category": "technical", "urgency": 3, "key_issue": "app crash on upload"}. '
                    '"How do I reset my password?" -> '
                    '{"sentiment": "neutral", "category": "account", "urgency": 2, "key_issue": "password reset help"}.'
                ),
            },
            {"role": "user", "content": message},
        ],
    )

    raw = response.choices[0].message.content
    if raw is None:
        raise ValueError("The model returned no analysis.")

    data = json.loads(raw)

    for key in ("sentiment", "category", "urgency", "key_issue"):
        if key not in data:
            raise ValueError(f"Missing key in the analysis: {key}")

    data["urgency"] = max(1, min(5, int(data["urgency"])))
    tokens = response.usage.total_tokens if response.usage else 0
    return data, tokens


def draft_reply(message, analysis, tone):
    """Return a suggested reply and the tokens used."""
    response = client.chat.complete(
        model="mistral-small-latest",
        temperature=0.7,
        max_tokens=250,
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a customer support agent. Write the reply in a {tone} tone. "
                    "Use only details from the customer message and the analysis. "
                    "Keep it under 120 words. Do not invent order numbers, dates, or policies. "
                    "End with a clear next step."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Customer message: {message}\n"
                    f"Analysis: sentiment={analysis['sentiment']}, "
                    f"category={analysis['category']}, urgency={analysis['urgency']}, "
                    f"key_issue={analysis['key_issue']}"
                ),
            },
        ],
    )

    text = response.choices[0].message.content
    if not text:
        raise ValueError("The model returned no reply.")

    tokens = response.usage.total_tokens if response.usage else 0
    return text.strip(), tokens


st.set_page_config(page_title="AI Customer Support Dashboard", page_icon="🎧", layout="wide")

st.title("AI Customer Support Dashboard")
st.write("Analyze a customer message, then draft a reply in the tone you pick.")

message = st.text_area(
    "Customer message",
    height=150,
    placeholder="Paste the customer's message here...",
)
auto_tone = st.checkbox("Auto-pick tone from sentiment", value=True)
tone = st.selectbox("Reply tone", TONES, disabled=auto_tone)

if st.button("Analyze"):
    if not message.strip():
        st.warning("Please enter a customer message.")
    else:
        try:
            with st.spinner("Analyzing message..."):
                analysis, analysis_tokens = analyze(message)

            if auto_tone:
                tone_used = {
                    "negative": "apologetic",
                    "positive": "friendly",
                }.get(analysis["sentiment"], "professional")
            else:
                tone_used = tone

            with st.spinner("Drafting reply..."):
                reply, reply_tokens = draft_reply(message, analysis, tone_used)

            st.session_state.result = {
                "analysis": analysis,
                "reply": reply,
                "tone_used": tone_used,
                "tokens": analysis_tokens + reply_tokens,
            }
        except json.JSONDecodeError:
            st.error("The model did not return valid JSON. Please try again.")
        except Exception as error:
            st.error(f"Something went wrong: {error}")

if "result" in st.session_state:
    result = st.session_state.result
    analysis = result["analysis"]

    st.subheader("Structured analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric("Urgency", f"{analysis['urgency']}/5")
    col2.metric("Sentiment", analysis["sentiment"].title())
    col3.metric("Category", analysis["category"].title())

    st.write("**Key issue:**", analysis["key_issue"])
    st.write("**Tone used:**", result["tone_used"])

    st.subheader("Suggested reply")
    edited_reply = st.text_area(
        "Edit the reply before sending",
        value=result["reply"],
        height=180,
    )

    if st.button("Send reply"):
        st.success("Reply sent (simulated).")
        st.write(edited_reply)

    tokens = result["tokens"]
    cost = tokens / 1000 * COST_PER_1K_TOKENS
    st.caption(f"Tokens used: {tokens} | Estimated cost: ${cost:.6f}")

    with st.expander("Raw analysis JSON"):
        st.json(analysis)
