import streamlit as st
from api_utils import get_api_response

def display_chat_interface():
    st.subheader("Chat Interface")

    # Danh sách file cho phép user chọn để query
    if "documents" in st.session_state and st.session_state.documents:
        selected_file_ids = st.multiselect(
            "Choose documents to search",
            options=[doc["id"] for doc in st.session_state.documents],
            format_func=lambda x: next(doc["filename"] for doc in st.session_state.documents if doc["id"] == x),
        )
    else:
        selected_file_ids = []

    user_input = st.text_input("Ask a question:")
    if st.button("Send") and user_input:
        with st.spinner("Thinking..."):
            resp = get_api_response(
                question=user_input,
                model=st.session_state.get("model", "gemini-2.5-flash"),
                session_id=st.session_state.get("session_id"),
                
            )
            if resp:
                st.session_state.session_id = resp["session_id"]
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "assistant", "content": resp["answer"]})

    # Hiển thị lịch sử chat
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
