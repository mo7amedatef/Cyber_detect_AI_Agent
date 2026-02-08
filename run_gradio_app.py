import gradio as gr
from src.incident_agents.graph import app

def process_incident(raw_log_input):
    """
    Triggers the LangGraph workflow from the Gradio UI.
    """
    # Initial state initialization
    initial_state = {
        "raw_data": raw_log_input,
        "logs": [],
        "detected_threats": [],
        "risk_score": 0,
        "incident_report": "",
        "next_step": ""
    }
    
    # Run the graph
    result = app.invoke(initial_state)
    
    # Return specific outputs to display in the UI
    return (
        result.get("risk_score", 0),
        result.get("incident_report", "No report generated."),
        f"Analysis completed. Threats detected: {len(result.get('detected_threats', []))}"
    )

# --- Gradio UI Layout ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛡️ Cyber Detect AI - Incident Response Dashboard")
    gr.Markdown("Input security logs below to trigger the multi-agent detection pipeline.")
    
    with gr.Row():
        with gr.Column(scale=1):
            log_input = gr.Textbox(
                label="Raw Security Logs", 
                placeholder="Paste logs here (e.g., failed logins, SSH errors...)",
                lines=10
            )
            submit_btn = gr.Button("Analyze Incident", variant="primary")
            
        with gr.Column(scale=1):
            risk_gauge = gr.Number(label="Calculated Risk Score (0-100)")
            status_output = gr.Label(label="System Status")
            
    report_display = gr.Markdown(label="Final Incident Report")

    # Connect the button to the logic
    submit_btn.click(
        fn=process_incident,
        inputs=log_input,
        outputs=[risk_gauge, report_display, status_output]
    )

if __name__ == "__main__":
    demo.launch()