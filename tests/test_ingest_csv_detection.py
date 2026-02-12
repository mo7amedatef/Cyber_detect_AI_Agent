import os

from src.incident_agents.nodes.ingest import ingest_node


def test_ingest_creates_temp_csv_path_for_csv_like_input():
    state = {
        "raw_data": "timestamp,ip,event\n2026-02-08T02:15:00,192.168.1.50,failed_login",
        "logs": [],
        "detected_threats": [],
        "risk_score": 0,
        "incident_report": "",
        "next_step": "",
    }
    out = ingest_node(state)

    assert out["next_step"] == "detect"
    assert "logs_csv_path" in out
    assert os.path.isfile(out["logs_csv_path"])

    os.remove(out["logs_csv_path"])
