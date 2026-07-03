import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from pypdf import PdfReader
st.set_page_config(
    page_title="AI Learning Assistant",
    page_icon="🤖",
    layout="wide"
)
# ---------------- IMPROVED CSS ----------------
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(to right, #eef2ff, #ffffff);
}
/* Title */
.main-title {
    text-align: center;
    font-size: 28px;
    color: #4F46E5;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    font-size: 15px;
    color: #555;
    margin-bottom: 20px;
}
/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff;
}
/* Sidebar title */
.sidebar-title {
    color: #4F46E5;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
}
/* ---------------- FIX: INPUT BOX BORDERS ---------------- */
/* Text input */
div[data-baseweb="input"] > div {
    border: 1px solid #c7d2fe !important;
    border-radius: 10px !important;
    padding: 2px;
    background: #ffffff !important;
}
/* Selectbox */
div[data-baseweb="select"] > div {
    border: 1px solid #c7d2fe !important;
    border-radius: 10px !important;
    background: #ffffff !important;
}
/* Focus effect */
div[data-baseweb="input"]:focus-within,
div[data-baseweb="select"]:focus-within {
    border: 2px solid #4F46E5 !important;
    box-shadow: 0 0 6px rgba(79,70,229,0.3);
}
/* Buttons */
.stButton>button {
    background: #4F46E5;
    color: white;
    border-radius: 10px;
    padding: 8px;
    border: none;
}
.stButton>button:hover {
    background: #2563EB;
}
/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 12px;
    margin: 10px 0;
    background: #ffffff;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)
# ---------------- API ----------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY not found.")
    st.stop()
client = Groq(api_key=api_key)
# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "progress" not in st.session_state:
    st.session_state.progress = {
        "questions_asked": 0,
        "answers_given": 0,
        "topics": set()
    }
# ---------------- HEADER ----------------
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="main-title">🤖 AI Learning Assistant</div>
    <div class="subtitle">Personalized AI Tutor for Every Student</div>
    """, unsafe_allow_html=True)
# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("<div class='sidebar-title'>👨‍🎓 Student Profile</div>", unsafe_allow_html=True)
    name = st.text_input("Student Name")
    grade = st.selectbox("Grade", ["1","2","3","4","5","6","7","8","9","10","11","12","College"])
    difficulty = st.selectbox("Difficulty", ["Easy","Medium","Hard"])
    learning_style = st.selectbox(
        "Learning Style",
        ["Step-by-Step","Visual","Examples","Bullet Points"]
    )
    # ---------------- PROGRESS ----------------
    with st.expander("📊 Learning Progress", expanded=False):
        st.metric("Questions Asked", st.session_state.progress["questions_asked"])
        st.metric("Answers Given", st.session_state.progress["answers_given"])
        st.metric("Topics Learned", len(st.session_state.progress["topics"]))
        st.markdown("#### 📚 Topics Covered")
        for t in list(st.session_state.progress["topics"])[-10:]:
            st.write("•", t)
        progress_val = min(st.session_state.progress["questions_asked"] / 20, 1.0)
        st.progress(progress_val)
    if st.button("🗑 Clear Chat"):
        st.session_state.messages.clear()
        st.session_state.pdf_text = ""
        st.session_state.progress = {
            "questions_asked": 0,
            "answers_given": 0,
            "topics": set()
        }
        st.rerun()
# ---------------- CHAT INPUT ----------------
prompt = st.chat_input("Ask anything...", accept_file=True, file_type=["pdf"])
question = ""
uploaded_file = None
if prompt:
    if hasattr(prompt, "text"):
        question = prompt.text
    else:
        question = str(prompt)
    if hasattr(prompt, "files") and prompt.files:
        uploaded_file = prompt.files[0]
# ---------------- PDF ----------------
if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    st.session_state.pdf_text = text[:12000]
    st.success("📄 PDF uploaded successfully")
pdf_text = st.session_state.pdf_text
with st.expander("📄 View Extracted PDF Text"):
    st.write(pdf_text)
# ---------------- TOPIC ----------------
def extract_topic(text):
    words = text.lower().split()
    stopwords = {"what", "is", "the", "how", "why", "explain", "define", "a", "an", "and", "or"}
    keywords = [w for w in words if w not in stopwords and len(w) > 3]
    return keywords[0] if keywords else "general"
# ---------------- CHAT ----------------
if question:
    topic = extract_topic(question)
    st.session_state.progress["topics"].add(topic)
    system_prompt = f"""
You are an AI tutor.
Student:
- Name: {name or "Student"}
- Grade: {grade}
- Style: {learning_style}
"""
    user_prompt = f"""
Question:
{question}
PDF:
{pdf_text if pdf_text else "No PDF uploaded"}
"""
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            messages=[
                {"role": "system", "content": system_prompt}
            ] + st.session_state.messages + [
                {"role": "user", "content": user_prompt}
            ]
        )
    answer = response.choices[0].message.content
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.progress["questions_asked"] += 1
    st.session_state.progress["answers_given"] += 1
# ---------------- CHAT DISPLAY ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])