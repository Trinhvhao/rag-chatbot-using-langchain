from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
import os

# --- Cấu hình text splitter ---
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)

# --- Dùng mô hình embedding mạnh E5-Large-Instruct, hỗ trợ đa ngôn ngữ (bao gồm tiếng Việt) ---
embedding_function = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large-instruct",
    model_kwargs={"device": "cuda"},                # chạy trên GPU (A30)
    encode_kwargs={"normalize_embeddings": True}    # chuẩn hóa vector để search ổn định
)

# --- Khởi tạo Chroma vectorstore ---
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_function
)

def load_and_split_document(file_path: str) -> List[Document]:
    """
    Load file PDF, DOCX, HTML và chia nhỏ thành chunks.
    """
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith('.html'):
        loader = UnstructuredHTMLLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
    
    documents = loader.load()
    return text_splitter.split_documents(documents)

def index_document_to_chroma(file_path: str, file_id: int) -> bool:
    """
    Index tài liệu vào ChromaDB kèm metadata file_id.
    """
    try:
        splits = load_and_split_document(file_path)

        # Gắn metadata cho từng chunk
        for split in splits:
            split.metadata['file_id'] = file_id
        
        vectorstore.add_documents(splits)
        # vectorstore.persist()  # bật nếu muốn lưu lại trên ổ đĩa sau mỗi lần thêm
        return True
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False

def delete_doc_from_chroma(file_id: int) -> bool:
    """
    Xóa tài liệu trong Chroma theo file_id.
    """
    try:
        docs = vectorstore.get(where={"file_id": file_id})
        print(f"Found {len(docs['ids'])} document chunks for file_id {file_id}")
        
        vectorstore._collection.delete(where={"file_id": file_id})
        print(f"Deleted all documents with file_id {file_id}")
        
        return True
    except Exception as e:
        print(f"Error deleting document with file_id {file_id} from Chroma: {str(e)}")
        return False
