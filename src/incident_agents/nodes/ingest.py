import tempfile
import os
from src.incident_agents.state import AgentState

def _looks_like_csv(text: str) -> bool:
    """Heuristic: has commas and newlines and no obvious non-CSV content."""
    if not text or len(text.strip()) < 10:
        return False
    lines = text.strip().splitlines()
    if len(lines) < 1:
        return False
    first = lines[0]
    return "," in first and len(first) < 500

def ingest_node(state: AgentState):
    print("---INGESTING LOGS---")
    raw_input = state.get("raw_data", "")
    out: dict = {"logs": [f"Validated: {raw_input}"], "next_step": "detect"}

    # If input looks like CSV (e.g. uploaded file), write to temp file so detect tools can use it
    if _looks_like_csv(raw_input):
        try:
            fd, path = tempfile.mkstemp(suffix=".csv", prefix="cyber_detect_")
            with os.fdopen(fd, "w") as f:
                f.write(raw_input)
            out["logs_csv_path"] = path
        except Exception:
            pass
    return out