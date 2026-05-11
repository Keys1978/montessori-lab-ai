# 🪵 Montessori Lab - Asistente Virtual con RAG

Este proyecto implementa un sistema de **Generación Aumentada por Recuperación (RAG)** diseñado para **Montessori Lab**, una empresa dedicada a la fabricación de muebles artesanales basados en la filosofía Montessori.

## 🚀 Objetivo
Optimizar la atención al cliente y la consulta de procesos internos mediante el uso de Modelos de Lenguaje de Gran Escala (LLM), permitiendo respuestas precisas basadas exclusivamente en la documentación oficial de la empresa.

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.12
* **LLM:** Google Gemini 2.5 Flash
* **Framework de IA:** LangChain
* **Base de Datos Vectorial:** ChromaDB
* **Embeddings:** HuggingFace (all-MiniLM-L6-v2)
* **Interfaz:** Streamlit

## 📂 Estructura del Repositorio
* `app.py`: Código principal de la aplicación e interfaz de usuario.
* `requirements.txt`: Dependencias necesarias para la ejecución.
* `data/`: Base de conocimiento compuesta por 10 documentos técnicos en formato .txt (procesos, seguridad, materiales y garantías).

## 🔧 Configuración
Para ejecutar este proyecto localmente o en la nube, se requiere una clave de API de Google AI Studio configurada como variable de entorno o en los secretos de Streamlit bajo el nombre `GOOGLE_API_KEY`.
