import os
import sys
from mistralai.client import Mistral
from dotenv import load_dotenv


load_dotenv()

# Windows console can choke on unicode such as smart quotes
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


def run_agent(role, content):
    response = client.chat.complete(
        model="mistral-small-latest",
        temperature=0.6,
        messages=[
            {
                "role": "system",
                "content": role,
            },
            {
                "role": "user",
                "content": content,
            },
        ],
    )

    return response.choices[0].message.content


topic = input("Enter a Topic : ")

print("Single AI Agent Start Working ...")

result = run_agent(
    """You are a Senior LinkedIn Content Strategist responsible for the complete post creation process. Research the topic, verify facts using credible sources, and write an original, engaging, professional LinkedIn post. Edit and proofread every post for accuracy, grammar, clarity, readability, and structure before delivering publication-ready content. Format: a strong hook line, 3-5 short paragraphs with line breaks, a call to action, and 3-5 relevant hashtags. Keep it under 1300 characters. Here is the topic to generate a LinkedIn post on : """,
    f"write a LinkedIn post in short on this topic : {topic}",
)

print(result)
