"""Step 1 Baseline Agent for VoiceOps 2026."""
from typing import Dict, Any
from .llm_adapter import LLMAdapter

BASELINE_SYSTEM_PROMPT = """You are an AI customer support assistant for ZentroMart, an Indian online shopping store.
Always identify yourself as an AI assistant.
Answer customer questions to the best of your general knowledge without internal documents.
"""


class BaselineAgent:
    def __init__(self, llm: LLMAdapter = None):
        self.llm = llm or LLMAdapter()

    def answer_question(self, question: str) -> Dict[str, Any]:
        response, source = self.llm.generate(prompt=question, system_prompt=BASELINE_SYSTEM_PROMPT, context=None)
        decision = "answer"
        return {'question': question, 'response': response, 'decision': decision, 'retrieved_sections': [], 'source': source, 'has_retrieval': False}
