import importlib
import pytest


def test_gradio_module_imports(monkeypatch):
    pytest.importorskip("gradio")
    pytest.importorskip("langgraph")
    pytest.importorskip("langchain_groq")
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    module = importlib.import_module("run_gradio_app")

    assert hasattr(module, "demo")
    assert hasattr(module, "process_incident")
