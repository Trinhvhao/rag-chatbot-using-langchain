# RAG Chatbot with FastAPI Backend and Streamlit Frontend
<img width="773" alt="RAG_Chatboat" src="https://github.com/user-attachments/assets/b135dd2e-abab-4b59-9051-795bda13e6b2" />

## Overview

This project demonstrates how to build a **multi-user RAG chatbot** that answers questions based on your own documents. The system utilizes **LangChain** for the RAG (Retrieval-Augmented Generation) component, **FastAPI** for the backend API, and **Streamlit** for the frontend interface.

This project covers:

- Implementing a **RAG system** using LangChain to combine document retrieval and response generation.
- Processing and storing documents for efficient retrieval in the RAG system.
- Building a **conversational AI** that handles multi-turn interactions.
- **Modularizing the code** for integration with FastAPI, enabling production-grade deployment.
- Creating an interactive **Streamlit frontend** that communicates with the FastAPI backend for real-time data management.

## What’s Built

- **RAG System**: Fundamentals of RAG and how to use LangChain’s models, prompts, and retrievers to create a system that answers document-based questions.
  
- **FastAPI Backend**: API endpoints for managing document uploads, processing queries, and delivering responses to the frontend.
  
- **Streamlit Frontend**: An intuitive interface that allows users to interact with the backend for uploading documents and asking questions.
<img width="699" alt="langchain2" src="https://github.com/user-attachments/assets/5c44562e-e468-4967-8004-1cded80f4a04" />


## Prerequisites

Before starting, ensure the following:

- **Python 3.8+** installed on the system.
- **pip** for managing dependencies.
- Basic understanding of **Python**, **FastAPI**, **Streamlit**, and **RESTful APIs**.
- Knowledge of **RAG systems** and **LangChain**.

### Required Packages

The following Python packages are required:

- `fastapi`
- `uvicorn`
- `streamlit`
- `langchain`
- `langchain-openai`
- `langchain-chroma`
- `python-multipart`
- `docx2txt`
- `pypdf`
