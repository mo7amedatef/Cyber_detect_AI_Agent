from typing import Annotated, List, TypedDict, Union
import operator

class AgentState(TypedDict):
    # Annotated with operator.add allows agents to append findings to the list
    raw_data: str
    logs: Annotated[List[str], operator.add]
    detected_threats: Annotated[List[dict], operator.add]
    risk_score: int
    incident_report: str
    next_step: str # Controls which agent acts next in the graph