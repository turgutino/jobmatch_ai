# JobMatch AI – Intelligent Mock Interviewer  
An AI-powered interview simulation system built with **Streamlit**, **OpenAI API**, and **Python**.  
The application analyzes the user's resume, conducts a structured interview (technical + behavioral), evaluates responses, and generates a final score report.

---

## 🚀 Features

### ✔ Resume Upload & Parsing
Upload a **PDF resume**, and the system automatically:
- extracts text,
- analyzes skills,
- generates a resume summary,
- stores key information for interview context.

### ✔ Dynamic Interview Agent (LLM)
The AI interviewer:
- behaves like a **Senior Software Engineer at Google**,
- asks **one question at a time**,
- generates resume-based, technical, and behavioral questions,
- remembers previous answers (conversation context),
- provides follow-up questions,
- stops only when the candidate writes: `finish interview`.

### ✔ Coding Sandbox (Secure Execution)
The interviewer asks coding questions naturally during the interview.  
The user writes Python code in the built-in sandbox:

- code is executed safely using a restricted environment
- output or errors are returned instantly
- supports logic testing, printing, functions, etc.

### ✔ Automated Evaluation Report
When the user writes `finish interview`, the system produces a structured analysis:

- Score (0–100)
- Strengths
- Weaknesses
- Suggested improvements
- Better example answers

---

## 🧠 System Architecture

