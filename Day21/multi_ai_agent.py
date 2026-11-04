import os
import sys
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

# Windows console can choke on unicode
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


def run_agent(role, content):
    response = client.chat.complete(
        model="mistral-small-latest",
        temperature=0.4,
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


topic = input("Enter a Product/Topic : ")

# Agent 1 - Research Agent
print(f"Research Work Start on this topic {topic}")
research_content = run_agent(
    "You are a Professional Research Agent responsible for conducting in-depth research on a given product. Gather, verify, and analyze relevant facts, specifications, features, pros, cons, and user feedback from credible sources. Ensure accurate, well-structured, and evidence-based research. Keep the research concise, factual, and organized. Generate output in approximately 200 words.",
    f"Research product is {topic}",
)
print("Research Agent Task is Complete ....")

# Agent 2 - Writer Agent
print(f"Writing Work Start on this topic {topic}")
draft_review = run_agent(
    "You are a Professional Content Writer Agent responsible for creating an original, engaging, and informative product review based on research. Write clear, well-structured, reader-friendly content with a verdict, pros and cons, and a recommendation. Keep it concise and honest. Generate output in approximately 200 words.",
    f"here is research content : {research_content}",
)
print("Writing Agent Task is Complete ....")

# Agent 3 - Editor Agent
print(f"Editing Work Start on this topic {topic}")
final = run_agent(
    "You are a Professional Review Editor responsible for reviewing, refining, and formatting the product review into a polished, professional, publication-ready format. Correct grammar, spelling, punctuation, sentence structure, and readability while improving headings, paragraphs, flow, and consistency without changing the original meaning. Ensure the final review looks professional, engaging, well-organized, and SEO-friendly. Generate output in approximately 200 words.",
    f"here is draft review : {draft_review}",
)

print(f"Here Final Product Review : {final}")
