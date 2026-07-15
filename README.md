# Intelligent Loan Processing Agent

A minimal, deterministic UiPath coded agent starter built with Python, LangGraph, and the UiPath coded-agent runtime.

The agent accepts one text message and returns a simple typed response. It intentionally has no LLM calls, banking connections, document extraction, credit-bureau integrations, human-review tasks, or cloud-resource dependencies. This keeps the project easy to understand, run, evaluate, and extend.

## What it does

Given this input:

```json
{
  "message": "Check loan application LA-1001"
}
```

the agent returns:

```json
{
  "response": "Intelligent Loan Processing Agent is ready. Received message: Check loan application LA-1001"
}
```

The output is deterministic: the same input always produces the same response, without credentials, network calls, or model variability.

## Architecture

```text
UiPath typed input
       |
       v
LangGraph START
       |
       v
respond node
       |
       v
UiPath typed output
```

The graph is defined in `main.py` and exported as `graph`. `langgraph.json` registers it under the UiPath entry-point name `agent`.

The core types are:

- `AgentInput`: accepts a non-empty `message` string.
- `AgentState`: carries the input and generated response through the graph.
- `AgentOutput`: returns a required `response` string.
- `respond`: the single deterministic graph node.

## Technology stack

- Python 3.11, 3.12, or 3.13
- UiPath Python SDK and coded-agent runtime
- UiPath LangChain integration
- LangGraph
- Pydantic
- `uv` for dependency and virtual-environment management
- UiPath evaluation framework with an exact-match evaluator

## Repository structure

```text
.
|-- main.py                              # Typed LangGraph coded agent
|-- langgraph.json                       # UiPath LangGraph entry-point mapping
|-- uipath.json                          # UiPath runtime and packaging settings
|-- project.uiproj                       # UiPath project metadata
|-- entry-points.json                    # Generated input/output schema
|-- bindings.json                        # UiPath resource bindings; empty by design
|-- pyproject.toml                       # Python project and dependencies
|-- uv.lock                              # Reproducible dependency lockfile
|-- agent.mermaid                        # Generated graph diagram
|-- examples/
|   `-- sample-input.json                # Ready-to-run input payload
`-- evaluations/
    |-- eval-sets/smoke-test.json        # Two smoke-test cases
    `-- evaluators/exact-match.json      # Deterministic output evaluator
```

## Prerequisites

Install the following tools:

1. Python 3.11-3.13. Python 3.13 is recommended for parity with this project.
2. [`uv`](https://docs.astral.sh/uv/) for environment and dependency management.
3. The UiPath CLI, which provides the `uip` command.

Confirm the tools are available:

```powershell
python --version
uv --version
uip --version
```

## Local setup

Clone the repository and enter the project directory:

```powershell
git clone https://github.com/1AIFanatic/intelligent-loan-processing-agent.git
Set-Location intelligent-loan-processing-agent
```

Create a Python 3.13 virtual environment and install the locked dependencies:

```powershell
uv venv --python 3.13
.\.venv\Scripts\Activate.ps1
uv sync
uip codedagent setup --force --output json
```

On macOS or Linux, activate the environment with:

```bash
source .venv/bin/activate
```

## Generate UiPath schemas

The repository includes generated schemas, but regenerate them after changing any Pydantic input/output/state field, entry-point signature, or graph configuration:

```powershell
uip codedagent init
```

This updates artifacts such as `entry-points.json`, the Mermaid graph, and UiPath project metadata.

## Run the agent

Use the included input file to avoid shell-specific JSON escaping:

```powershell
uip codedagent run agent `
  --input-file examples\sample-input.json `
  --output-file run-output.json
```

Inspect the authoritative output file:

```powershell
Get-Content -Raw run-output.json
```

Expected result:

```json
{
  "response": "Intelligent Loan Processing Agent is ready. Received message: Check loan application LA-1001"
}
```

For Bash-compatible shells:

```bash
uip codedagent run agent \
  --input-file examples/sample-input.json \
  --output-file run-output.json
```

## Run the smoke evaluation

The smoke suite contains two exact-match cases. It is local and does not require an LLM judge:

```powershell
uip codedagent eval agent `
  evaluations\eval-sets\smoke-test.json `
  --no-report `
  --output-file eval-results.json
```

Expected outcome:

```text
Loan status message  1.0
Greeting message     1.0
Average              1.0
```

Why exact match? The agent is deterministic, so a binary output comparison is more precise, faster, and cheaper than an LLM-based evaluator.

## UiPath authentication

Local deterministic execution does not call external UiPath resources. Authentication becomes necessary when you push, deploy, invoke a published package, report evaluations to Studio Web, or add cloud-backed SDK services.

Check the current session with:

```powershell
uip login status --output json
```

Use an explicit organization and tenant when logging in:

```powershell
uip login --organization "<ORGANIZATION>" --tenant "<TENANT>"
```

Do not commit `.env`, access tokens, credentials, or local runtime state. The included `.gitignore` excludes those files.

## UiPath resource bindings

`bindings.json` currently contains:

```json
{
  "version": "2.0",
  "resources": []
}
```

That is intentional because `main.py` does not access assets, queues, buckets, processes, connections, Action Center apps, context indexes, or MCP servers.

When adding UiPath SDK resource calls, regenerate or update bindings so resources can be overridden per deployment environment.

## Packaging behavior

`uipath.json` excludes local environments and runtime state from packages:

- `.venv`
- `__pycache__`
- `__uipath`

The lockfile remains included so target environments can reproduce dependency resolution.

## Security and compliance posture

This repository is a technical starter, not a production lending-decision system.

- It stores no applicant data.
- It sends no data to third parties.
- It uses no secrets or credentials.
- It performs no automated credit decision.
- It makes no KYC, AML, fraud, eligibility, or underwriting determination.
- It has no authority to approve, deny, or modify a loan application.

Before using an expanded version in financial services, add appropriate privacy controls, encryption, access control, audit logging, retention policies, model-risk governance, explainability, bias testing, human review, vendor due diligence, and jurisdiction-specific legal/compliance review.

## Extending the starter

A practical evolution path is:

1. Replace the simple message with a structured loan-application input model.
2. Add document metadata or UiPath job attachments.
3. Introduce mockable adapters for credit, banking, document, email, KYC/AML, and fraud services.
4. Add deterministic validation and policy rules.
5. Add an LLM only where unstructured interpretation is genuinely needed.
6. Produce explainable risk factors and confidence values.
7. Add an explicit underwriter review mechanism before any final decision.
8. Add audit records with correlation IDs and redacted data.
9. Expand evaluations to cover missing documents, inconsistent income, adverse-action explanations, fraud flags, and service failures.
10. Deploy through Studio Web or a governed UiPath tenant only after security and compliance approval.

## Development checks

Run linting:

```powershell
ruff check main.py
```

Validate the main generated JSON files:

```powershell
python -m json.tool entry-points.json > $null
python -m json.tool bindings.json > $null
python -m json.tool evaluations\eval-sets\smoke-test.json > $null
```

## Current verification status

The initial version was verified with:

- Successful import as a `CompiledStateGraph`.
- Successful `ruff check main.py`.
- Successful `uip codedagent init` with one `agent` entry point.
- Successful local UiPath coded-agent execution.
- Two exact-match smoke evaluations, both scoring `1.0`.
- JSON validation for generated schemas, bindings, and evaluation configuration.

## Contributing

Keep changes focused and preserve these invariants:

- No module-level UiPath SDK or LLM clients.
- Re-run `uip codedagent init` after schema or entry-point changes.
- Keep `bindings.json` synchronized with resource calls.
- Add or update evaluation cases for behavior changes.
- Never commit credentials, `.env`, `.venv`, or `__uipath` runtime state.

Open an issue or pull request with a concise description of the change and the checks used to validate it.
