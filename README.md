# 🤖 AI Learning Assistant

An AI-powered personalized learning assistant built with **Streamlit** and **Groq LLM (LLaMA 3)**.  
It works like a smart tutor that adapts answers based on student profile, learning style, and uploaded PDF content.

---

## 🚀 Live Demo
https://ai-personalized-learning-assistant-emdmprmaaup3vyyuqegr4j.streamlit.app/

---

## ✨ Features

- 🧠 AI Tutor powered by Groq (LLaMA 3.3 70B)
- 👨‍🎓 Personalized learning based on:
  - Student name
  - Grade level
  - Learning style (Visual, Step-by-step, Examples, Bullet points)
  - Difficulty level
- 📄 PDF upload support for context-based learning
- 💬 Chat-like interface (similar to ChatGPT)
- 📊 Learning progress tracker:
  - Questions asked
  - Answers generated
  - Topics learned
- 🧾 Extract and display PDF text inside the app
- 🎨 Modern UI with custom CSS styling

---

## 🛠️ Tech Stack

- Streamlit
- Groq API (LLaMA 3.3 70B Versatile)
- PyPDF
- python-dotenv
- Python 3.9+

---

## 📂 Project Structure

.
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

---

## ⚙️ Installation & Setup

### 1. Clone the repository
git clone https://github.com/your-username/ai-learning-assistant.git
cd ai-learning-assistant

---

### 2. Create virtual environment
python -m venv venv

Activate:

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

---

### 3. Install dependencies
pip install -r requirements.txt

---

### 4. Add API Key

Create a `.env` file:

GROQ_API_KEY=your_api_key_here

OR for Streamlit Cloud:

# .streamlit/secrets.toml
GROQ_API_KEY = "your_api_key_here"

---

## ▶️ Run the App
streamlit run app.py

---

## 📄 How It Works

1. Enter student profile in sidebar  
2. Ask questions in chat  
3. Upload PDF (optional)  
4. AI uses:
   - Chat history
   - Student profile
   - PDF content  
   to generate personalized answers  

---

## 📊 Progress Tracking

Tracks:
- Questions asked  
- Answers generated  
- Topics learned  

---

## 📦 Requirements

streamlit
groq
python-dotenv
pypdf

---

## 💡 Future Improvements

- Voice assistant 🎤  
- Quiz generator 🧪  
- Multi-PDF support 📚  
- Login system 🔐  
- Better topic detection using NLP  

---

## 👨‍💻 Author

Built with ❤️ using Streamlit + Groq LLM
