import os

import streamlit as st
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

# st.title("GEN AI Session..")
# st.header("Chapter 7 Token and Cost Control and streaming ...")
# st.write("Every API Costs Money ..")
# st.warning("You hit API Limit...")
# st.success("Congrats you become a father..")

# # input 

# address = st.text_area("Enter your Address")
# gfname = st.text_input("ENter your gf name ")
# age = st.slider("Enter your age",0,100,25)
# mood = st.selectbox("Mood", ["Happy","angry","bad"])


# if st.button("submit"):
#     print(address,gfname, age ,mood )
#     st.success("your data is submiited")

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

st.title("Flashcard Generator")
st.write("Turn a topic or your notes into study flashcards.")

with st.form("flashcard_form", clear_on_submit=True):
    topic = st.text_area("Topic or notes", placeholder="e.g. Photosynthesis")
    num_cards = st.slider("Number of flashcards", 5, 20, 10)
    difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])
    submitted = st.form_submit_button("Generate")

if submitted:
    if not topic.strip():
        st.warning("Please enter a topic or some notes.")
    else:
        with st.spinner("Generating flashcards..."):
            response = client.chat.stream(
                model="mistral-small-latest",
                temperature=0.5,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You create study flashcards. "
                            f"Produce exactly {num_cards} flashcards at {difficulty} difficulty. "
                            "Format each card as two lines:\n"
                            "Q: <question>\n"
                            "A: <answer>\n"
                            "Separate cards with one blank line. "
                            "Do not add extra commentary."
                        ),
                    },
                    {"role": "user", "content": topic},
                ],
            )

            def token_stream():
                for chunk in response:
                    content = chunk.data.choices[0].delta.content
                    if content:
                        yield content

            st.write_stream(token_stream())

        st.success("Flashcards generated successfully!")
