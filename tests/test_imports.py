import importlib
import pytest


def test_graph_import_and_state_shape(monkeypatch):
    pytest.importorskip("langgraph")
    pytest.importorskip("langchain_groq")
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    graph = importlib.import_module("src.incident_agents.graph")
    state = importlib.import_module("src.incident_agents.state")

    assert hasattr(graph, "app")
    assert "logs_csv_path" in state.AgentState.__annotations__
