
import json
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from src.services.retriever import vector_db
from src.config import settings

def ingest_faqs():
    print("🚀 Starting Data Ingestion...")
    
    faq_path = os.path.join("data", "sample_faqs.json")
    if not os.path.exists(faq_path):
        print(f"❌ Error: {faq_path} not found!")
        return

    with open(faq_path, "r") as f:
        faqs = json.load(f)
        
    documents = []
    for faq in faqs:
        doc = {
            "id": faq["id"],
            "text": f"Question: {faq['question']}\nAnswer: {faq['answer']}",
            "metadata": {"category": faq["category"]}
        }
        documents.append(doc)
        
    print(f"📄 Found {len(documents)} FAQs. Adding to Vector DB...")
    vector_db.add_documents(documents)
    print("✅ Ingestion Complete!")

if __name__ == "__main__":
    ingest_faqs()
