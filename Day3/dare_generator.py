import os
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

num_people = input("Group size (e.g. 4): ").strip()
mood = input("Mood (funny / chill / filmy): ").strip().lower()
language = input("Language (english / hinglish / gujlish): ").strip().lower()
num_dares = input("How many dares (e.g. 3): ").strip()

if language not in ("english", "hinglish", "gujlish"):
    print("Unknown language, using hinglish.")
    language = "hinglish"

system_prompt = (
    "You are a fun party host for game nights. "
    "Generate ONLY harmless, safe, family-friendly dares. "
    "Rules: no physical danger, no alcohol, no personal contact, "
    "no embarrassment, house items only. "
    "Output a numbered list only, one dare per line."
)

if language == "hinglish":
    system_prompt += (
        " Write in Hinglish (Hindi in Roman script). "
        'Example: "Apne best filmy dialogue ko full action ke saath bolo."'
    )
elif language == "gujlish":
    system_prompt += (
        " Write ONLY in Gujlish (Gujarati in Roman script, no Hindi words). "
        "Use words like tara, tamne, karo, batav, hasav. "
        'Examples: "Tara best Garba step 30 second ma kari ne batav." '
        '"Room ma rakhela koi pan 3 vastu upadi ne tenu funny Gujarati naam aapo."'
    )

response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.9,
    max_tokens=400,
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Group of {num_people} people, mood {mood}, language {language}. Give {num_dares} dares.",
        },
    ],
)

print(response.choices[0].message.content)
