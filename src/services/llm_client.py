"""
LLM Client to interact with Google Gemini API
"""
import google.generativeai as genai
from typing import AsyncGenerator, Dict, Any, List, Optional
from src.config import settings
import logging

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        """Initialize Gemini client"""
        self._model = None
        self._generation_config = None

    @property
    def model(self):
        """Lazy load Gemini model"""
        if self._model is None:
            if not settings.gemini_api_key or "your_gemini_api_key" in settings.gemini_api_key:
                logger.warning("Invalid or missing Gemini API key")
            
            genai.configure(api_key=settings.gemini_api_key)
            self._model = genai.GenerativeModel(settings.llm_model)
            self._generation_config = genai.types.GenerationConfig(
                temperature=settings.llm_temperature,
                max_output_tokens=settings.llm_max_tokens,
            )
        return self._model

    @property
    def generation_config(self):
        if self._generation_config is None:
            # Trigger model load to init config
            _ = self.model
        return self._generation_config

    async def generate_response_stream(
        self, 
        prompt: str,
    ) -> AsyncGenerator[str, None]:
        """
        Generate streaming response from Gemini
        
        Args:
            prompt: The full prompt string
            
        Yields:
            Chunks of generated text
        """
        try:
            response = await self.model.generate_content_async(
                prompt,
                generation_config=self.generation_config,
                stream=True
            )
            
            async for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            yield f"Error: {str(e)}"

    async def generate_response(
        self, 
        prompt: str
    ) -> str:
        """
        Generate complete response (non-streaming)
        """
        try:
            response = await self.model.generate_content_async(
                prompt,
                generation_config=self.generation_config
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise e

    def count_tokens(self, text: str) -> int:
        """Count tokens for text"""
        return self.model.count_tokens(text).total_tokens

# Global LLM client instance
llm_client = LLMClient()
