import time
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from ..infrastructure.llm_factory import (
    get_chair_model,
    get_visionary_model,
    get_skeptic_model,
    get_strategist_model,
)
from ..core.personas import CHAIRPERSON, VISIONARY, SKEPTIC, STRATEGIST


MAX_ROUNDS = 100
MAX_TIME_SECONDS = 3600  # 1 hour


# ------------------------------------------------------------
# Utility: append messages in correct LangChain format
# ------------------------------------------------------------
# ------------------------------------------------------------
# Utility: get last message content safely
# ------------------------------------------------------------
def get_last_content(messages):
    if not messages:
        return None
    msg = messages[-1]
    if isinstance(msg, dict):
        return msg.get("content", "")
    return msg.content

# ------------------------------------------------------------
# Utility: create AIMessage
# ------------------------------------------------------------
def create_ai_message(speaker, content):
    return AIMessage(content=content, name=speaker)



# ------------------------------------------------------------
# CHAIRPERSON NODE
# ------------------------------------------------------------
def chair_node(state):
    """Chair moderates and selects next speaker."""

    model = get_chair_model()
    last_msg = get_last_content(state["messages"]) or "Start the discussion."

    system_prompt = f"""
You are {CHAIRPERSON["name"]}, the council moderator.

Rules:
- Summarize the last speaker briefly.
- Decide the next speaker.
- Do NOT give your own ideas.
- Output exactly one line containing:
  NEXT_SPEAKER: Orion / Cipher / Marcus / FINISH
"""

    full_prompt = system_prompt + "\n\n" + last_msg
    # Use invoke instead of generate_content
    response = model.invoke(full_prompt)
    text = response.content
    
    # Extract NEXT_SPEAKER
    next_speaker = "FINISH"
    for line in text.splitlines():
        if line.strip().startswith("NEXT_SPEAKER"):
            parts = line.split(":")
            if len(parts) > 1:
                next_speaker = parts[1].strip()
            break

    return {
        "next_speaker": next_speaker,
        "messages": [create_ai_message("Chairperson", text)]
    }


# ------------------------------------------------------------
# VISIONARY NODE
# ------------------------------------------------------------
def visionary_node(state):
    model = get_visionary_model()

    system_prompt = f"""
You are {VISIONARY["name"]}.
Directive: {VISIONARY["directive"]}
Respond with futuristic, unconstrained ideation.
"""

    user_msg = get_last_content(state["messages"])

    response = model.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_msg)
    ]).content

    return {"messages": [create_ai_message("Visionary", response)]}


# ------------------------------------------------------------
# SKEPTIC NODE
# ------------------------------------------------------------
def skeptic_node(state):
    model = get_skeptic_model()

    system_prompt = f"""
You are {SKEPTIC["name"]}.
Directive: {SKEPTIC["directive"]}
Identify 2–3 critical flaws or risks.
"""

    user_msg = get_last_content(state["messages"])

    response = model.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_msg)
    ]).content

    return {"messages": [create_ai_message("Skeptic", response)]}


# ------------------------------------------------------------
# STRATEGIST NODE
# ------------------------------------------------------------
def strategist_node(state):
    model = get_strategist_model()

    system_prompt = f"""
You are {STRATEGIST["name"]}.
Directive: {STRATEGIST["directive"]}
Provide an MVP plan, trade-offs, and next-step actions.
"""

    user_msg = get_last_content(state["messages"])

    response = model.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_msg)
    ]).content

    return {"messages": [create_ai_message("Strategist", response)]}


# ------------------------------------------------------------
# CONSENSUS CHECK NODE
# ------------------------------------------------------------
def consensus_check_node(state):
    """
    Ask: "Is everyone agreeing with the decision?"
    If any persona says NO → continue debate.
    """

    now = time.time()

    # Time limit
    if "start_time" in state and state["start_time"] is not None:
        elapsed = now - state["start_time"]
        if elapsed >= MAX_TIME_SECONDS:
            return {
                "final_verdict": "Timeout exceeded. Forced decision.",
                "next_speaker": "FINISH"
            }

    # Round limit
    if state["current_round"] >= MAX_ROUNDS:
        return {
            "final_verdict": "Max rounds exceeded. Forced decision.",
            "next_speaker": "FINISH"
        }

    question = "Is everyone agreeing with the decision?"

    model_map = {
        "Orion (Visionary)": get_visionary_model(),
        "Cipher (Skeptic)": get_skeptic_model(),
        "Marcus (Strategist)": get_strategist_model(),
    }

    decisions = []
    new_messages = []

    for name, model in model_map.items():
        response = model.invoke([
            SystemMessage(content=f"You are {name}. Reply ONLY YES or NO."),
            HumanMessage(content=question)
        ]).content.strip().upper()

        decisions.append((name, response))
        new_messages.append(create_ai_message(name, f"{name} replies: {response}"))

    # If any disagree
    if any(r == "NO" for _, r in decisions):
        next_speaker = "Orion"  # restart debate
    else:
        next_speaker = "FINISH"

    return {
        "next_speaker": next_speaker,
        "messages": new_messages,
        # "final_verdict": ... # We handle timeout above, but here we just route
    }


# ------------------------------------------------------------
# FINAL VERDICT NODE
# ------------------------------------------------------------
def final_verdict_node(state):
    """
    Compile a final decision summary.
    """

    visionary = None
    skeptic = None
    strategist = None

    # Go backwards through the messages and pick the latest from each persona
    for msg in reversed(state["messages"]):
        # Safely get name and content from both dict and object messages
        name = getattr(msg, "name", None) or (msg.get("speaker") if isinstance(msg, dict) else None)
        content = getattr(msg, "content", None) or (msg.get("content") if isinstance(msg, dict) else None)
        
        if name == "Visionary" and visionary is None:
            visionary = content
        if name == "Skeptic" and skeptic is None:
            skeptic = content
        if name == "Strategist" and strategist is None:
            strategist = content
        if visionary and skeptic and strategist:
            break

    final_text = f"""
The decision after debating is:

Visionary (North Star Idea):
{visionary}

Skeptic (Risks / Kill-zones):
{skeptic}

Strategist (MVP Execution Plan):
{strategist}

The council's final decision is:
"{strategist}"
""".strip()

    return {
        "final_verdict": final_text,
        "messages": [create_ai_message("Chairperson", final_text)]
    }
