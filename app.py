import os
import streamlit as st
from google import genai

# 🛠️ 1. Cấu hình giao diện Streamlit
st.set_page_config(page_title="NGPH AI", page_icon="⚡", layout="wide")

# CSS Custom để kéo nút ➕ vào thẳng bên trong thanh chat kiểu Gemini
st.markdown("""
<style>
    /* Định vị container chứa nút bấm */
    div[data-element-baseline="true"] {
        position: relative;
    }
    /* Đẩy nút popover lồng vào góc trái thanh chat */
    div[data-testid="stPopover"] {
        position: absolute;
        bottom: 12px;
        left: 15px;
        z-index: 999;
    }
    /* Tùy chỉnh kiểu dáng nút ➕ */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 35px !important;
        height: 35px !important;
        padding: 0 !important;
        border: none !important;
        background-color: #2b2c2e !important;
        color: #ffffff !important;
    }
    /* Thêm lề trái cho ô chat input để chữ không đè lên nút ➕ */
    div[data-testid="stChatInput"] textarea {
        padding-left: 50px !important;
    }
</style>
""", unsafe_allow_html=True)

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

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    avatar_icon = "⚡" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

# 🛠️ 5. Nút ➕ lồng thẳng trên thanh gõ câu hỏi
with st.popover("➕", help="Thêm file đính kèm"):
    uploaded_file = st.file_uploader("Tải tệp đính kèm:", type=["png", "jpg", "jpeg", "pdf", "txt"], key="gemini_file")
    if uploaded_file:
        st.caption(f"📎 {uploaded_file.name}")

prompt = st.chat_input("Hỏi NGPH AI bất cứ điều gì...")

# 🛠️ 6. Xử lý gửi tin nhắn
if prompt:
    display_prompt = prompt
    if uploaded_file:
        display_prompt = f"📎 **[Đính kèm: {uploaded_file.name}]**\n\n{prompt}"
        
    st.session_state.messages.append({"role": "user", "content": display_prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(display_prompt)

    # Trả lời từ NGPH AI với Avatar Sấm sét ⚡
    with st.chat_message("assistant", avatar="⚡"):
        if not client:
            st.error("Chưa cấu hình GEMINI_API_KEY trong Secrets!")
        else:
            with st.spinner("⚡ **NGPH AI đang suy nghĩ...**"):
                try:
                    full_content = f"{SYSTEM_INSTRUCTION}\n\nNgười dùng hỏi: {prompt}"
                    if uploaded_file:
                        full_content += f"\n\n[Tệp đính kèm: {uploaded_file.name}]"

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=full_content
                    )
                    
                    st.toast("⚡ Đã chuẩn bị câu trả lời cho bạn!", icon="⚡")
                    
                    answer = response.text
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Lỗi API: {str(e)}")
