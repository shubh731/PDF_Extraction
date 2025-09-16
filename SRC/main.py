import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import unicodedata
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variable
load_dotenv()
os.getenv("GOOGLE_API_KEY")

# ------------------------------
# Unicode normalization function
# ------------------------------
def normalize_text(text):
    return unicodedata.normalize("NFKC", text).strip()

# ------------------------------
# Extract and normalize text from PDFs
# ------------------------------
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                normalized = normalize_text(page_text)
                text += normalized + "\n"
    return text

# ------------------------------
# Chunk large text into smaller parts
# ------------------------------
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return text_splitter.split_text(text)

# ------------------------------
# Create and store vector embeddings
# ------------------------------
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# ------------------------------
# Setup QA chain with custom prompt
# ------------------------------
def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context.
    If the answer is not in the context, say "Answer is not available in the context".
    Do not make up an answer.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

# ------------------------------
# Query handler
# ------------------------------
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    st.write("📌 **Answer:**", response["output_text"])

# ------------------------------
# Streamlit UI
# ------------------------------
def main():
    st.set_page_config(page_title="Chat with Multilingual PDF (Gemini)", layout="wide")
    st.header("📚 Chat with PDF (English & Marathi) using Gemini 💬")

    user_question = st.text_input("Ask a question about your documents:")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("📎 Upload PDFs")
        pdf_docs = st.file_uploader("Upload your PDF files here:", accept_multiple_files=True)
        if st.button("📥 Submit & Process"):
            with st.spinner("🔄 Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("✅ Documents processed successfully!")

# ------------------------------
if __name__ == "__main__":
    main()
