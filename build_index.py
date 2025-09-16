from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

pdf_dir = (r"D:\Agentic_applications\Webscraping_ai_agent\SRC\data\pdfs")  # ✅ make sure this path is correct

documents = []
for file in os.listdir(pdf_dir):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(pdf_dir, file))
        documents.extend(loader.load())

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = splitter.split_documents(documents)

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/distiluse-base-multilingual-cased-v2")
vectorstore = FAISS.from_documents(docs, embedding)
vectorstore.save_local("vectorstore")

print(f"✅ {len(docs)} chunks indexed")
