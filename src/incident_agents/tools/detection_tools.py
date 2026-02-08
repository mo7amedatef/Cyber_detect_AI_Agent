from langchain_core.tools import tool
import pandas as pd
import os

@tool
def query_security_logs(query: str):
    """
    Searches the local security_logs.csv for specific patterns.
    Use this to find failed logins, IP addresses, or specific error codes.
    """
    # Systematic approach: loading data from your 'data/' folder
    log_path = "data/security_logs.csv"
    if not os.path.exists(log_path):
        return "Error: security_logs.csv not found in data/ directory."
    
    df = pd.read_csv(log_path)
    # Simple keyword search for demonstration
    results = df[df.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)]
    return results.head(5).to_json()

@tool
def check_ip_reputation(ip_address: str):
    """
    Checks the reputation of an IP address.
    Returns whether the IP is known for malicious activity like phishing or botnets.
    """
    # This acts as a mock for a real API like VirusTotal
    malicious_ips = ["192.168.1.50", "45.33.22.11"]
    if ip_address in malicious_ips:
        return f"ALARM: {ip_address} is flagged as MALICIOUS in threat intelligence."
    return f"IP {ip_address} appears to be CLEAN or UNKNOWN."

# Export tools as a list for the agent
cyber_tools = [query_security_logs, check_ip_reputation]