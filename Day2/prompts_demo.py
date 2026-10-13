import os
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

response = client.chat.complete(
    model="mistral-small-latest",
    messages=[
        {"role": "system", 
        "content": "You are a helpful assistant for a clothing store named Urban Thread. For each review output in this format - Sentiment: Positive / Negative / Neutral | Summary: one-line summary. Do not output only 1 word, always give sentiment along with summary. Examples - Input: Jacket zip broke in 2 days, very bad quality. Output: Sentiment: Negative | Summary: Customer unhappy with jacket quality as zip broke quickly. Input: Love the black hoodie, super comfy and perfect fit! Output: Sentiment: Positive | Summary: Customer loves hoodie comfort and fit. Input: Ordered black hoodie, delivered in 3 days. Output: Sentiment: Neutral | Summary: Customer states order delivery fact with no strong feeling."},
        {"role": "user", 
        "content": "Part 1 - Zero shot: Whats the name of Store? Part 2 - Few shot: Using same format as examples, classify this review - Red dress color faded after first wash, not happy."},
    ],
)

print(response.choices[0].message.content)
