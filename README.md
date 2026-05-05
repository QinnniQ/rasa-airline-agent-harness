# Rasa Airline Agent Harness

A Rasa Pro / CALM assistant project built to demonstrate a working **Rasa MCP tools harness** inside VS Code, including a tool-backed **ReAct sub-agent**.

The project started as a small airline customer service assistant and now includes two working features:

1. **Flight upgrade flow** — collects a booking reference and destination.
2. **Baggage policy feature** — implemented as a Rasa ReAct sub-agent connected to a local MCP server.

The development loop for this project is intentionally simple and inspectable:

```text
make a small change → validate → train → test in Rasa Inspector → capture transcript
```

---

## Latest Update: Baggage Policy ReAct Sub-Agent

This project now includes a second airline feature: a baggage policy assistant implemented as a **Rasa ReAct sub-agent**.

The flow works as:

```text
User baggage question
→ Rasa `baggage_policy` flow
→ `baggage_policy_agent` ReAct sub-agent
→ local MCP server
→ `lookup_baggage_policy` tool
→ customer-facing baggage answer
```

Verified locally:

- `rasa data validate --endpoints endpoints.yml`
- `rasa train`
- `rasa inspect`
- Rasa logs show `baggage_policy_agent` connecting successfully to the local MCP server
- MCP server logs show successful `/mcp` tool calls
- Rasa Inspector returns baggage answers for carry-on and extra baggage questions

---

## What This Project Demonstrates

This repo demonstrates:

- Rasa Pro 3.16.5
- CALM / flow-based assistant design
- Rasa Inspector local testing
- Rasa MCP tools configured for VS Code / GitHub Copilot
- MCP server running in `stdio` mode for VS Code tooling
- Copilot using Rasa MCP tools to inspect flows, slots, and validate the project
- A working flight upgrade flow
- A working baggage policy feature implemented as a ReAct sub-agent
- A local MCP server exposing a baggage policy lookup tool
- A clean GitHub-ready setup with virtual environments, models, cache files, and local secrets excluded

---

## Current Assistant Capabilities

### 1. Flight Upgrade Requests

The assistant can handle a basic flight upgrade request by collecting:

- `booking_reference`
- `destination`

Example:

```text
User: I want to upgrade my flight
Assistant: Sure, I can help check upgrade eligibility. What is your booking reference?

User: ABC123
Assistant: Thanks. What is the destination for this flight?

User: Amsterdam
Assistant: Thanks. I have your booking reference as ABC123 and your destination as Amsterdam. I’ll now check whether this flight may be eligible for an upgrade.
```

### 2. Baggage Policy Questions

The assistant can answer baggage-related questions through a ReAct sub-agent and local MCP tool.

Example:

```text
User: Can I bring a carry-on bag?

Assistant: Yes. You can bring:
- 1 carry-on/cabin bag, which must fit in the overhead bin
- 1 personal item, such as a handbag, laptop bag, or small backpack, which must fit under the seat in front of you

Size and weight limits can vary by route, fare, and operating airline.
```

---

## Verified MCP Tooling Status

The Rasa MCP tools are configured and working in VS Code.

Verified locally:

- Rasa Pro is installed and licensed
- Python environment rebuilt on Python 3.11.9
- VS Code starts the `rasa-tools` MCP server successfully
- MCP server runs in `stdio` mode for VS Code
- VS Code discovered 17 Rasa tools
- GitHub Copilot can call Rasa MCP tools
- Copilot successfully inspected project flows, slots, validation status, and important Rasa files
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
│   └── skills/                         # Rasa Copilot skill files installed by Rasa Tools
├── .rasa/
│   └── tools.yaml                      # Rasa MCP tools configuration
├── .vscode/
│   └── mcp.example.json                # Portable example MCP config
├── actions/
├── data/
│   ├── flows.yml                       # Main assistant flow definitions
│   └── patterns.yml                    # Built-in/default Rasa patterns
├── sub_agents/
│   └── baggage_policy_agent/
│       ├── config.yml                  # ReAct sub-agent configuration
│       ├── custom_agent.py             # Minimal custom agent class
│       └── prompt_template.jinja2      # Custom prompt template for the sub-agent
├── tools/
│   └── baggage_policy_mcp_server.py    # Local MCP server exposing baggage policy tool
├── CLAUDE.md
├── config.yml
├── credentials.yml
├── domain.yml
├── endpoints.yml
├── pyproject.toml
├── uv.lock
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

This project has two local servers during baggage sub-agent testing:

1. The baggage MCP server on port `8000`
2. Rasa Inspector / Rasa server on port `5005`

### 1. Start the baggage MCP server

In terminal 1:

```powershell
.venv\Scripts\activate
python .\tools\baggage_policy_mcp_server.py
```

Expected output should show something like:

```text
Uvicorn running on http://127.0.0.1:8000
```

The MCP endpoint used by Rasa is:

```text
http://127.0.0.1:8000/mcp
```

### 2. Validate the project

In terminal 2:

```powershell
.venv\Scripts\activate
rasa data validate --endpoints endpoints.yml
```

### 3. Train the assistant

```powershell
rasa train
```

### 4. Run Rasa Inspector

```powershell
rasa inspect
```

Then open the browser URL shown in the terminal, usually:

```text
http://localhost:5005/webhooks/socketio/inspect.html
```

---

## Test Conversations

### Flight Upgrade Test

```text
I want to upgrade my flight
ABC123
Amsterdam
```

Expected behavior:

- Assistant asks for booking reference
- Assistant asks for destination
- Assistant confirms it will check upgrade eligibility

### Baggage Policy Test

```text
Can I bring a carry-on bag?
```

Expected behavior:

- Rasa routes to `baggage_policy`
- `baggage_policy_agent` connects to the local MCP server
- The MCP server receives a `/mcp` tool call
- Assistant answers with the general carry-on policy

Example MCP server logs:

```text
POST /mcp HTTP/1.1 200 OK
Processing request of type CallToolRequest
```

---

## MCP Tools Setup for VS Code

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

## Current Flows

The main flows are defined in:

```text
data/flows.yml
```

### Flight Upgrade Flow

```yaml
flight_upgrade:
  description: Help users check whether their flight booking may be eligible for an upgrade.
  steps:
    - collect: booking_reference
      description: The passenger booking reference or reservation code.
    - collect: destination
      description: The destination city or airport for the flight.
    - action: utter_upgrade_check_placeholder
```

### Baggage Policy Flow

```yaml
baggage_policy:
  description: >
    Use this flow whenever the user asks about baggage, luggage, carry-on bags,
    cabin bags, hand luggage, checked bags, suitcases, baggage allowance,
    extra baggage, excess baggage, overweight baggage, oversized baggage,
    baggage fees, baggage costs, restricted items, or prohibited items.
  steps:
    - call: baggage_policy_agent
```

---

## ReAct Sub-Agent

The baggage sub-agent lives in:

```text
sub_agents/baggage_policy_agent/
```

It connects to the MCP server defined in `endpoints.yml`:

```yaml
mcp_servers:
  - name: baggage_policy_tools
    url: http://127.0.0.1:8000/mcp
    type: http
```

The sub-agent configuration uses tool filtering so it only has access to:

```text
lookup_baggage_policy
```

---

## Local Baggage MCP Server

The local MCP server lives in:

```text
tools/baggage_policy_mcp_server.py
```

It exposes:

```text
lookup_baggage_policy(question: str) -> str
```

The tool returns general baggage policy information for:

- carry-on baggage
- checked baggage
- extra / excess baggage fees
- overweight or oversized baggage
- restricted or prohibited items

The MCP server uses `streamable-http` transport:

```python
mcp.run(transport="streamable-http")
```

Rasa connects to it through:

```text
http://127.0.0.1:8000/mcp
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
- `rasa data validate` should be run with `--endpoints endpoints.yml` because rephrase-based NLG and MCP server configuration are defined there.
- The baggage MCP server must be running before starting `rasa inspect` if testing the baggage sub-agent.
- The ReAct sub-agent feature is beta, so output wording can occasionally vary.
- Hugging Face may show an unauthenticated request warning. This is not currently blocking local testing.
- The assistant is an early prototype and does not yet connect to a real airline booking system.

---

## Next Steps

Planned improvements:

- Add passenger name collection to the flight upgrade flow
- Add current cabin and desired cabin to the flight upgrade flow
- Improve final response formatting from the baggage sub-agent
- Add a flight change/cancellation flow
- Add clearer fallback handling
- Add example test transcripts
- Add screenshots or a short demo video
- Add a mock booking lookup action
- Add end-to-end Rasa tests
- Add a short architecture diagram

---

## Status

Current status:

```text
MCP harness: working
VS Code Rasa MCP tools: working
Rasa Inspector: working
Flight upgrade flow: working
Baggage ReAct sub-agent: working
Local baggage MCP server: working
Project validation: working with endpoints.yml
Training: working
GitHub repo: updated and merged
```
