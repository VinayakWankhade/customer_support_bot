"""
Prompt Orchestrator Service
Constructs the final prompt for the LLM using context and templates
"""
import json
from typing import List, Dict, Any, Optional
from src.prompts.prompts import SYSTEM_PROMPT, RAG_PROMPT_TEMPLATE
from src.services.retriever import vector_db
from src.models.schemas import MessageResponse

class PromptOrchestrator:
    def __init__(self):
        pass

    async def build_prompt(
        self,
        user_message: str,
        chat_history: List[MessageResponse],
        session_summary: str = "No previous summary."
    ) -> str:
        """
        Construct the complete prompt with RAG context
        """
        # 1. Retrieve relevant documents
        # For a production app, we might rewrite the query based on history here
        retrievals = vector_db.search(user_message, k=3)
        
        # 2. Format retrieved context
        if retrievals:
            context_str = "\n".join(
                [f"{i+1}) [{doc.get('id', 'unknown')}] {doc['text']}" 
                 for i, doc in enumerate(retrievals)]
            )
        else:
            context_str = "No relevant documents found."
            
        # 3. Format chat history (last 5 messages)
        recent_history = chat_history[-5:] if chat_history else []
        history_str = "\n".join(
            [f"{msg.role.capitalize()}: {msg.content}" for msg in recent_history]
        )
        
        # 4. Fill template
        prompt = RAG_PROMPT_TEMPLATE.format(
            system_prompt=SYSTEM_PROMPT,
            session_summary=session_summary,
            retrieved_context=context_str,
            chat_history=history_str,
            user_query=user_message
        )
        
        return prompt, retrievals

    def parse_llm_response(self, llm_text: str) -> Dict[str, Any]:
        """
        Parse JSON response from LLM, handling potential formatting issues
        """
        try:
            # Clean markdown code blocks if present
            clean_text = llm_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            
            return json.loads(clean_text)
        except json.JSONDecodeError:
            # Fallback if LLM fails to output valid JSON
            return {
                "answer_text": llm_text,
                "confidence": 0.5,
                "sources": [],
                "next_action": "reply",
                "action_payload": {}
            }

# Global instance
orchestrator = PromptOrchestrator()
