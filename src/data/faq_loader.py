"""
FAQ Data Loader
Loads FAQ dataset from JSON/CSV and populates Vector DB
"""
import json
import csv
import os
from typing import List, Dict, Any
from src.services.retriever import vector_db
import logging

logger = logging.getLogger(__name__)

def load_faqs_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Load FAQs from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def process_and_index_faqs(faqs: List[Dict[str, Any]]):
    """
    Process FAQs and add to vector DB
    Format:
    {
        "id": "...",
        "question": "...",
        "answer": "...",
        "category": "..."
    }
    """
    documents = []
    for faq in faqs:
        # Create a text representation for embedding
        # We assume the user searches for the question or content related to the answer
        text = f"Question: {faq['question']}\nAnswer: {faq['answer']}"
        
        doc = {
            "id": faq.get("id"),
            "text": text,
            "metadata": {
                "category": faq.get("category"),
                "question": faq.get("question"),
                "answer": faq.get("answer")
            }
        }
        documents.append(doc)
    
    if documents:
        vector_db.add_documents(documents)
        logger.info(f"Successfully indexed {len(documents)} FAQs")

def load_sample_data(sample_path: str = "./data/sample_faqs.json"):
    """Load sample data if exists"""
    if os.path.exists(sample_path):
        logger.info(f"Loading sample data from {sample_path}")
        faqs = load_faqs_from_json(sample_path)
        process_and_index_faqs(faqs)
    else:
        logger.warning(f"Sample data file not found: {sample_path}")
