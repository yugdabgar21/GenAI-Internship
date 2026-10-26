import chromadb

client = chromadb.Client()

collection = client.create_collection(name="doc_genai")

documents = [
    "CITY PUBLIC LIBRARY - MEMBERSHIP AND BORROWING POLICY Library Location: Anand, Gujarat. 1. Membership Any resident of Anand district can apply for a library card by submitting proof of address and a passport-size photograph. Membership is free for students and senior citizens.",

    "2. Borrowing Rules A member can borrow up to 4 books at a time for 14 days. Books can be renewed once if no one else has reserved them. Late returns attract a fine of Rs. 5 per day per book. 3. Reference Section Reference books, encyclopedias, and rare collections cannot be borrowed and must be used inside the library.",

    "4. Lost or Damaged Books If a book is lost or damaged, the member must pay the replacement cost plus a processing fee of Rs. 50. 5. Digital Resources Members can access e-books and online journals using their library card number on the library portal. 6. Code of Conduct Members must maintain silence in reading halls and keep mobile phones on silent mode. Note: This is a sample document created for RAG/vector database testing. It is not an official library policy."
]

collection.add(
    ids=["1", "2", "3"],
    documents=documents
)

result = collection.query(
    query_texts=["What are the rules for borrowing books and late returns?"],
    n_results=4
)

print(result)
