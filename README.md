# Cyber Detect AI Agent

Cyber Detect AI Agent is a multi-agent cybersecurity incident detection and response system built with LangGraph.  
It ingests security logs, detects suspicious behavior, classifies risk, and generates actionable incident reports.

## Key Features

- Multi-agent workflow (Ingest -> Detect -> Classify -> Report)
- ReAct-style threat analysis with tool-assisted reasoning
- Threat intelligence enrichment for contextual risk scoring
- Markdown report generation and archival
- CLI simulation and Gradio dashboard support

## Pipeline Workflow

```mermaid
graph LR
    A[Raw Security Logs / CSV Upload] --> B[Ingest Agent]
    B --> C[Detect Agent]
    C --> D[Classify Agent]
    D --> E[Report Agent]
    E --> F[Incident Report (.md)]
```

### Stage Details

1. **Ingest Agent** (`src/incident_agents/nodes/ingest.py`)
   - Validates incoming data.
   - Detects CSV-like input and creates a temporary CSV path for downstream analysis.

2. **Detect Agent** (`src/incident_agents/nodes/detect.py`)
   - Uses LLM + tools to query logs and inspect IP reputation.
   - Produces structured threat findings.

3. **Classify Agent** (`src/incident_agents/nodes/classify.py`)
   - Enriches findings with threat intelligence.
   - Assigns a normalized risk score (0-100).

4. **Report Agent** (`src/incident_agents/nodes/report.py`)
   - Generates a professional Markdown incident report.
   - Saves the report in `reports/`.

## Repository Structure

```text
.
├── main.py
├── run_gradio_app.py
├── data/
│   ├── security_logs.csv
│   └── threat_intel.json
├── reports/
├── src/
│   └── incident_agents/
│       ├── config.py
│       ├── graph.py
│       ├── state.py
│       ├── nodes/
│       │   ├── ingest.py
│       │   ├── detect.py
│       │   ├── classify.py
│       │   └── report.py
│       └── tools/
│           ├── detection_tools.py
│           └── reporting_tools.py
└── tests/
```

## Requirements

- Python 3.13+
- Groq API key

## Setup (Recommended: uv)

```bash
uv sync
cp .env.example .env
```

Set your API key in `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Run

### CLI Simulation

```bash
uv run python main.py
```

### Gradio Dashboard

```bash
uv run python run_gradio_app.py
```

## Testing and Validation

```bash
uv run python -m compileall -q .
uv run pytest -q
```

## Troubleshooting

- **`Missing GROQ_API_KEY`**
  - Ensure `.env` exists and contains a valid `GROQ_API_KEY`.
- **`ModuleNotFoundError`**
  - Run `uv sync` and use `uv run ...` commands.

## License

Licensed under the Apache License 2.0. See `LICENSE`.
