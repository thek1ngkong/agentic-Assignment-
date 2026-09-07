# CyberSec Multi-Agent AI

A beginner-friendly Agentic AI cybersecurity project implementing the four assignment requirements:

1. PDF/document retrieval and question answering (RAG Agent)
2. Research Agent that searches, summarizes, and produces references
3. Security Log Analyst Agent that identifies threats, severity, and mitigations
4. Multi-agent collaboration using a LangGraph workflow

## Architecture

User -> Orchestrator -> PDF/RAG Agent -> Security Analyst -> Research Agent -> Report Agent -> Final Report

## Setup (Windows)

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and add your API key.

Run:
```cmd
streamlit run app.py
```

The application also works in DEMO MODE when no API key is configured. Demo mode uses deterministic local logic so the project can be demonstrated without an API call.

## Input

- Upload a PDF in the sidebar for the RAG component.
- Upload a `.log`, `.txt`, or `.csv` security log.
- Enter a question or investigation objective.

A sample security log is included in `logs/security.log`.

## Assignment mapping

### Requirement 1
The Document/RAG Agent extracts PDF text, creates TF-IDF vectors, retrieves relevant chunks, and uses the LLM to answer the query.

### Requirement 2
The Research Agent performs a web search using the OpenAI Responses API when an API key is available, summarizes the findings, and records references.

### Requirement 3
The Security Analyst Agent parses authentication/security logs, detects suspicious patterns, assigns severity, and recommends mitigations.

### Requirement 4
The Orchestrator coordinates specialized agents:
- Document/RAG Agent
- Security Analyst Agent
- Research Agent
- Report Agent

## Safety

This is a defensive educational project. It analyzes supplied logs and produces defensive recommendations; it does not perform exploitation.
