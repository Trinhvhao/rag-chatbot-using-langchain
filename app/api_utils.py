import requests
import streamlit as st

API_URL = "http://localhost:9990"

def get_api_response(question, session_id, model):
    """Gửi câu hỏi tới backend"""
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "question": question,
        "model": model
    }
    if session_id:
        data["session_id"] = session_id

    try:
        st.sidebar.info(f"[DEBUG] Sending question: {question}, model={model}, session_id={session_id}")
        response = requests.post(f"{API_URL}/chat", headers=headers, json=data)
        st.sidebar.info(f"[DEBUG] Chat response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API request failed [{response.status_code}]: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred when calling /chat: {str(e)}")
        return None


def upload_document(file):
    """Upload file lên backend"""
    try:
        st.sidebar.info(f"[DEBUG] Uploading file: {file.name}")
        files = {"file": (file.name, file.getvalue(), file.type)}  # lấy bytes từ Streamlit file
        response = requests.post(f"{API_URL}/upload-doc", files=files)
        st.sidebar.info(f"[DEBUG] Upload response: {response.status_code} {response.text}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to upload file [{response.status_code}]: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while uploading the file: {str(e)}")
        return None


def list_documents():
    """Lấy danh sách file đã upload"""
    try:
        st.sidebar.info("[DEBUG] Fetching document list...")
        response = requests.get(f"{API_URL}/list-docs")
        st.sidebar.info(f"[DEBUG] List docs response: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch document list [{response.status_code}]: {response.text}")
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching the document list: {str(e)}")
        return []


def delete_document(file_id):
    """Xoá file theo id"""
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {"file_id": file_id}

    try:
        st.sidebar.info(f"[DEBUG] Deleting file id={file_id}")
        response = requests.post(f"{API_URL}/delete-doc", headers=headers, json=data)
        st.sidebar.info(f"[DEBUG] Delete response: {response.status_code} {response.text}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to delete document [{response.status_code}]: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while deleting the document: {str(e)}")
        return None
