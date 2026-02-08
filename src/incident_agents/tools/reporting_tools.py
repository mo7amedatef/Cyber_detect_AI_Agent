import os
from datetime import datetime
from langchain_core.tools import tool

@tool
def save_incident_report(content: str, report_type: str = "incident"):
    """
    Saves the generated AI report as a Markdown file in the reports/ directory.
    report_type can be 'incident' or 'test'.
    """
    # Aligning with your project structure
    directory = "reports"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{directory}/{report_type}_report_{timestamp}.md"
    
    with open(filename, "w") as f:
        f.write(content)
    
    return f"Report successfully saved to {filename}"