import streamlit as st
from summarizer import summarize_text

st.set_page_config(page_title="Text Summarizer", layout="wide")
st.title("📚 Text Summarizer Chatbot")

text_input = st.text_area("Paste your text here", height=300)

if st.button("Summarize"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Summarizing..."):
            summary = summarize_text(text_input)
            st.success("✅ Summary:")
            st.write(summary)
