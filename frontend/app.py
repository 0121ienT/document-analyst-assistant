import streamlit as st
import requests

# Sidebar để nhập API URL
with st.sidebar:
    api_url = st.text_input("API URL", key="chatbot_api_url", value="http://localhost:8000/chat")

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by your API")

# Khởi tạo session lưu tin nhắn
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Tôi có thể giúp gì cho bạn ?"}]

# Hiển thị tin nhắn trước đó
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Gửi tin nhắn mới
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Gọi API với streaming
    try:
        with requests.post(api_url, json={"text": prompt}, stream=True) as response:
            response.raise_for_status()  # Kiểm tra lỗi HTTP

            msg = ""
            chat_placeholder = st.empty()  # Tạo vùng hiển thị phản hồi

            for chunk in response.iter_content(chunk_size=32):  # Đọc từng phần nhỏ
                text_chunk = chunk.decode("utf-8")
                msg += text_chunk
                chat_placeholder.markdown(msg)  # Cập nhật nội dung hiển thị dần dần

        # Lưu tin nhắn của chatbot
        st.session_state.messages.append({"role": "assistant", "content": msg})
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling API: {e}")
