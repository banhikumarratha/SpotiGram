from langchain_community.llms import Ollama
from langchain_core.language_models.llms import BaseLLM
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler

class MockLLM(BaseLLM):
    """Fallback LLM if Ollama is unreachable."""
    @property
    def _llm_type(self) -> str:
        return "mock"
    
    def _generate(self, prompts, **kwargs):
        from langchain_core.outputs import Generation, LLMResult
        generations = [[Generation(text="[Fallback] I am a mock AI DJ. Here is a chill track!")] for _ in prompts]
        return LLMResult(generations=generations)

def get_llm(model_name: str = "llama2") -> BaseLLM:
    """Returns Ollama LLM, or a MockLLM on connection failure."""
    try:
        # Assuming Ollama is on host machine when running in Docker
        llm = Ollama(
            model=model_name,
            base_url="http://host.docker.internal:11434",
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
        )
        # Quick test to see if it responds (could timeout)
        # llm.invoke("test") 
        return llm
    except Exception as e:
        print(f"Warning: Failed to connect to Ollama. Using fallback MockLLM. Error: {e}")
        return MockLLM()
