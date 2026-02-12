from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from src.incident_agents.config import llm
from src.incident_agents.state import AgentState
from src.incident_agents.tools.detection_tools import cyber_tools

llm_with_tools = llm.bind_tools(cyber_tools)
MAX_DETECT_STEPS = 6

def _tool_by_name(name: str):
    for t in cyber_tools:
        if t.name == name:
            return t
    return None

def detect_node(state: AgentState):
    """
    ReAct-style detect agent: reasons and acts using tools (query_security_logs, check_ip_reputation).
    """
    print("---THREAT DETECTION REASONING---")
    logs_context = state.get("logs", [])
    logs_csv_path = state.get("logs_csv_path")

    prompt = f"""
    You are a Senior Cyber Analyst. Analyze the following for brute force attempts or suspicious IPs.
    Use the tools: query_security_logs to search logs, and check_ip_reputation to check any IPs you find.

    Current findings in state: {logs_context}
    """
    messages = [HumanMessage(content=prompt)]
    tool_results: list[str] = []
    step = 0

    while step < MAX_DETECT_STEPS:
        step += 1
        response = llm_with_tools.invoke(messages)
        if not getattr(response, "tool_calls", None):
            break
        messages.append(response)
        for tc in response.tool_calls:
            name = tc.get("name") if isinstance(tc, dict) else getattr(tc, "name", None)
            args = tc.get("args") if isinstance(tc, dict) else getattr(tc, "args", {}) or {}
            tc_id = tc.get("id") if isinstance(tc, dict) else getattr(tc, "id", str(step))
            if not name:
                continue
            tool_fn = _tool_by_name(name)
            if not tool_fn:
                messages.append(ToolMessage(content=f"Unknown tool: {name}", tool_call_id=tc_id))
                continue
            if name == "query_security_logs" and logs_csv_path and "csv_path" not in args:
                args = {**args, "csv_path": logs_csv_path}
            try:
                result = tool_fn.invoke(args)
                tool_results.append(str(result))
                messages.append(ToolMessage(content=str(result), tool_call_id=tc_id))
            except Exception as e:
                tool_results.append(f"Tool error: {e}")
                messages.append(ToolMessage(content=f"Error: {e}", tool_call_id=tc_id))

    content = getattr(response, "content", "") or ""
    if tool_results:
        content += "\n\nTool findings:\n" + "\n".join(tool_results)
    return {
        "detected_threats": [{"analysis": content}],
        "next_step": "classify",
    }