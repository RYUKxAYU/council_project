import time
from src.council.application.graph_builder import build_graph
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

MAX_ROUNDS = 100
MAX_TIME = 3600  # 1 hour

def run_debate(user_input: str):
    """
    Run the council debate system.
    
    The graph will handle routing between chair and personas.
    Chair decides when to call each speaker or finish.
    """
    app = build_graph()
    state = {
        "messages": [HumanMessage(content=user_input)],
        "next_speaker": "chair",
        "current_round": 0,
        "final_verdict": None,
        "start_time": time.time()
    }

    # Run the debate - the graph will handle routing and stopping conditions
    for round_num in range(MAX_ROUNDS):
        # Update round counter
        state["current_round"] = round_num
        
        # Check timeout
        elapsed = time.time() - state["start_time"]
        if elapsed > MAX_TIME:
            print(f"⏱️  Time limit exceeded ({elapsed:.0f}s). Ending debate.")
            return "Debate timed out before reaching consensus."
        
        # Let the graph process the next step
        state = app.invoke(state)
        
        # Check if we have a final verdict
        if state.get("final_verdict"):
            break
    
    # Return the final verdict or a timeout message
    return state.get("final_verdict") or "Debate reached maximum rounds without consensus."

if __name__ == "__main__":
    print("=" * 60)
    print("🏛️  Council Debate System Online")
    print("=" * 60)
    query = input("\n❓ Enter your question: ")
    print("\n" + "=" * 60)
    print("⚙️  Starting debate...")
    print("=" * 60 + "\n")
    
    verdict = run_debate(query)
    
    print("\n" + "=" * 60)
    print("📋 Final Verdict:")
    print("=" * 60)
    print(verdict if verdict else "No verdict reached.")
    print("=" * 60)
