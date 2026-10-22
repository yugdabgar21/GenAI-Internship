import json
import os

from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.4,
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "You analyze movie reviews. "
    "Reply with one JSON object and nothing else. "
    'Keys: "sentiment" (one of "positive", "negative", "mixed"), '
    '"rating_score" (integer 1 to 5 stars, where 1 is terrible and 5 is excellent), '
    '"summarize" (one short sentence, max 20 words).'},
        {"role": "user", "content": "The visuals were stunning but the plot dragged in the middle "
    "and the ending felt rushed."},
    ],
)

raw = response.choices[0].message.content

if raw is None:
    print("No content returned by the model.")
else:
    print(raw)
    try:
        data = json.loads(raw)
        print("Sentiment:", data["sentiment"])
        print("Rating:", data["rating_score"])
        print("Summary:", data["summarize"])
    except json.JSONDecodeError:
        print("Error while parsing to JSON.")
    except KeyError as missing:
        print(f"Missing key in response: {missing}")
