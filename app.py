import streamlit as st
from interviewer_agent.agent import InterviewAgent
from interviewer_agent.evaluation import InterviewEvaluator
from resume_processor.extractor import extract_text_from_pdf
from resume_processor.analyzer import analyze_resume
from sandbox.executor import run_python_code

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="JobMatch AI – Mock Interviewer",
    layout="centered"
)

# =========================
# API KEY (replace!)
# =========================
API_KEY = "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"

# =========================
# UI HEADER
# =========================
st.title("JobMatch AI – Mock Interviewer")
st.write("Welcome! Upload your resume to begin the interview process.")

# =========================
# RESUME UPLOAD SECTION
# =========================
uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

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

    # Create Interview Agent ONE TIME
    if "agent" not in st.session_state:
        st.session_state.agent = InterviewAgent(
            api_key=API_KEY,
            resume_summary=resume_data["summary_text"]
        )

    # Create conversation history
    if "conversation" not in st.session_state:
        st.session_state.conversation = ""

    st.write("---")
    st.subheader("Interview Chat")

    user_msg = st.text_input("Your message:")

    if st.button("Send"):
        if user_msg.strip() == "":
            st.warning("Please type a message.")
        else:
            reply = st.session_state.agent.ask(user_msg)

            st.session_state.conversation += (
                f"\nUser: {user_msg}\nAI: {reply}\n"
            )

            st.write("**Interviewer:**")
            st.info(reply)

    # =========================
    # FINISH INTERVIEW BUTTON
    # =========================
    if st.button("Finish Interview"):
        evaluator = InterviewEvaluator(API_KEY)

        with st.spinner("Generating evaluation report..."):
            report = evaluator.evaluate(st.session_state.conversation)

        st.subheader("Final Evaluation Report")
        st.markdown(report)

    # =========================
    # CODING QUESTION SECTION
    # =========================
    st.write("---")
    st.subheader("💻 Coding Question")

    if st.button("Generate Coding Question"):
        question = st.session_state.agent.ask("Give me a coding challenge.")
        st.session_state["coding_question"] = question

    if "coding_question" in st.session_state:
        st.info(st.session_state["coding_question"])

    # =========================
    # CODING SANDBOX SECTION
    # =========================
    st.write("---")
    st.subheader("🧪 Coding Sandbox")

    user_code = st.text_area(
        "Write Python code:",
        height=200,
        placeholder="print('Hello World')"
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
