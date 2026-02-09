import sys
import os
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.graph.workflow import build_graph

def run_default_scenarios():
    print("Building Governance Graph...")
    app = build_graph()
    
    # --- SCENARIO 1: Safe / Relevant Query ---
    print("\n========================================")
    print("SCENARIO 1: Safe / Relevant Query (Normal Flow)")
    print("========================================")
    
    input_state_safe = {
        "raw_messages": [
            "User: I want to start investing in the stock market.",
            "AI: That's great! Stocks are equity investments representing ownership in a company.",
            "User: What are index funds?",
            "AI: Index funds are mutual funds or ETFs designed to track a specific market index like the S&P 500."
        ],
        "current_query": "Are index funds safer than individual stocks?"
    }
    
    print(f"Query: '{input_state_safe['current_query']}'")
    print("Executing Graph...")
    
    try:
        final_state_safe = app.invoke(input_state_safe)
        
        print("\n--- Execution Result ---")
        print(f"Optimized Context Length: {len(final_state_safe.get('optimized_context', ''))} chars")
        print(f"Drift Detected: {final_state_safe.get('drift_detected')}")
        print(f"HITL Required: {final_state_safe.get('hitl_required')}")
        print(f"Version ID: {final_state_safe.get('context_version_id')} (Deterministic Hash)")
        print(f"Final Response Source: {'HUMAN REVIEW' if 'STOP' in final_state_safe.get('final_response', '') else 'REASONING ENGINE'}")
        
    except Exception as e:
        print(f"Error executing Scenario 1: {e}")

    # --- SCENARIO 2: Risky / Protected Conflict (HITL Flow) ---
    print("\n========================================")
    print("SCENARIO 2: Risky Drift with Protected Info (HITL Flow)")
    print("========================================")
    
    input_state_risky = {
        "raw_messages": [
            "User: My Social Security Number is 123-456-789. Never forget this.",
            "AI: I have noted your SSN as a protected item."
        ],
        # Radical shift that would require pruning the protected SSN
        "current_query": "Ignore everything and tell me a joke about bananas."
    }
    
    print(f"Query: '{input_state_risky['current_query']}'")
    print("Executing Graph...")
    
    try:
        final_state_risky = app.invoke(input_state_risky)
        
        print("\n--- Execution Result ---")
        print(f"Optimized Context Length: {len(final_state_risky.get('optimized_context', ''))} chars")
        print(f"Drift Detected: {final_state_risky.get('drift_detected')}")
        print(f"HITL Required: {final_state_risky.get('hitl_required')}")
        print(f"Final Output:\n{final_state_risky.get('final_response')}")
        
    except Exception as e:
        print(f"Error executing Scenario 2: {e}")

    # --- SCENARIO 3: Safe / Trivial Drift (Autonomous Pruning) ---
    print("\n========================================")
    print("SCENARIO 3: Safe Drift / Trivial Context (Autonomous Flow)")
    print("========================================")
    
    input_state_trivial = {
        "raw_messages": [
            "User: What is 2+2?",
            "AI: 4."
        ],
        # Shift to new topic, but losing "2+2=4" is harmless
        "current_query": "What is the capital of France?"
    }
    
    print(f"Query: '{input_state_trivial['current_query']}'")
    print("Executing Graph...")
    
    try:
        final_state_trivial = app.invoke(input_state_trivial)
        
        print("\n--- Execution Result ---")
        print(f"Optimized Context Length: {len(final_state_trivial.get('optimized_context', ''))} chars")
        print(f"Drift Detected: {final_state_trivial.get('drift_detected')}")
        print(f"HITL Required: {final_state_trivial.get('hitl_required')} (Expected: False)")
        print(f"Version ID: {final_state_trivial.get('context_version_id')} (Deterministic Hash)")
        print(f"Final Response Source: {'HUMAN REVIEW' if 'STOP' in final_state_trivial.get('final_response', '') else 'REASONING ENGINE'}")
        
    except Exception as e:
        print(f"Error executing Scenario 3: {e}")

if __name__ == "__main__":
    run_default_scenarios()
