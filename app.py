import streamlit as st
import os
import google.generativeai as genai
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Configuración de la página
st.set_page_config(page_title="Asistente Montessori Lab", page_icon="🪵")

# Título e interfaz
st.title("🪵 Asistente Inteligente Montessori Lab")
st.markdown("Consulta información sobre nuestros muebles artesanales y filosofía.")

# 1. Configuración de Seguridad (API Key desde los Secrets de la plataforma)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Por favor, configura la GOOGLE_API_KEY en los Secrets.")
    st.stop()

# 2. Preparación de la Base de Datos (Carga de archivos TXT)
@st.cache_resource
def preparar_cerebro():
    # Buscamos archivos .txt en la carpeta 'data'
    path_datos = "data/"
    archivos = [f for f in os.listdir(path_datos) if f.endswith('.txt')]
    
    docs = []
    for f in archivos:
        loader = TextLoader(os.path.join(path_datos, f), encoding='utf-8')
        docs.extend(loader.load())
    
    # Procesamiento
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    
    # Motor de búsqueda local (HuggingFace)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
    return vectorstore

# Inicializar el "cerebro"
with st.spinner("Cargando catálogo de Montessori Lab..."):
    vectorstore = preparar_cerebro()

# 3. Interfaz de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt_usuario := st.chat_input("¿En qué puedo ayudarte hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt_usuario})
    with st.chat_message("user"):
        st.markdown(prompt_usuario)

    # Lógica de Respuesta (RAG)
    with st.chat_message("assistant"):
        # Búsqueda de contexto
        docs_relevantes = vectorstore.similarity_search(prompt_usuario, k=3)
        contexto = "\n\n".join([d.page_content for d in docs_relevantes])
        
        # Generación con Gemini 2.5 Flash
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        prompt_final = f"""
        Eres un experto de Montessori Lab. 
        Responde basándote estrictamente en este contexto:
        {contexto}
        
        Pregunta: {prompt_usuario}
        """
        
        response = model.generate_content(prompt_final)
        respuesta_texto = response.text
        st.markdown(respuesta_texto)
    
    st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})