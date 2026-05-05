# Rasa Airline Agent Harness

A small Rasa Pro / CALM assistant project built to test and demonstrate a working **Rasa MCP tools harness** inside VS Code.

The assistant is currently an early airline customer service prototype. Its first working flow helps a user start a flight upgrade request by collecting a booking reference and destination, then returning a structured upgrade-check response.

This project was built step by step with a simple development loop:

```text
make a small change → validate → train → test in Rasa Inspector → capture transcript
```

---

## What This Project Demonstrates

This repo demonstrates:

- Rasa Pro 3.16.5
- CALM / flow-based assistant design
- Rasa Inspector local testing
- Rasa MCP tools configured for VS Code / GitHub Copilot
- MCP server running in `stdio` mode
- Copilot using Rasa MCP tools to inspect flows, slots, and validate the project
- A working airline upgrade flow
- A clean GitHub-ready setup with virtual environments, models, cache files, and local secrets excluded

---

## Current Assistant Capability

The assistant currently supports a basic **flight upgrade request**.

It collects:

- `booking_reference`
- `destination`

Example conversation:

```text
User: I want to upgrade my flight

Assistant: Sure, I can help check upgrade eligibility. What is your booking reference?

User: ABC123

Assistant: Thanks. What is the destination for this flight?

User: Amsterdam

Assistant: Thanks. I have your booking reference as ABC123 and your destination as Amsterdam. I’ll now check whether this flight may be eligible for an upgrade.
```

This is intentionally still simple. The focus of this repo is proving the Rasa + MCP + VS Code harness works cleanly before expanding the assistant.

---

## Verified MCP Tooling Status

The Rasa MCP tools are configured and working in VS Code.

Verified locally:

- Rasa Pro is installed and licensed
- Python environment rebuilt on Python 3.11.9
- VS Code starts the `rasa-tools` MCP server successfully
- MCP server runs in `stdio` mode
- VS Code discovered 17 Rasa tools
- GitHub Copilot can call Rasa MCP tools
- Copilot successfully inspected:
  - project flows
  - slots
  - validation status
  - important Rasa files
- The project validates when `endpoints.yml` is passed
- The model trains successfully
- Rasa Inspector runs the assistant locally

---

## Important Setup Note

This project should be run with **Python 3.11.9** or another modern Python 3.11 patch release.

During setup, Python 3.11.0 caused an import issue when starting the Rasa MCP server because the OpenAI agents dependency failed during import. Rebuilding the virtual environment with Python 3.11.9 resolved the issue.

Recommended:

```text
Python 3.11.9+
Rasa Pro 3.16.5
```

Avoid using Python 3.12+ or Python 3.13+ for this project unless Rasa compatibility is confirmed.

---

## Project Structure

```text
rasa-airline-agent-harness/
├── .github/
│   └── skills/                  # Rasa Copilot skill files installed by Rasa Tools
├── .rasa/
│   └── tools.yaml               # Rasa MCP tools configuration
├── .vscode/
│   └── mcp.example.json         # Portable example MCP config
├── actions/
│   ├── __init__.py
│   └── actions.py
├── data/
│   ├── flows.yml                # Main assistant flow definitions
│   └── patterns.yml             # Built-in/default Rasa patterns
├── CLAUDE.md                    # Agent/coding-assistant project instructions
├── config.yml                   # Rasa pipeline and policy configuration
├── credentials.yml              # Channel credentials
├── domain.yml                   # Slots and responses
├── endpoints.yml                # Action endpoint and NLG/rephrase config
├── pyproject.toml               # Python project dependencies
├── uv.lock                      # Locked dependency versions
└── README.md
```

Generated or local-only files are intentionally ignored:

```text
.venv/
.venv_py3110_backup/
models/
.rasa/cache/
.rasa/llms.txt
.rasa/llms-full.txt
.vscode/mcp.json
.env
```

---

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/QinnniQ/rasa-airline-agent-harness.git
cd rasa-airline-agent-harness
```

### 2. Create a virtual environment

Use Python 3.11.9 or another compatible Python 3.11 patch version.

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
python --version
```

Expected:

```text
Python 3.11.9
```

### 3. Install dependencies

This project uses `uv`.

```powershell
uv sync
```

### 4. Set the Rasa license

Rasa Pro requires a valid license.

For the current PowerShell session:

```powershell
$env:RASA_LICENSE = "PASTE_YOUR_RASA_LICENSE_HERE"
```

Or set it permanently at Windows user level:

```powershell
[System.Environment]::SetEnvironmentVariable(
  "RASA_LICENSE",
  "PASTE_YOUR_RASA_LICENSE_HERE",
  "User"
)
```

Do not commit your license to GitHub.

---

## Running the Project

### Validate the project

Because this project uses an NLG/rephrase endpoint in `endpoints.yml`, pass the endpoints file explicitly:

```powershell
rasa data validate --endpoints endpoints.yml
```

### Train the assistant

```powershell
rasa train
```

### Run Rasa Inspector

```powershell
rasa inspect
```

Then open the browser URL shown in the terminal, usually:

```text
http://localhost:5005/webhooks/socketio/inspect.html
```

Test with:

```text
I want to upgrade my flight
ABC123
Amsterdam
```

---

## MCP Tools Setup

The Rasa MCP tools were initialized with:

```powershell
uv run rasa tools init
```

This generated:

```text
.rasa/tools.yaml
.vscode/mcp.json
.github/skills/
```

The local `.vscode/mcp.json` file contains machine-specific paths and is ignored by Git.

A portable example is included here:

```text
.vscode/mcp.example.json
```

To use it locally, copy it:

```powershell
Copy-Item .vscode\mcp.example.json .vscode\mcp.json
```

Then open the project in VS Code:

```powershell
code .
```

In VS Code:

```text
Ctrl + Shift + P
MCP: List Servers
```

Start:

```text
rasa-tools
```

A successful connection should show that VS Code discovered the available Rasa tools.

---

## Example Copilot MCP Prompt

Once the MCP server is running, this prompt can be used in GitHub Copilot Chat:

```text
Using the Rasa MCP tools, inspect this project and tell me:
1. What Rasa project type this is
2. What flows currently exist
3. What slots currently exist
4. Whether the project is ready to train
5. Which Rasa files are most important for this project

Do not edit any files yet. Only inspect and summarize.
```

Expected output should mention:

- Rasa Pro / CALM project
- `flight_upgrade` flow
- `booking_reference` slot
- `destination` slot
- key files such as `domain.yml`, `data/flows.yml`, `data/patterns.yml`, `config.yml`, and `endpoints.yml`

---

## Current Flow

The main flow is defined in:

```text
data/flows.yml
```

Current flow:

```yaml
flows:
  flight_upgrade:
    description: Help users check whether their flight booking may be eligible for an upgrade.
    steps:
      - collect: booking_reference
        description: The passenger booking reference or reservation code.
      - collect: destination
        description: The destination city or airport for the flight.
      - action: utter_upgrade_check_placeholder
```

The slots and responses are defined in:

```text
domain.yml
```

---

## Development Loop

When making changes, follow this loop:

```text
1. Make one small change
2. Validate the project
3. Train the model
4. Test in Rasa Inspector
5. Capture the transcript
6. Commit the change
```

Useful commands:

```powershell
rasa data validate --endpoints endpoints.yml
rasa train
rasa inspect
```

---

## Known Notes

- Python 3.11.0 caused an MCP import issue in this setup.
- Python 3.11.9 resolved the MCP server issue.
- `rasa data validate` should be run with `--endpoints endpoints.yml` because rephrase-based NLG is configured there.
- Hugging Face may show an unauthenticated request warning. This is not currently blocking local testing.
- The assistant is an early prototype and does not yet connect to a real airline booking system.

---

## Next Steps

Planned improvements:

- Add passenger name collection
- Add current cabin and desired cabin
- Add a baggage policy flow
- Add a flight change/cancellation flow
- Add clearer fallback handling
- Add example test transcripts
- Add screenshots or a short demo video
- Add a mock booking lookup action
- Add end-to-end Rasa tests

---

## Status

Current status:

```text
MCP harness: working
Rasa Inspector: working
Flight upgrade flow: working
Project validation: working with endpoints.yml
Training: working
GitHub repo: initialized and pushed
```
