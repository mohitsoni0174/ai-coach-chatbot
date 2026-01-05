import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings # Free local embeddings

# 1. New Helper Function: Process the PDF
def process_pdf(uploaded_file):
    # Save temp file
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Load and split into chunks
    loader = PyPDFLoader("temp.pdf")
    data = loader.load()
    
    # Chunking is key: standard is 1000 chars with 200 char overlap
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(data)
    
    # Create Vector Store (Knowledge Base)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

# 2. Add UI for Upload in your Sidebar
with st.sidebar:
    st.markdown("---")
    st.subheader("📁 Knowledge Base")
    uploaded_file = st.file_uploader("Upload coach manual (PDF)", type="pdf")
    if uploaded_file:
        with st.spinner("Analyzing document..."):
            st.session_state.vector_db = process_pdf(uploaded_file)
            st.success("Knowledge Added!")

# 3. Modify Chat Logic to use RAG
# Inside your chat input block, before the API call:
context = ""
if "vector_db" in st.session_state:
    # Find top 3 most relevant chunks to the user's question
    docs = st.session_state.vector_db.similarity_search(prompt, k=3)
    context = "\n".join([doc.page_content for doc in docs])

# Update system instruction to include context
system_content = f"{coach_prompts[coach_mode]} Answer ONLY using this context if provided: {context}"