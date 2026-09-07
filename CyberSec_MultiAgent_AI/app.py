import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

from agents import LLM, Orchestrator
from rag_agent import RAGAgent

load_dotenv()
st.set_page_config(page_title="CyberSec Multi-Agent AI", page_icon="🛡️", layout="wide")

st.title("🛡️ CyberSec Multi-Agent AI")
st.caption("PDF RAG + Security Log Analyst + Research Agent + Report Agent")

with st.sidebar:
    st.header("1. Document / PDF")
    uploaded_pdf = st.file_uploader("Upload a PDF or TXT reference", type=["pdf", "txt"])

    st.header("2. Security Log")
    uploaded_log = st.file_uploader("Upload .log, .txt or .csv", type=["log", "txt", "csv"])

    st.header("3. Research")
    use_research = st.checkbox("Run Research Agent", value=True)

    if os.getenv("OPENAI_API_KEY"):
        st.success("LLM API key detected")
    else:
        st.warning("DEMO MODE: no OPENAI_API_KEY found")

default_question = "Analyze the logs, identify likely threats, classify severity, and recommend defensive mitigation steps."
question = st.text_area("Investigation objective", default_question)

sample_log = Path("logs/security.log").read_text(encoding="utf-8")
log_text = sample_log
if uploaded_log:
    log_text = uploaded_log.read().decode("utf-8", errors="ignore")

rag = RAGAgent()
if uploaded_pdf:
    temp = Path("documents") / uploaded_pdf.name
    temp.write_bytes(uploaded_pdf.getvalue())
    rag.load_file(temp)
else:
    demo_doc = Path("documents/security_reference.txt")
    rag.load_file(demo_doc)

if st.button("🚀 Run Multi-Agent Analysis", type="primary"):
    llm = LLM()
    orchestrator = Orchestrator(llm, rag)
    with st.spinner("Agents collaborating..."):
        result = orchestrator.run(question, log_text, use_research)

    a = result["analyst"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Severity", a["severity"])
    c2.metric("Failed Attempts", a["failed_attempts"])
    c3.metric("Successful Logins", a["successful_logins"])

    st.subheader("🔎 Threat Analyst")
    st.write("**Potential threats**")
    for t in a["threats"]:
        st.write("• " + t)

    st.write("**Source IPs**")
    st.write(a["source_ips"])

    st.subheader("📄 RAG / Document Agent")
    st.write(result["rag_answer"])

    st.subheader("🌐 Research Agent")
    st.write(result["research"])

    st.subheader("📝 Final Report")
    st.markdown(result["report"])

    out = Path("reports") / "security_report.md"
    out.write_text(result["report"], encoding="utf-8")
    st.success(f"Report saved to {out}")
else:
    st.info("Upload your files if desired, then click Run Multi-Agent Analysis.")
    st.subheader("Assignment coverage")
    st.markdown("""
    **1. PDF/document RAG:** extracts, chunks and retrieves relevant content.  
    **2. Research:** summarizes findings and produces references.  
    **3. Security logs:** detects repeated authentication failures and classifies severity.  
    **4. Multi-agent collaboration:** Orchestrator coordinates RAG, Analyst, Research and Report agents.
    """)
