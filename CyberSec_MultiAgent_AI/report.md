# Assignment Report

## Title
CyberSec Multi-Agent AI: Agentic Security Log Analysis and Research System

## Objective
To design an Agentic AI system in which multiple specialized agents collaborate to retrieve document knowledge, analyze security logs, research threats, and produce a structured cybersecurity report.

## Technologies
- Python
- Streamlit
- OpenAI API
- LangGraph dependency
- PyPDF
- Scikit-learn TF-IDF retrieval
- Requests

## Agents
### 1. Document/RAG Agent
Reads PDF/TXT documents, splits them into chunks, creates TF-IDF representations, retrieves the most relevant chunks, and generates an answer from retrieved context.

### 2. Security Analyst Agent
Parses security logs, counts failed and successful authentication events, extracts source IPs, identifies suspicious patterns, classifies severity, and recommends mitigations.

### 3. Research Agent
Uses the LLM research capability to summarize the likely attack technique and provide references.

### 4. Report Agent
Combines the outputs of the other agents into a structured incident report.

### 5. Orchestrator
Coordinates the workflow and passes state between the specialized agents.

## Workflow
User -> Orchestrator -> RAG Agent -> Security Analyst -> Research Agent -> Report Agent -> Final Report

## Expected Result
For repeated SSH authentication failures, the system should identify possible brute-force activity, assign an appropriate severity, recommend MFA/rate limiting/log review and produce a structured report.

## Limitations
The demonstration is educational and defensive. Automated classification is not a replacement for a human SOC analyst. Source reputation, identity, host context and successful-session details should be validated before taking action.

## Future Enhancements
- Replace TF-IDF with a persistent vector database and embedding model.
- Add Splunk/ELK ingestion.
- Add MITRE ATT&CK mapping.
- Add alert correlation and time-window analysis.
- Add authentication anomaly scoring.
- Add human approval before blocking an IP.
