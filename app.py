import streamlit as st
import os
from dotenv import load_dotenv

from interviewer_agent.agent import InterviewAgent
from interviewer_agent.evaluation import InterviewEvaluator
from resume_processor.extractor import extract_text_from_pdf
from resume_processor.analyzer import analyze_resume
from sandbox.executor import run_python_code

# =========================
# LOAD API KEY
# =========================
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    st.error("ERROR: No API key found. Add it to .env as OPENAI_API_KEY")
    st.stop()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="JobMatch AI – Mock Interviewer",
    layout="centered"
)

# =========================
# HEADER
# =========================
st.title("JobMatch AI – Mock Interviewer")
st.write("Welcome! Upload your resume to begin the interview process.")

# =========================
# RESUME UPLOAD
# =========================
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

resume_data = None

if uploaded_file:
    with st.spinner("Extracting text from PDF..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Analyzing resume..."):
        resume_data = analyze_resume(resume_text)

    st.success("Resume processed successfully!")
    st.subheader("Resume Summary")
    st.json(resume_data)

# =========================
# INTERVIEW SECTION
# =========================
if resume_data:

    
    if "agent" not in st.session_state:
        st.session_state.agent = InterviewAgent(
            api_key=API_KEY,
            resume_summary=resume_data["summary_text"]
        )

  
    if "conversation" not in st.session_state:
        st.session_state.conversation = ""

    st.write("---")
    st.subheader("Interview Chat")

    
    user_msg = st.text_area(
        "Your message:",
        height=140,
        placeholder="Type your response or answer the interviewer's question...",
    )

    if st.button("Send"):
        if user_msg.strip() == "":
            st.warning("Please type a message before sending.")
        else:
            
            reply = st.session_state.agent.ask(user_msg)

            
            st.session_state.conversation += f"\nUser: {user_msg}\nAI: {reply}\n"

            
            st.write("**Interviewer:**")
            st.info(reply)

    # =========================
    # FINISH INTERVIEW
    # =========================
    if st.button("Finish Interview"):
        evaluator = InterviewEvaluator(API_KEY)

        with st.spinner("Generating final evaluation report..."):
            report = evaluator.evaluate(st.session_state.conversation)

        st.subheader("Final Evaluation Report")
        st.markdown(report)

    # =========================
    # CODING SANDBOX
    # =========================
    st.write("---")
    st.subheader("🧪 Coding Sandbox")
    st.caption("Use this area to write Python code when the interviewer asks coding questions.")

    user_code = st.text_area(
        "Write Python code:",
        height=200,
        placeholder="def solve():\n    pass"
    )

    if st.button("Run Code"):
        if user_code.strip() == "":
            st.warning("Please enter code first.")
        else:
            result = run_python_code(user_code)

            if result["success"]:
                st.success("Execution Successful!")
                st.code(result["output"])
            else:
                st.error(f"Error: {result['error']}")

else:
    st.info("Please upload your resume to start the interview.")
