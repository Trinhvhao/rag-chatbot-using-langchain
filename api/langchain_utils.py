# Sử dụng Gemini thay cho OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings  # nếu sau này cần embedding Gemini
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
import os
from chroma_utils import vectorstore
from dotenv import load_dotenv

# Tự động load biến môi trường từ file .env
load_dotenv()

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
output_parser = StrOutputParser()

# ---- PROMPT ----
contextualize_q_system_prompt = (
    "You are an assistant helping to rewrite the user's question into a clear and complete one.\n"
    "Given the previous chat history and the latest user message, rewrite the message into a standalone, fully clear question.\n"
    "If the message is already clear, return it as is.\n"
    "Do NOT answer the question."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

qa_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a friendly and helpful AI assistant.\n"
        "Answer the user's question using the provided context below.\n\n"
        "If the answer is in the context, use it directly. If not enough info, say politely that you’re not sure.\n"
        "When answering:\n"
        "- Make it natural, smooth, and easy to read (clear sentences, no unnecessary jargon).\n"
        "- Explain more details or reasoning based on the original context when possible, so the user fully understands.\n"
        "- Avoid making up information not found in the context.\n"
    ),
    ("system", "Context:\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])


def get_rag_chain(model="gemini-2.5-flash"):
    """
    Tạo RAG chain sử dụng Google Gemini với câu trả lời mượt mà và có thể giải thích thêm dựa vào dữ liệu gốc.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError(
            "⚠️ GOOGLE_API_KEY chưa được thiết lập. Hãy thêm vào file .env hoặc export biến môi trường."
        )

    # ✅ Tạo LLM Google Gemini, ép dùng API key từ .env
    llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=google_api_key
    )

    # Tạo retriever có khả năng hiểu ngữ cảnh trước
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

    # Tạo chain trả lời câu hỏi
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    # Kết hợp thành retrieval-augmented chain
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain
