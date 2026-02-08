from src.incident_agents.graph import app
from src.incident_agents.state import AgentState

def run_simulation():
    """
    Simulates a Brute Force Attack scenario to test the multi-agent system.
    """
    print("🚀 Starting Cyber Detect AI Simulation...")

    # Define a realistic threat scenario
    initial_input = """
    CRITICAL ALERT: Multiple failed login attempts detected.
    Source IP: 192.168.1.50
    Target: Admin_Portal_01
    Timestamp: 2026-02-08T02:15:00
    Event: 5 failed attempts in 30 seconds followed by a successful login.
    """

    # Initialize the state with our raw log data
    initial_state: AgentState = {
        "raw_data": initial_input,
        "logs": [],
        "detected_threats": [],
        "risk_score": 0,
        "incident_report": "",
        "next_step": ""
    }

    # Execute the LangGraph pipeline
    final_output = app.invoke(initial_state)

    print("\n" + "="*50)
    print("📋 FINAL INCIDENT REPORT SUMMARY")
    print("="*50)
    print(f"Risk Score: {final_output.get('risk_score')}/100")
    print("\n--- Report Content ---")
    print(final_output.get('incident_report'))
    print("="*50)

if __name__ == "__main__":
    run_simulation()