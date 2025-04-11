import streamlit as st
import os
import google.generativeai as genai
from io import StringIO

# Get Gemini API Key from environment
gemini_api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
else:
    st.error("Gemini API key not set. Please set GOOGLE_API_KEY as an environment variable.")

# Streamlit UI
st.set_page_config(page_title="StudyBuddy: AI College Assistant", layout="centered", page_icon="🎓")
st.title("🎓 StudyBuddy: AI College Assistant")

# Sidebar navigation
option = st.sidebar.selectbox("Choose a Feature", [
    "🎓 Ask Any Question",
    "📅 Study Planner",
    "🧠 Summarizer & Flashcards"
])

# Feature 1: Ask Any Question
if option == "🎓 Ask Any Question":
    st.subheader("Ask Any Academic Question")
    question = st.text_input("Enter your question")

    if st.button("Get Answer"):
        if not gemini_api_key:
            st.error("Gemini API key not found. Please set GOOGLE_API_KEY.")
        elif question.strip() == "":
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Thinking..."):
                    response = model.generate_content(question)
                    answer = response.text
                st.markdown("#### 🧠 Answer:")
                st.success(answer)
            except Exception as e:
                st.error(f"Error:\n\n{str(e)}")

# Feature 2: Study Planner
elif option == "📅 Study Planner":
    st.subheader("📅 Subject-Wise Study Planner")
    subjects = st.text_input("Enter your subjects (comma-separated)", "Math, Physics, Chemistry")
    hours_per_day = st.slider("Study hours per day", 1, 12, 4)

    if st.button("Generate Study Plan"):
        prompt = (
            f"Create a 7-day study plan for the following subjects: {subjects}. "
            f"The student has {hours_per_day} hours per day to study. "
            f"Balance the subjects and give a table-like summary."
        )
        try:
            with st.spinner("Generating your plan..."):
                response = model.generate_content(prompt)
                st.text_area("🗓️ Your Study Plan", response.text, height=300)
        except Exception as e:
            st.error(f"Error:\n\n{str(e)}")

# Feature 3: Summarizer & Flashcards
elif option == "🧠 Summarizer & Flashcards":
    st.subheader("🧠 Topic Summarizer & Flashcards")
    topic = st.text_area("Enter a topic or content to summarize and create flashcards")

    if st.button("Generate Summary and Flashcards"):
        prompt = (
            f"Summarize the following topic in 5 lines, then generate 3-5 flashcards (Q&A format):\n{topic}"
        )
        try:
            with st.spinner("Generating..."):
                response = model.generate_content(prompt)
                flashcard_output = response.text
                st.text_area("📘 Summary + Flashcards", flashcard_output, height=400)

                # Download option
                st.download_button(
                    label="📥 Download Flashcards",
                    data=flashcard_output,
                    file_name="flashcards.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"Error:\n\n{str(e)}")