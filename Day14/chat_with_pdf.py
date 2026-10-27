from pypdf import PdfReader
import chromadb
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# read pdf and extract text
reader = PdfReader(os.path.join(BASE_DIR, "sample.pdf"))
text = ""
for page in reader.pages:
    text += page.extract_text() or ""

# chunking
def chunks_text(text, chunk_size=500, overlap=50):
    start = 0
    chunks = []
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap
    return chunks

chunks = chunks_text(text)

# embedding and store in db
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("chatwithpdf")

collection.add(
    documents=chunks,
    ids=[str(i) for i in range(len(chunks))],
)

# user input
user_input = input("Ask question to pdf: ")

relevant = collection.query(
    query_texts=user_input,
    n_results=4,
)

context = "\n\n".join(relevant["documents"][0])

# injection + generation
user_prompt = f"""
Provide an answer based on the user input using only the context below.
If the answer is not in the context, reply with "I don't Know".

Context:
{context}

Question: {user_input}
"""

if not os.getenv("MISTRAL_API_KEY"):
    raise SystemExit("MISTRAL_API_KEY is not set. Add it to Day14/.env")

mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

response = mistral_client.chat.complete(
    model="mistral-small-latest",
    temperature=0.6,
    messages=[
        {
            "role": "user",
            "content": user_prompt,
        },
    ],
)

print(response.choices[0].message.content)
