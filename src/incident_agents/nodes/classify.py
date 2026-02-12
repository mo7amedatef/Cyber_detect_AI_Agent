import json
import re
from src.incident_agents.config import llm
from src.incident_agents.state import AgentState
from src.incident_agents.tools.detection_tools import load_threat_intel

def _parse_risk_score_from_response(response_text: str) -> int:
    """Extract risk score (0-100) from LLM response. Falls back to 50 if unparseable."""
    # Try explicit JSON block first
    json_match = re.search(r"\{[^{}]*\"risk_score\"\s*:\s*(\d+)[^{}]*\}", response_text, re.DOTALL | re.IGNORECASE)
    if json_match:
        try:
            val = int(json_match.group(1))
            return max(0, min(100, val))
        except ValueError:
            pass
    # Try "Risk Score: N" or "score: N"
    for pattern in [r"risk\s*score\s*[:\s]+(\d+)", r"score\s*[:\s]+(\d+)", r"(\d+)\s*/\s*100"]:
        match = re.search(pattern, response_text, re.IGNORECASE)
        if match:
            try:
                val = int(match.group(1))
                return max(0, min(100, val))
            except ValueError:
                continue
    return 50

def classify_node(state: AgentState):
    """
    Assesses risk levels and enriches findings with context from threat intelligence.
    """
    print("---RISK CLASSIFICATION & ENRICHMENT---")
    
    threats = state.get("detected_threats", [])
    intel = load_threat_intel()
    
    prompt = f"""
    You are a Cybersecurity Risk Assessor. Evaluate these findings:
    {threats}
    
    Threat intelligence context (use to enrich assessment):
    {intel}
    
    Task:
    1. Assign a Risk Score (0-100).
    2. Classify the priority: LOW, MEDIUM, HIGH, or CRITICAL.
    3. Determine if this matches a specific MITRE ATT&CK technique.
    
    Provide the output in structured JSON format with a "risk_score" field (number 0-100).
    """
    
    response = llm.invoke(prompt)
    response_text = response.content if hasattr(response, "content") else str(response)
    risk_score = _parse_risk_score_from_response(response_text)
    
    return {
        "risk_score": risk_score,
        "next_step": "report"
    }