import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from app.core.models import HygieneOutput
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

class ContextHygieneController:
    def __init__(self, llm=None, model_name: str = "gemini-2.5-flash", prompt_type: str = "standard"):
        """
        Initialize the Context Hygiene Controller.
        
        Args:
            llm: Optional LangChain ChatModel instance.
            model_name: Default Gemini model.
            prompt_type: "standard" (Master), "optimized" (API), or "opensource" (Llama/Mistral).
        """
        # Select prompt file
        prompt_map = {
            "standard": "context_hygiene_controller.txt",
            "optimized": "context_hygiene_optimized.txt",
            "opensource": "context_hygiene_opensource.txt"
        }
        filename = prompt_map.get(prompt_type, "context_hygiene_controller.txt")
        
        prompt_path = Path(__file__).parent.parent.parent / "prompts" / filename
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

        print(f"Debug: Loaded Governance Prompt Strategy: {prompt_type}")

        if llm:
            self.llm = llm
            print(f"Debug: Using provided external LLM: {type(llm).__name__}")
            return

        # Fallback to default internal Gemini setup
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print(f"Debug: Environment file looked for at {env_path}")
            print(f"Debug: Current working directory: {os.getcwd()}")
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
            
        api_key = api_key.strip()
        
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=0.0  # Deterministic behavior
            )
        except Exception:
            raise

    def optimize_context(self, raw_context: list[str], new_query: str, max_token_threshold: int = 2000) -> HygieneOutput:
        """
        Optimizes the given context based on the user query and token threshold.

        Args:
            raw_context: List of strings representing the conversation history.
            new_query: The new user query.
            max_token_threshold: The maximum allowed token count.

        Returns:
            HygieneOutput: The structured optimization result.
        """
        
        # Construct the full prompt
        # We use SystemMessage for the system prompt to avoid template parsing of the JSON examples
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=self.system_prompt),
            ("human", "Here is the input:\n\nRaw Context: {raw_context}\n\nNew Query: {new_query}\n\nMax Token Threshold: {max_token_threshold}")
        ])
        
        # Create the chain with structured output
        chain = prompt | self.llm.with_structured_output(HygieneOutput)
        
        # Execute the chain
        result = chain.invoke({
            "raw_context": raw_context,
            "new_query": new_query,
            "max_token_threshold": max_token_threshold
        })
        
        return result
