from langgraph.graph import StateGraph
from ..core.state import CouncilState
from .nodes import (
    chair_node,
    visionary_node,
    skeptic_node,
    strategist_node,
    consensus_check_node,
    final_verdict_node,
)


def router(state):
    """ok
    Determines next node based on chair decision.
    """
    next_speaker = state.get("next_speaker", "FINISH")

    if next_speaker == "Orion":
        return "visionary"
    if next_speaker == "Cipher":
        return "skeptic"
    if next_speaker == "Marcus":
        return "strategist"
    if next_speaker == "FINISH":
        return "final_verdict"

    return "final_verdict"


def build_graph():
    workflow = StateGraph(CouncilState)

    # Add nodes
    workflow.add_node("chair", chair_node)
    workflow.add_node("visionary", visionary_node)
    workflow.add_node("skeptic", skeptic_node)
    workflow.add_node("strategist", strategist_node)
    workflow.add_node("consensus", consensus_check_node)
    workflow.add_node("final_verdict", final_verdict_node)

    workflow.set_entry_point("chair")

    # Chair decides where to go (visionary, skeptic, strategist, or FINISH)
    workflow.add_conditional_edges("chair", router)

    # After each agent speaks → go back to chair for next decision
    workflow.add_edge("visionary", "chair")
    workflow.add_edge("skeptic", "chair")
    workflow.add_edge("strategist", "chair")

    # Consensus routing (not used in current flow but kept for future)
    # workflow.add_conditional_edges("consensus", router)

    app = workflow.compile()
    return app
