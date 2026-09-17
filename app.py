import os
import streamlit as st
from google import genai

# 🛠️ 1. Cấu hình giao diện Streamlit
st.set_page_config(page_title="NGPH AI", page_icon="⚡", layout="wide")

# 🛠️ 2. Lấy API Key từ Secrets hoặc Biến môi trường
API_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
client = genai.Client(api_key=API_KEY) if API_KEY else None

SYSTEM_INSTRUCTION = """
Bạn là NGPH AI, một trợ lý trò chuyện thông minh.
- Tác giả / Người tạo: BÙI TẤN NGHĨA
- Trường học: THCS NGUYỄN HIỀN
Khi người dùng hỏi về người tạo hoặc trường học, hãy trả lời chính xác các thông tin trên.
"""

# 🛠️ 3. Quản lý trạng thái Đăng nhập (Authlib / Streamlit User)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Sidebar điều khiển
with st.sidebar:
    st.title("⚡ NGPH AI System")
    
    # Kiểm tra trạng thái người dùng
    try:
        if hasattr(st, "user") and st.user.is_logged_in:
            st.session_state.logged_in = True
            st.success(f"👤 **Xin chào:** {st.user.email}")
            if st.button("🚪 Đăng xuất", use_container_width=True):
                st.logout()
        else:
            st.warning("🔒 Chưa đăng nhập")
            if st.button("🔑 Đăng nhập", use_container_width=True):
                st.login()
    except Exception:
        # Nếu chạy local hoặc chưa bật Auth trên Cloud
        st.info("💡 Chế độ khách (Guest Mode)")
        st.session_state.logged_in = True

# 🛠️ 4. Khung Chat chính
st.header("⚡ NGPH AI - Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Nhập câu hỏi từ người dùng
if prompt := st.chat_input("Nhập câu hỏi cho NGPH..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not client:
            st.error("Chưa cấu hình GEMINI_API_KEY trong Secrets!")
        else:
            with st.spinner("⚡ NGPH AI đang suy nghĩ..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"{SYSTEM_INSTRUCTION}\n\nNgười dùng: {prompt}"
                    )
                    answer = response.text
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Lỗi API: {str(e)}")
