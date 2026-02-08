from src.incident_agents.state import AgentState

def ingest_node(state: AgentState):
    print("---INGESTING LOGS---")
    raw_input = state.get("raw_data", "")
    # Logic to validate or format the data goes here
    return {"logs": [f"Validated: {raw_input}"], "next_step": "detect"}