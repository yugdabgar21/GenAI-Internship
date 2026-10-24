import os

import streamlit as st
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

CONTENT_TYPES = ["Blog intro", "LinkedIn post", "Product description", "Email"]
TONES = ["professional", "casual", "persuasive", "friendly", "witty"]

# Rough cost estimate for mistral-small. Adjust if pricing changes.
COST_PER_1K_TOKENS = 0.0001


def stream_one(topic, content_type, tone):
    """Yield streamed chunks from Mistral for one piece of content."""
    response = client.chat.stream(
        model="mistral-small-latest",
        temperature=0.8,
        max_tokens=350,
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a marketing copywriter. Write a {content_type.lower()} "
                    f"in a {tone} tone. Use only the topic details. "
                    "Keep it concise, engaging, and ready to publish."
                ),
            },
            {"role": "user", "content": f"Topic: {topic}"},
        ],
    )

    for chunk in response:
        content = chunk.data.choices[0].delta.content
        if content:
            yield content


st.set_page_config(page_title="AI Content Studio", page_icon="✍️", layout="wide")

st.title("AI Content Studio")
st.write("Generate marketing content with a live streaming output.")

if "history" not in st.session_state:
    st.session_state.history = []

topic = st.text_input("Topic", placeholder="e.g. Launch of our new eco-friendly water bottle")
content_type = st.selectbox("Content type", CONTENT_TYPES)
tone = st.selectbox("Tone", TONES)
variations = st.checkbox("Generate 3 variations (A/B testing)")

generate = st.button("Generate")
regenerate = st.button("Regenerate")

if generate or regenerate:
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        try:
            if variations:
                cols = st.columns(3)
                texts = []
                for index, col in enumerate(cols):
                    with col:
                        st.subheader(f"Variation {index + 1}")
                        text = st.write_stream(stream_one(topic, content_type, tone))
                        texts.append(text or "")

                for index, text in enumerate(texts, start=1):
                    words = len(text.split())
                    tokens = int(words * 1.3)
                    cost = tokens / 1000 * COST_PER_1K_TOKENS
                    st.caption(
                        f"Variation {index}: {words} words | ~{tokens} tokens | ${cost:.6f}"
                    )

                st.session_state.history.append(
                    {"topic": topic, "type": content_type, "tone": tone, "text": texts[0]}
                )
            else:
                st.subheader("Generated content")
                full_text = st.write_stream(stream_one(topic, content_type, tone))
                full_text = full_text or ""

                words = len(full_text.split())
                tokens = int(words * 1.3)
                cost = tokens / 1000 * COST_PER_1K_TOKENS

                st.metric("Word count", words)
                st.caption(f"Estimated tokens: {tokens} | Estimated cost: ${cost:.6f}")
                st.code(full_text)

                st.session_state.history.append(
                    {"topic": topic, "type": content_type, "tone": tone, "text": full_text}
                )
        except Exception as error:
            st.error(f"Something went wrong: {error}")

with st.expander("History"):
    if not st.session_state.history:
        st.write("No content generated yet.")
    else:
        for item in reversed(st.session_state.history):
            st.write(f"**{item['type']}** ({item['tone']}) - {item['topic']}")
            st.write(item["text"])
            st.divider()
