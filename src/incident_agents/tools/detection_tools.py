import json
import os
from typing import Optional

import pandas as pd
from langchain_core.tools import tool


_THREAT_INTEL_PATH = "data/threat_intel.json"
_THREAT_INTEL_CACHE: Optional[dict] = None


def load_threat_intel() -> str:
    """Load threat intelligence from data/threat_intel.json and return a string summary for prompts."""
    global _THREAT_INTEL_CACHE
    if _THREAT_INTEL_CACHE is not None:
        return _format_threat_intel(_THREAT_INTEL_CACHE)
    if not os.path.exists(_THREAT_INTEL_PATH):
        return "No threat intelligence file found."
    try:
        with open(_THREAT_INTEL_PATH, "r") as f:
            _THREAT_INTEL_CACHE = json.load(f)
        return _format_threat_intel(_THREAT_INTEL_CACHE)
    except Exception as e:
        return f"Error loading threat intel: {e}"


def _format_threat_intel(data: dict) -> str:
    """Format threat intel dict as a readable string."""
    parts = []
    if "malicious_ips" in data:
        parts.append("Malicious IPs: " + json.dumps(data["malicious_ips"], indent=2))
    if "known_ttps" in data:
        parts.append("Known TTPs: " + ", ".join(data["known_ttps"]))
    return "\n".join(parts) if parts else json.dumps(data)


def _get_malicious_ips_from_intel() -> set:
    """Return set of IPs marked as malicious in threat intel."""
    global _THREAT_INTEL_CACHE
    if _THREAT_INTEL_CACHE is None and os.path.exists(_THREAT_INTEL_PATH):
        try:
            with open(_THREAT_INTEL_PATH, "r") as f:
                _THREAT_INTEL_CACHE = json.load(f)
        except Exception:
            _THREAT_INTEL_CACHE = {}
    if not _THREAT_INTEL_CACHE or "malicious_ips" not in _THREAT_INTEL_CACHE:
        return set()
    return set(_THREAT_INTEL_CACHE["malicious_ips"].keys())


@tool
def query_security_logs(query: str, csv_path: Optional[str] = None):
    """
    Searches security logs for specific patterns.
    Use this to find failed logins, IP addresses, or specific error codes.
    csv_path: optional path to a CSV file; if not provided, uses data/security_logs.csv.
    """
    log_path = csv_path or "data/security_logs.csv"
    if not os.path.exists(log_path):
        return "Error: CSV file not found at " + log_path

    df = pd.read_csv(log_path)
    results = df[df.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)]
    return results.head(5).to_json()


@tool
def check_ip_reputation(ip_address: str):
    """
    Checks the reputation of an IP address using threat intelligence.
    Returns whether the IP is known for malicious activity like phishing or botnets.
    """
    malicious = _get_malicious_ips_from_intel()
    if ip_address in malicious:
        intel = _THREAT_INTEL_CACHE or {}
        details = (intel.get("malicious_ips") or {}).get(ip_address, {})
        rep = details.get("reputation", "malicious")
        typ = details.get("type", "unknown")
        return f"ALARM: {ip_address} is flagged in threat intelligence (reputation={rep}, type={typ})."
    return f"IP {ip_address} appears to be CLEAN or UNKNOWN."


cyber_tools = [query_security_logs, check_ip_reputation]
