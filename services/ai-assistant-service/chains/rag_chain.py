"""
RAG chain using LangChain.
Retrieves user context and constructs a grounded prompt for the LLM.
This module is the ONLY place LangChain is imported in the application layer.
"""
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from domain.models import UserContext, AIResponse
from domain.ports import AIProviderPort
from infrastructure.prompt_loader import get_system_prompt, render_user_prompt


def _build_context_string(context: Optional[UserContext]) -> str:
    if context is None:
        return "No user context available."
    return context.as_context_string()


async def run_rag_chain(
    question: str,
    provider: AIProviderPort,
    context: Optional[UserContext] = None,
    history: str = "",
    prompt_version: str = "v1",
) -> AIResponse:
    """
    Augments the user question with retrieved context (Music DNA, mood, history)
    and runs it through the configured LLM provider.
    """
    context_str = _build_context_string(context)
    system = get_system_prompt("query", prompt_version)
    user_prompt = render_user_prompt(
        "query",
        version=prompt_version,
        context=context_str,
        history=history or "No prior conversation.",
        question=question,
    )
    return await provider.complete(prompt=user_prompt, system=system)
