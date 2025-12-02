# 🏛️ Council Debate System

The **Council Debate System** is an advanced multi-agent AI application designed to facilitate structured debates on complex topics. Built using **LangGraph** and **LangChain**, it simulates a council of distinct personas who debate, critique, and refine ideas to reach a well-rounded verdict.

## 🌟 Features

-   **Multi-Agent Architecture**: Orchestrates interactions between specialized AI agents.
-   **Distinct Personas**:
    -   **Chairperson**: Moderates the discussion and routes the conversation.
    -   **Orion (The Visionary)**: Proposes futuristic and unconstrained ideas.
    -   **Cipher (The Skeptic)**: Identifies risks, flaws, and critical weaknesses.
    -   **Marcus (The Strategist)**: Develops practical MVP plans and execution strategies.
-   **Dynamic Routing**: The debate flow is dynamically managed by the Chairperson based on the context of the conversation.
-   **Consensus Mechanism**: Includes logic to check for agreement among council members (configurable).
-   **Timeout & Round Limits**: Ensures debates conclude within a specified time or number of rounds.

## 🏗️ Architecture

The system is built on a state graph where each node represents an agent or a process:

1.  **State**: Shared context containing the message history, current speaker, round count, and final verdict.
2.  **Nodes**: Python functions defining the behavior of each agent.
3.  **Edges**: Routing logic determined by the Chairperson or system constraints (e.g., timeout).

## 📂 Project Structure

```
council_project/
├── main.py                 # Entry point for the application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API keys)
├── src/
│   └── council/
│       ├── application/
│       │   ├── graph_builder.py  # Defines the LangGraph workflow
│       │   └── nodes.py          # Implementation of agent nodes
│       ├── core/
│       │   ├── personas.py       # Persona definitions
│       │   └── state.py          # State schema definition
│       └── infrastructure/
│           └── llm_factory.py    # LLM initialization logic
```

## 🚀 Getting Started

### Prerequisites

-   Python 3.10+
-   API Keys for the LLMs you intend to use (e.g., OpenAI, Anthropic, Google Gemini).

### Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  Create a `.env` file in the root directory.
2.  Add your API keys. The required keys depend on the models configured in `src/council/infrastructure/llm_factory.py`.
    ```env
    OPENAI_API_KEY=sk-...
    # Add other keys as needed (e.g., ANTHROPIC_API_KEY, GOOGLE_API_KEY)
    ```

## 🏃 Usage

Run the main script to start the council:

```bash
python main.py
```

1.  The system will initialize and prompt you for a question.
2.  **Enter your query**: e.g., "Should we adopt a 4-day work week?"
3.  Watch as the council members (Visionary, Skeptic, Strategist) debate the topic under the Chairperson's moderation.
4.  The system will output a **Final Verdict** summarizing the decision.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.