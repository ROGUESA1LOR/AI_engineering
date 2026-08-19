# Podman Agentic CI Flake Classifier

An end-to-end local AI toolchain engine that connects live to the GitHub REST API, automates the ingestion of failed workflow telemetry, isolates log noise via stream filtering, and leverages local Ollama models to diagnose environmental flakes versus code regressions.

## Architecture Pipeline

```text
[GitHub Cloud VM] ──(Fails Run)──► [GitHub REST API]
                                            │
                                      (curl Ingestion)
                                            │
                                            ▼
[Local state.json Cache] ◄──(Dump)─── [agent.py Engine] ◄──► [Local Ollama Core]
```

## System Features

* **Authenticated API Telemetry Ingestion:** Leverages native subprocess curl operations matching GitHub data domain routing keys to extract raw binary log archives (`logs.zip`).
* **Blackboard State Machine Pattern:** Implements a strict Read-Update-Write structural database synchronization loop inside RAM using valid JSON notation keys.
* **Context Fencing Rules:** Filters away trailing control characters, whitespace formatting variables, and setup boilerplate code to prevent quadratic context window bloat before inference.

## Quick Start Run

Ensure your local Ollama core is up with the required inference model initialized:
```bash
ollama run llama3.1:8b
```

Initialize your authenticated access parameter environment file variable inside `.env`:
```text
GITHUB_TOKEN=ghp_your_classic_token_string_here
```

Execute the core pipeline transaction loop:
```bash
python3 agent.py
```
.
## Outcome

![Result](<Screenshot from 2026-08-18 21-05-21.png>)

