import os
import streamlit as st
from google import genai

# 🛠️ 1. Cấu hình giao diện Streamlit
st.set_page_config(page_title="NGPH AI", page_icon="⚡", layout="wide")

# CSS căn chỉnh giao diện
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem !important;
    }
    div[data-testid="stPopover"] > button {
        border-radius: 12px !important;
        height: 45px !important;
        width: 45px !important;
        border: 1px solid #30363d !important;
        background-color: #1e1e1e !important;
        color: #1677ff !important;
        font-size: 20px !important;
        font-weight: bold !important;
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

# 🛠️ 3. Header giao diện: Tiêu đề bên trái, Đăng nhập / Đăng ký bên phải
col_header_left, col_header_right = st.columns([0.7, 0.3], vertical_alignment="center")

with col_header_left:
    st.title("⚡ NGPH AI")

with col_header_right:
    try:
        if hasattr(st, "user") and st.user.is_logged_in:
            st.success(f"👤 {st.user.email}")
            if st.button("🚪 Đăng xuất", key="btn_logout"):
                st.logout()
        else:
            if st.button("🔑 Đăng nhập / Đăng ký", key="btn_login", use_container_width=True):
                st.login()
    except Exception:
        if st.button("🔑 Đăng nhập / Đăng ký", key="btn_guest_login", use_container_width=True):
            st.info("Chức năng Google OAuth đang chạy ở Chế độ Khách!")

st.divider()

# Khởi tạo danh sách tin nhắn
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🛠️ 4. Hiển thị Lời chào mừng trên màn hình chính khi chưa nhắn tin
if len(st.session_state.messages) == 0:
    st.markdown("""
        <div style="text-align: center; padding: 40px 20px;">
            <h1 style="font-size: 2.2rem; font-weight: 700; color: #1677ff;">⚡ Xin chào bạn, chúc bạn một ngày thật vui vẻ!</h1>
            <p style="font-size: 1.1rem; color: #888; margin-top: 10px;">NGPH AI đã sẵn sàng hỗ trợ. Hãy nhập câu hỏi bên dưới để bắt đầu trò chuyện nhé!</p>
        </div>
    """, unsafe_allow_html=True)

# 🛠️ 5. Hiển thị lịch sử chat
for msg in st.session_state.messages:
    avatar_icon = "⚡" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])

# 🛠️ 6. Thanh nhập câu hỏi tích hợp Nút ➕
col_btn, col_input = st.columns([0.08, 0.92], vertical_alignment="bottom")

with col_btn:
    with st.popover("➕", help="Thêm file đính kèm"):
        uploaded_file = st.file_uploader("Tải tệp đính kèm:", type=["png", "jpg", "jpeg", "pdf", "txt"], key="gemini_file")
        if uploaded_file:
            st.caption(f"📎 {uploaded_file.name}")

with col_input:
    prompt = st.chat_input("Hỏi NGPH AI bất cứ điều gì...")

# 🛠️ 7. Xử lý gửi tin nhắn
if prompt:
    display_prompt = prompt
    if 'uploaded_file' in locals() and uploaded_file:
        display_prompt = f"📎 **[Đính kèm: {uploaded_file.name}]**\n\n{prompt}"
        
    st.session_state.messages.append({"role": "user", "content": display_prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(display_prompt)

    with st.chat_message("assistant", avatar="⚡"):
        if not client:
            st.error("Chưa cấu hình GEMINI_API_KEY trong Secrets!")
        else:
            with st.spinner("⚡ **NGPH AI đang suy nghĩ...**"):
                try:
                    full_content = f"{SYSTEM_INSTRUCTION}\n\nNgười dùng hỏi: {prompt}"
                    if 'uploaded_file' in locals() and uploaded_file:
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
