from src.incident_agents.config import llm
from src.incident_agents.state import AgentState
from src.incident_agents.tools.reporting_tools import save_incident_report

def report_node(state: AgentState):
    """
    Generates structured incident reports and action plans.
    """
    print("---GENERATING FINAL REPORT---")
    
    # Gather all context from the state
    threats = state.get("detected_threats", [])
    risk = state.get("risk_score", 0)
    
    prompt = f"""
    You are a Lead Incident Responder. Based on these findings:
    - Threats: {threats}
    - Risk Score: {risk}/100
    
    Generate a professional Markdown Incident Report including:
    1. Executive Summary
    2. Detailed Findings (mapped to MITRE ATT&CK if possible)
    3. Recommended Action Plan (Immediate containment steps)
    """
    
    # Reasoning step with Groq
    report_content = llm.invoke(prompt).content
    
    # Acting step: Save the report using our tool
    save_incident_report.invoke(report_content)
    
    return {
        "incident_report": report_content,
        "next_step": "end"
    }