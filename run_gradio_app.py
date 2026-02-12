import gradio as gr
import pandas as pd
import os
from src.incident_agents.graph import app

# Using Slate for neutrals and Sky for the primary focus to create a calm atmosphere
kind_theme = gr.themes.Soft(
    primary_hue="sky",
    secondary_hue="slate",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "sans-serif"]
).set(
    # Custom CSS-like overrides for a "softer" feel
    body_background_fill="#F9FBFC",  # Soft off-white to reduce glare
    block_title_text_weight="600",
    block_label_text_size="*text_sm",
    button_primary_background_fill="#0284C7", # Soft Sky Blue
    button_primary_background_fill_hover="#0369A1",
)

def get_report_history():
    if not os.path.exists("reports"): return []
    files = [f for f in os.listdir("reports") if f.endswith(".md")]
    return sorted(files, reverse=True)

def load_report_content(filename):
    if not filename: return "Select a report to view."
    with open(os.path.join("reports", filename), "r") as f:
        return f.read()

def preview_csv(file_obj):
    if file_obj is None:
        return pd.DataFrame()
    try:
        return pd.read_csv(file_obj.name).head(5)
    except Exception:
        return pd.DataFrame()

def process_incident(file_obj, text_input):
    raw_data = ""
    if file_obj:
        # Preserve raw CSV content so ingest can route this run to the uploaded dataset.
        with open(file_obj.name, "r", encoding="utf-8") as f:
            raw_data = f.read()
    elif text_input:
        raw_data = text_input
    else:
        return 0, "⚠️ Please provide log data.", "Idle", gr.update()

    # Shared state logic
    initial_state = {
        "raw_data": raw_data, "logs": [], "detected_threats": [],
        "risk_score": 0, "incident_report": "", "next_step": ""
    }
    
    result = app.invoke(initial_state)
    
    return (
        result.get("risk_score", 0),
        result.get("incident_report", "Analysis complete."),
        "✅ System Ready",
        gr.update(choices=get_report_history())
    )

# --- Friendly UI Layout ---
with gr.Blocks(theme=kind_theme, title="Cyber Detect AI") as demo:
    with gr.Column(elem_id="container"):
        gr.Markdown("# 🛡️ Cyber Detect AI")
        gr.Markdown("A systematic, multi-agent approach to security incident detection.")
        
        with gr.Row():
            with gr.Column(scale=3):
                with gr.Tabs():
                    with gr.TabItem("📁 Log Upload"):
                        file_input = gr.File(label="Upload CSV Logs", file_types=[".csv"])
                        preview = gr.Dataframe(label="Data Preview", interactive=False)
                        file_input.change(fn=preview_csv, inputs=file_input, outputs=preview)
                    
                    with gr.TabItem("✍️ Snippet Entry"):
                        text_input = gr.Textbox(label="Manual Log Input", lines=6, placeholder="Paste log lines here...")

                    with gr.TabItem("📜 History"):
                        report_list = gr.Dropdown(label="Previous Reports", choices=get_report_history())
                        history_md = gr.Markdown("*Select a report above to view details.*")
                        report_list.change(fn=load_report_content, inputs=report_list, outputs=history_md)

                analyze_btn = gr.Button("RUN DETECTION ENGINE", variant="primary")
                
            with gr.Column(scale=1):
                # Using a 'Label' and 'Number' for clarity
                risk_display = gr.Number(label="Threat Probability (%)", precision=0)
                status_box = gr.Label(label="Engine Status", value="System Idle")
                
        with gr.Row():
            gr.Markdown("### 📊 Live Analysis Output")
            report_out = gr.Markdown("Analysis report will appear here...")

    # Event Wiring
    analyze_btn.click(
        fn=process_incident,
        inputs=[file_input, text_input],
        outputs=[risk_display, report_out, status_box, report_list]
    )

if __name__ == "__main__":
    demo.launch()
