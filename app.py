import os
import streamlit as st
from google import genai

# 🛠️ 1. Cấu hình giao diện Streamlit
st.set_page_config(page_title="NGPH AI", page_icon="⚡", layout="wide")

# 🛠️ 2. Lấy API Key từ Secrets hoặc Biến môi trường
API_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

client = None
if API_KEY:
    client = genai.Client(api_key=API_KEY)

# Chỉ dẫn hệ thống nhận diện Tác giả & Trường học
SYSTEM_INSTRUCTION = """
Bạn là NGPH AI, một trợ lý trí tuệ nhân tạo thông minh.
KHI CÓ BẤT KỲ CÂU HỎI NÀO VỀ NGƯỜI TẠO, TÁC GIẢ HOẶC TRƯỜNG HỌC (Ví dụ: "Ai tạo ra bạn", "Ai là người sáng tạo ra bạn", "Tác giả của bạn là ai", "Bạn học trường nào"):
-> BẮT BUỘC TRẢ LỜI LÀ: "Mình được tạo ra bởi Bùi Tấn Nghĩa, học sinh tại trường THCS Nguyễn Hiền!"
"""

# 🛠️ 3. Quản lý trạng thái Đăng nhập
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

with st.sidebar:
    st.title("⚡ NGPH AI System")
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
        st.info("💡 Chế độ khách (Guest Mode)")
        st.session_state.logged_in = True

# 🛠️ 4. Khung Chat chính
st.header("⚡ NGPH AI - Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat (Icon Sấm sét cho NGPH AI)
for msg in st.session_state.messages:
    avatar_icon = "⚡" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

# Nhập câu hỏi từ người dùng
if prompt := st.chat_input("Nhập câu hỏi cho NGPH..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Trả lời từ NGPH AI với Avatar Sấm sét ⚡
    with st.chat_message("assistant", avatar="⚡"):
        if not client:
            st.error("Chưa cấu hình GEMINI_API_KEY trong Secrets!")
        else:
            # Hiển thị trạng thái "Đang suy nghĩ..."
            with st.spinner("⚡ **NGPH AI đang suy nghĩ...**"):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=f"{SYSTEM_INSTRUCTION}\n\nNgười dùng hỏi: {prompt}"
                    )
                    
                    # Thông báo trạng thái đã chuẩn bị câu trả lời
                    st.toast("⚡ Đã chuẩn bị câu trả lời cho bạn!", icon="⚡")
                    
                    answer = response.text
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Lỗi API: {str(e)}")
