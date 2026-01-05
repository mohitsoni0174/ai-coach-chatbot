import streamlit as st
from dotenv import load_dotenv
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

# -----------------------
# App Config
# -----------------------
st.set_page_config(page_title="RAG Document Chatbot", layout="wide")
st.title("📄 RAG Document Chatbot")

# -----------------------
# Load Environment
# -----------------------
load_dotenv()

# -----------------------
# Load Embeddings
# -----------------------
@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

embeddings = load_embeddings()

# -----------------------
# Load Vector Store
# -----------------------
@st.cache_resource
def load_vectorstore():
    if os.path.exists("rag/faiss_index"):
        return FAISS.load_local(
            "rag/faiss_index",
            embeddings,
            allow_dangerous_deserialization=True
        )

    loader = TextLoader("rag/data/sample.txt", encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("rag/faiss_index")
    return vectorstore

vectorstore = load_vectorstore()

# -----------------------
# Load LLM (Ollama)
# -----------------------
@st.cache_resource
def load_llm():
   return Ollama(model="llama3.2:latest")


llm = load_llm()

# -----------------------
# Chat UI
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
query = st.chat_input("Ask a question about the document")

if query:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Retrieve context
    docs = vectorstore.similarity_search(query, k=3)

    if not docs:
        answer = "I don't know based on the provided document."
    else:
        context = "\n\n".join(d.page_content for d in docs)

        prompt = f"""
You are a document assistant.
Answer ONLY using the context below.
If the answer is not in the context, say:
"I don't know based on the provided document."

Context:
{context}

Question:
{query}

Answer:
"""

        answer = llm.invoke(prompt)

    # Show assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
