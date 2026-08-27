# AI Engineering Lab

A working repository for experiments in Python, AI systems, automation, and backend development.

This repo is intentionally a lab rather than a polished single application. The projects below are the parts worth looking at first.

## Projects

### Agentic CI Flake Classifier

A local AI pipeline that connects to the GitHub REST API, ingests failed workflow telemetry, filters log noise, maintains local state, and uses Ollama to diagnose likely environmental flakes versus code regressions.

**Stack:** Python, GitHub REST API, Ollama, JSON, Podman

→ [Open project](./podman-agentic-ci-prototype)

### Duo Agent Debate

A local multi-agent experiment where two Ollama models debate a topic through a shared state file and FIFO synchronization, with a human moderator controlling the loop.

**Stack:** Bash, Ollama, jq, Linux, named pipes

→ [Open project](./duo-agent-debate)

## Lab notes

The rest of this repository contains smaller experiments and learning work. They are kept here as development history rather than presented as portfolio projects.

## Direction

I'm primarily interested in Python backend systems, AI applications, local LLM infrastructure, automation, and understanding systems from the lower level up.
