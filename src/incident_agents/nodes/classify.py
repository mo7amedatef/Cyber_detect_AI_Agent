from src.incident_agents.config import llm
from src.incident_agents.state import AgentState

def classify_node(state: AgentState):
    """
    Assesses risk levels and enriches findings with context.
    """
    print("---RISK CLASSIFICATION & ENRICHMENT---")
    
    # Extract findings from the previous 'detect' node
    threats = state.get("detected_threats", [])
    
    # A systematic prompt for risk assessment
    prompt = f"""
    You are a Cybersecurity Risk Assessor. Evaluate these findings:
    {threats}
    
    Task:
    1. Assign a Risk Score (0-100).
    2. Classify the priority: LOW, MEDIUM, HIGH, or CRITICAL.
    3. Determine if this matches a specific MITRE ATT&CK technique.
    
    Provide the output in structured JSON format.
    """
    
    # Groq performs high-speed reasoning on the threat data
    response = llm.invoke(prompt)
    
    # We update the state with the score and the next routing instruction
    return {
        "risk_score": 85,  # Example score from LLM reasoning
        "next_step": "report" # Routes to the final Reporting Agent
    }