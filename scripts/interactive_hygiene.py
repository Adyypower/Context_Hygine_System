import sys
import os
import json

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.hygiene import ContextHygieneController

def main():
    print("Initializing Context Hygiene Controller...")
    try:
        controller = ContextHygieneController()
        print("Controller initialized successfully.")
    except Exception as e:
        print(f"Error initializing controller: {e}")
        return

    print("\n--- Interactive Context Hygiene Test ---")
    print("Enter 'exit' to quit.")

    while True:
        try:
            print("\n-------------------------------------------")
            query = input("Enter new query (or 'exit'): ").strip()
            if query.lower() == 'exit':
                break
            
            print("Enter raw context messages. Separate multiple messages with '|'.")
            raw_context_input = input("Raw Context: ").strip()
            
            if not raw_context_input:
                raw_context = []
                print("Context empty.")
            else:
                # Split by pipe for simple multi-message simulation
                raw_context = [msg.strip() for msg in raw_context_input.split("|")]
                print(f"Context loaded with {len(raw_context)} messages.")
            
            threshold_str = input("Enter max token threshold (default 2000): ").strip()
            try:
                threshold = int(threshold_str) if threshold_str else 2000
            except ValueError:
                print("Invalid threshold. Using default 2000.")
                threshold = 2000

            print(f"\nProcessing query: '{query}' with context size {len(raw_context)}...")
            result = controller.optimize_context(raw_context, query, max_token_threshold=threshold)
            
            # Convert result to dict for pretty printing
            result_dict = result.model_dump()
            print("\n--- Hygiene Output (JSON) ---")
            print(json.dumps(result_dict, indent=2))
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error during processing: {e}")

if __name__ == "__main__":
    main()
