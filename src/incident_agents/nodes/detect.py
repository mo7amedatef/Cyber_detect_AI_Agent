from src.incident_agents.config import llm
from src.incident_agents.state import AgentState
from src.incident_agents.tools.detection_tools import cyber_tools

# Bind the tools to Groq so it 'knows' it can call them
llm_with_tools = llm.bind_tools(cyber_tools)

def detect_node(state: AgentState):
    """
    The reasoning core of the Detect Agent.
    """
    print("---THREAT DETECTION REASONING---")
    
    # Simple prompt to guide the LLM's reasoning
    prompt = f"""
    You are a Senior Cyber Analyst. Analyze the following request:
    Analyze the logs for any brute force attempts or suspicious IPs.
    
    Current Findings in State: {state.get('logs', [])}
    """
    
    # Use Groq to determine the next action
    response = llm_with_tools.invoke(prompt)
    
    # In a full LangGraph setup, the 'ToolNode' would execute the tools.
    # For now, we update the state with the LLM's thought process.
    return {
        "detected_threats": [{"analysis": response.content}], 
        "next_step": "classify"
    }