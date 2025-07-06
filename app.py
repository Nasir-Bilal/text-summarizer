import streamlit as st
from summarizer import summarize_text
import fitz  # PyMuPDF
import docx
from newspaper import Article

st.set_page_config(page_title="Text Summarizer", layout="wide")
st.title("📚 Text Summarizer")


isText=False

# ⚙️ Sidebar settings
st.sidebar.header("⚙️ Settings")

compression_ratio = st.sidebar.slider(
    "Compression Ratio (%)",
    min_value=10,
    max_value=90,
    value=30,
    help="Defines how much the input should be compressed. A lower value means a shorter summary."
)

max_depth = st.sidebar.slider(
    "Recursion Depth",
    min_value=1,
    max_value=10,
    value=3,
    help="Controls how many times the summary should be refined recursively. Higher depth gives more concise results."
)

# 📥 Select input type
input_mode = st.radio(
    "Select input type:",
    ("Text", "Upload File", "URL")
)

text_input = ""

#If input option is text
if input_mode == "Text":
    text_input = st.text_area("Paste your text here", height=300)
    isText=True

#If input option is File
elif input_mode == "Upload File":
    isText=False
    uploaded_file = st.file_uploader("Upload a .txt, .pdf, or .docx file", type=["txt", "pdf", "docx"])
    
    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1]

        try:
            if file_type == "txt":
                text_input = uploaded_file.read().decode("utf-8")
            elif file_type == "pdf":
                pdf_reader = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                for page in pdf_reader:
                    text_input += page.get_text()
            elif file_type == "docx":
                doc = docx.Document(uploaded_file)
                for para in doc.paragraphs:
                    text_input += para.text + "\n"
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

#if input option is URL
elif input_mode == "URL":
    isText=False
    url = st.text_input("Enter a URL:")
    if url:
        try:
            article = Article(url)
            article.download()
            article.parse()
            text_input = article.text
        except Exception as e:
            st.error(f"Invalid URL!!! Failed to extract content: {e}")

#show the extracted text if URL and file is selected
if text_input and not isText:
    st.markdown("### ✨ Extracted Text Preview")
    st.text_area("Extracted Text", text_input, height=250)

#call the summarize function
if st.button("Summarize"):
    if not text_input.strip():
        st.warning("⚠️ No input to summarize.")
    else:
        with st.spinner("Summarizing..."):
            summary = summarize_text(text_input, compression_ratio=compression_ratio, max_depth=max_depth)
            st.success("✅ Summary:")
            st.write(summary)
