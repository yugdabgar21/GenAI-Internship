import random

from pymilvus import MilvusClient

# Milvus Lite: a local, file-backed vector database (no Docker/server needed).
client = MilvusClient("milvus_demo.db")

collection_name = "library_policy"

# Start fresh on every run.
if client.has_collection(collection_name=collection_name):
    client.drop_collection(collection_name=collection_name)

client.create_collection(
    collection_name=collection_name,
    dimension=768,
)

docs = [
    "CITY PUBLIC LIBRARY - MEMBERSHIP: Any resident of Anand district can apply for a library card by submitting proof of address and a passport-size photograph. Membership is free for students and senior citizens.",
    "BORROWING RULES: A member can borrow up to 4 books at a time for 14 days. Books can be renewed once if no one else has reserved them. Late returns attract a fine of Rs. 5 per day per book.",
    "REFERENCE SECTION: Reference books, encyclopedias, and rare collections cannot be borrowed and must be used inside the library.",
    "LOST OR DAMAGED BOOKS: If a book is lost or damaged, the member must pay the replacement cost plus a processing fee of Rs. 50.",
    "DIGITAL RESOURCES: Members can access e-books and online journals using their library card number on the library portal.",
    "CODE OF CONDUCT: Members must maintain silence in reading halls and keep mobile phones on silent mode.",
]

# Easiest path: use random vectors (no embedding model download).
# Note: results will not reflect real semantic similarity.
vectors = [[random.uniform(-1, 1) for _ in range(768)] for _ in docs]
data = [
    {"id": i, "vector": vectors[i], "text": docs[i]}
    for i in range(len(docs))
]

client.insert(collection_name=collection_name, data=data)

query = "What are the rules for borrowing books and late returns?"
query_vectors = [[random.uniform(-1, 1) for _ in range(768)]]

res = client.search(
    collection_name=collection_name,
    data=query_vectors,
    limit=3,
    output_fields=["text"],
)

print(res)

# Clean up the demo collection when done.
client.drop_collection(collection_name=collection_name)
