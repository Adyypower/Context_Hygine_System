import sys
import os

# Add the project root to python path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.hygiene import ContextHygieneController
import json

def run_verification():
    print("Initializing Context Hygiene Controller...")
    controller = ContextHygieneController()
    
    # Mock Context: A conversation about Neural Networks
    mock_context = [
        "User: Explain backpropagation.",
        "AI: Backpropagation is an algorithm for supervised learning of artificial neural networks using gradient descent. given an artificial neural network and an error function, the method calculates the gradient of the error function with respect to the neural network's weights.",
        "User: How does the learning rate affect it?",
        "AI: The learning rate is a hyperparameter that controls how much to change the model in response to the estimated error each time the model weights are updated. A learning rate that is too small may result in a long training process and the possibility of getting stuck, while a value that is too large may result in learning a sub-optimal set of weights too fast or an unstable training process.",
        "User: What are some common optimizers?",
        "AI: Common optimizers include SGD, Adam, and RMSprop. Adam is widely used because it adapts the learning rate for each parameter."
    ]
    
    print("\n------------------------------------------------")
    print("Test Case 1: Relevant Query (Low compression expected)")
    print("------------------------------------------------")
    query_relevant = "Tell me more about Adam optimizer."
    result_relevant = controller.optimize_context(mock_context, query_relevant, max_token_threshold=500)
    
    print(f"Tokens Before: {result_relevant.tokens_before}")
    print(f"Tokens After: {result_relevant.tokens_after}")
    print(f"Compression: {result_relevant.compression_level}")
    print(f"Drift Detected: {result_relevant.drift_detected}")
    print(f"Optimized Context:\n{result_relevant.optimized_context}")

    print("\n------------------------------------------------")
    print("Test Case 2: Context Drift (Drift detection expected)")
    print("------------------------------------------------")
    query_drift = "What is the recipe for chocolate cake?"
    result_drift = controller.optimize_context(mock_context, query_drift, max_token_threshold=500)
    
    print(f"Tokens Before: {result_drift.tokens_before}")
    print(f"Tokens After: {result_drift.tokens_after}")
    print(f"Compression: {result_drift.compression_level}")
    print(f"Drift Detected: {result_drift.drift_detected}")
    print(f"Optimized Context (Should be pruned):\n{result_drift.optimized_context}")

if __name__ == "__main__":
    run_verification()
