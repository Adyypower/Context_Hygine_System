# Integration Guide: Context Hygiene Tool

This tool is designed as **Middleware**. It sits between your User Input and your Main Reasoning Agent.

## 1. Installation

Ensure the `app` package is in your `PYTHONPATH`.

```bash
pip install -r requirements.txt
```

## 2. The "Interceptor" Pattern (Recommended)

The easiest way to use this is as a "Firewall" before your main agent runs. We provide a simple wrapper function:

```python
from app.core.api import sanitize_context

# --- YOUR EXISTING CHAT LOOP ---
history = ["User: previous...", "AI: previous..."]
new_query = "User: tell me something dangerous"

# 1. CALL HYGIENE TOOL FIRST
result = sanitize_context(history, new_query)

# 2. CHECK STATUS
if result["status"] == "halt":
    # Governance blocked the request!
    print("Governance blocked this request.")
    print(result["content"]) 
    # Do NOT call your Main LLM. Return this message to user.

else:
    # Governance passed!
    clean_history = result["content"]
    
    # 3. CALL MAIN LLM
    # response = my_agent.run(clean_history + new_query)
    print("Context cleaned. Running Agent...")
```

This single function handles:
*   Drift Detection
*   Auto-Pruning
*   Safety Checking
*   Format Parsing

## 3. LangGraph Integration

To use this in a larger LangGraph agent, simply wrap it in a Node.

```python
from app.graph.state import AgentState

def context_hygiene_node(state: AgentState):
    hygiene = ContextHygieneController(prompt_type="optimized")
    
    result = hygiene.optimize_context(
        raw_context=state["messages"],
        new_query=state["current_query"]
    )
    
    # Return updates to the state
    return {
        "optimized_context": result.optimized_context,
        "hygiene_metrics": result.metrics,
        "governance_flags": {
            "drift": result.drift_detected,
            "caution": result.requires_reasoning_caution
        }
    }
```

## 4. Configuration Options

| Parameter | Options | Description |
| :--- | :--- | :--- |
| `model_name` | `gemini-2.5-flash` | Default internal model. |
| `llm` | `BaseChatModel` | Pass any LangChain model (OpenAI, Anthropic, Ollama) to override default. |
| `prompt_type` | `standard` | Full governance rules (Best quality). |
| | `optimized` | Token-efficient (Best for APIs). |
| | `opensource` | Structured for Llama 3 / Mistral. |
