from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/distiluse-base-multilingual-cased-v2")
vectorstore = FAISS.load_local("vectorstore", embedding, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

llm = OllamaLLM(model="llama2")  # ✅ Updated

qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

def get_answer(query: str) -> str:
    return qa.invoke({"query": query})["result"]
