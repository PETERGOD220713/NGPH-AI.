import os
import streamlit as st
from google import genai

# 🛠️ 1. Cấu hình giao diện Streamlit chuẩn Cyberpunk
st.set_page_config(page_title="NGPH AI", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem !important;
    }
    /* Style cho avatar Google góc trên */
    .user-avatar-img {
        border-radius: 50%;
        border: 2px solid #1677ff;
    }
    /* Custom nút bấm ➕ */
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

# 🛠️ 2. Khởi tạo Gemini Client
API_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
client = genai.Client(api_key=API_KEY) if API_KEY else None

SYSTEM_INSTRUCTION = """
Bạn là NGPH AI, một trợ lý trí tuệ nhân tạo thông minh.
KHI CÓ BẤT KỲ CÂU HỎI NÀO VỀ NGƯỜI TẠO, TÁC GIẢ HOẶC TRƯỜNG HỌC (Ví dụ: "Ai tạo ra bạn", "Ai là người sáng tạo ra bạn", "Tác giả của bạn là ai", "Bạn học trường nào"):
-> BẮT BUỘC TRẢ LỜI LÀ: "Mình được tạo ra bởi Bùi Tấn Nghĩa, học sinh tại trường THCS Nguyễn Hiền!"
"""

# Khai báo kho lưu trữ lịch sử chat toàn cục theo từng User ID
if "chat_db" not in st.session_state:
    st.session_state.chat_db = {}

# 🛠️ 3. Thanh Header & Đăng nhập / Đăng ký Google
col_header_left, col_header_right = st.columns([0.6, 0.4], vertical_alignment="center")

user_id = "guest_user"
user_avatar = "👤"
is_logged = False

with col_header_left:
    st.title("⚡ NGPH AI")

with col_header_right:
    try:
        if hasattr(st, "user") and st.user.is_logged_in:
            is_logged = True
            user_id = getattr(st.user, "email", "google_user")
            user_name = getattr(st.user, "name", "Người dùng Google")
            user_avatar = getattr(st.user, "picture", "👤")

            c_pic, c_info = st.columns([0.2, 0.8], vertical_alignment="center")
            with c_pic:
                if user_avatar != "👤":
                    st.image(user_avatar, width=42)
                else:
                    st.write("👤")
            with c_info:
                st.markdown(f"**{user_name}**")
                if st.button("🚪 Đăng xuất", key="btn_logout"):
                    st.logout()
        else:
            if st.button("🔑 Đăng nhập / Đăng ký bằng Google", key="btn_login", use_container_width=True):
                st.login("google")
    except Exception:
        if st.button("🔑 Đăng nhập / Đăng ký Google", key="btn_guest_login", use_container_width=True):
            st.info("💡 Bạn đang dùng Chế độ Khách (Dữ liệu lưu tạm thời)!")

st.divider()

# 🛠️ 4. Tải lịch sử cuộc trò chuyện riêng của Tài khoản
if user_id not in st.session_state.chat_db:
    st.session_state.chat_db[user_id] = []

user_chat_history = st.session_state.chat_db[user_id]

# 🛠️ 5. Hiển thị Lời chào mừng trên màn hình chính khi chưa có tin nhắn
if len(user_chat_history) == 0:
    st.markdown("""
        <div style="text-align: center; padding: 40px 20px;">
            <h1 style="font-size: 2.2rem; font-weight: 700; color: #1677ff;">⚡ Xin chào bạn, chúc bạn một ngày thật vui vẻ!</h1>
            <p style="font-size: 1.1rem; color: #888; margin-top: 10px;">NGPH AI đã sẵn sàng hỗ trợ. Hãy nhập câu hỏi bên dưới để bắt đầu trò chuyện nhé!</p>
        </div>
    """, unsafe_allow_html=True)

# Hiển thị tất cả tin nhắn đã lưu trong lịch sử của user này
for msg in user_chat_history:
    msg_avatar = "⚡" if msg["role"] == "assistant" else msg.get("avatar", "👤")
    with st.chat_message(msg["role"], avatar=msg_avatar):
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

# 🛠️ 7. Xử lý gửi tin nhắn & Tự động LƯU cuộc trò chuyện
if prompt:
    display_prompt = prompt
    if 'uploaded_file' in locals() and uploaded_file:
        display_prompt = f"📎 **[Đính kèm: {uploaded_file.name}]**\n\n{prompt}"
        
    # Lưu tin nhắn người dùng vào bộ nhớ riêng của user đó
    user_msg_obj = {"role": "user", "content": display_prompt, "avatar": user_avatar}
    user_chat_history.append(user_msg_obj)
    
    with st.chat_message("user", avatar=user_avatar):
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
                    
                    # Lưu tin nhắn của AI vào bộ nhớ riêng của user đó
                    ai_msg_obj = {"role": "assistant", "content": answer}
                    user_chat_history.append(ai_msg_obj)
                except Exception as e:
                    st.error(f"Lỗi API: {str(e)}")
