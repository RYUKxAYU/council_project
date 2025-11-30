# src/council/infrastructure/llm_factory.py

# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_ibm import WatsonxLLM
# from langchain_groq import ChatGroq
# from langchain_anthropic import ChatAnthropic
import os

"""
Make sure you have these API keys in .env:

OPENAI_API_KEY=
GOOGLE_API_KEY=
IBM_WATSONX_APIKEY=
ANTHROPIC_API_KEY=
GROQ_API_KEY=
"""

# -----------------------------
# CHAIRPERSON → Gemini 2.0 (Low Temperature)
# -----------------------------
def get_chair_model():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-pro-exp",
        temperature=0.2,
        api_key=os.getenv("GOOGLE_API_KEY")
    )


# -----------------------------
# VISIONARY → Gemini 2.0 (High Temperature)
# -----------------------------
def get_visionary_model():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-pro-exp",
        temperature=0.8,
        api_key=os.getenv("GOOGLE_API_KEY")
    )


# -----------------------------
# SKEPTIC → Gemini 2.0 (Very Low Temperature)
# -----------------------------
def get_skeptic_model():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-pro-exp",
        temperature=0.1,
        api_key=os.getenv("GOOGLE_API_KEY")
    )


# -----------------------------
# STRATEGIST → Gemini 2.0 (Medium Temperature)
# -----------------------------
def get_strategist_model():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-pro-exp",
        temperature=0.3,
        api_key=os.getenv("GOOGLE_API_KEY")
    )


# -----------------------------
# FINAL VERDICT → Gemini 2.0 (Very Low Temperature)
# -----------------------------
def get_decision_model():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-pro-exp",
        temperature=0.1,
        api_key=os.getenv("GOOGLE_API_KEY")
    )
