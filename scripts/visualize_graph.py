import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.graph.workflow import build_graph

def main():
    print("Building Graph...")
    app = build_graph()
    
    print("Generating Graph Image...")
    try:
        # Generate PNG binary
        png_data = app.get_graph().draw_mermaid_png()
        
        output_path = "graph_visualization.png"
        with open(output_path, "wb") as f:
            f.write(png_data)
            
        print(f"Graph saved to {os.path.abspath(output_path)}")
        
        # Also print Mermaid synthesis for debugging/text view
        print("\n--- Mermaid Definition ---")
        print(app.get_graph().draw_mermaid())
        
    except Exception as e:
        print(f"Error generating graph image: {e}")
        print("Note: You may need to install graphviz or have internet access for mermaid rendering.")

if __name__ == "__main__":
    main()
