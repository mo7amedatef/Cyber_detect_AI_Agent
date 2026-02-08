from langgraph.graph import StateGraph, START, END
from src.incident_agents.state import AgentState
from src.incident_agents.nodes.ingest import ingest_node
from src.incident_agents.nodes.detect import detect_node
from src.incident_agents.nodes.classify import classify_node
from src.incident_agents.nodes.report import report_node

workflow = StateGraph(AgentState)

# Define all nodes
workflow.add_node("ingest", ingest_node)
workflow.add_node("detect", detect_node)
workflow.add_node("classify", classify_node)
workflow.add_node("report", report_node)

# Build the pipeline flow
workflow.add_edge(START, "ingest")
workflow.add_edge("ingest", "detect")
workflow.add_edge("detect", "classify")
workflow.add_edge("classify", "report")
workflow.add_edge("report", END)

# Compile the final system
app = workflow.compile()