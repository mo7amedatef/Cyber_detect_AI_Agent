import gradio as gr
import pandas as pd
import os
from src.incident_agents.graph import app

# 🎨 Customizing the look and feel
custom_theme = gr.themes.Soft(
    primary_hue="emerald",
    secondary_hue="slate",
    neutral_hue="slate",
)

def get_report_history():
    """Scans the reports folder and returns a list of filenames."""
    if not os.path.exists("reports"):
        return []
    # List .md files, sorted by newest first
    files = [f for f in os.listdir("reports") if f.endswith(".md")]
    return sorted(files, reverse=True)

def load_report_content(filename):
    """Reads and returns the content of a selected report file."""
    if not filename:
        return "Select a report from the list to view it."
    path = os.path.join("reports", filename)
    with open(path, "r") as f:
        return f.read()

def preview_csv(file):
    if file is None: return None
    return pd.read_csv(file.name).head(10)

def process_incident(file_obj, text_input):
    raw_data = ""
    if file_obj:
        raw_data = pd.read_csv(file_obj.name).to_string()
    elif text_input:
        raw_data = text_input
    else:
        return 0, "⚠️ No data provided.", "Error", gr.update(choices=get_report_history())

    initial_state = {
        "raw_data": raw_data, "logs": [], "detected_threats": [],
        "risk_score": 0, "incident_report": "", "next_step": ""
    }
    
    result = app.invoke(initial_state)
    
    # Update the history list after a new report is generated
    return (
        result.get("risk_score", 0),
        result.get("incident_report", "No report generated."),
        "✅ Analysis Complete",
        gr.update(choices=get_report_history())
    )

# --- Gradio UI Layout ---
with gr.Blocks(theme=custom_theme, title="Cyber Detect AI") as demo:
    gr.Markdown("# 🛡️ Cyber Detect AI - Security Command Center")
    
    with gr.Row():
        with gr.Column(scale=2):
            with gr.Tabs() as tabs:
                with gr.TabItem("📁 File Analysis", id=0):
                    file_input = gr.File(label="Upload logs.csv", file_types=[".csv"])
                    preview_table = gr.Dataframe(label="Log Preview", interactive=False)
                    file_input.change(fn=preview_csv, inputs=file_input, outputs=preview_table)
                
                with gr.TabItem("✍️ Manual Entry", id=1):
                    text_input = gr.Textbox(label="Raw Log Snippets", lines=8)

                with gr.TabItem("📜 History", id=2):
                    gr.Markdown("### Past Incident Reports")
                    report_list = gr.Dropdown(label="Select a Report", choices=get_report_history())
                    history_display = gr.Markdown("Select a file above to preview.")
                    refresh_btn = gr.Button("🔄 Refresh List")

            analyze_btn = gr.Button("🔍 START DETECTION ENGINE", variant="primary")
            
        with gr.Column(scale=1):
            risk_gauge = gr.Number(label="Threat Risk Score (0-100)")
            status_label = gr.Label(label="Engine Status", value="Ready")
            
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📜 AI Generated Incident Report")
            report_markdown = gr.Markdown("The report will appear here after analysis.")

    # Event Wiring
    analyze_btn.click(
        fn=process_incident,
        inputs=[file_input, text_input],
        outputs=[risk_gauge, report_markdown, status_label, report_list]
    )
    
    report_list.change(fn=load_report_content, inputs=report_list, outputs=history_display)
    refresh_btn.click(fn=lambda: gr.update(choices=get_report_history()), outputs=report_list)

if __name__ == "__main__":
    demo.launch()