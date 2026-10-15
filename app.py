import os
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from streamlit_oauth import OAuth2Component

# 🛠️ 1. Cấu hình trang & Nhúng Meta Google Search Console
st.set_page_config(page_title="NGPH AI - Trợ Lý Trí Tuệ Nhân Tạo", page_icon="⚡", layout="wide")

# Script tự động nhúng thẻ meta Google Search Console vào thẻ <head>
components.html(
    """
    <script>
        var meta = document.createElement('meta');
        meta.name = "google-site-verification";
        meta.content = "DURWEmlubkF"; // Mã xác minh Google Search Console của boss
        parent.document.getElementsByTagName('head')[0].appendChild(meta);
    </script>
    """,
    height=0,
)

# CSS căn chỉnh giao diện Cyberpunk & nút đính kèm ➕
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem !important;
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

# 🛠️ 2. Khởi tạo Gemini Client & OAuth Configuration
API_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
client = genai.Client(api_key=API_KEY) if API_KEY else None

CLIENT_ID = st.secrets.get("GOOGLE_CLIENT_ID", os.environ.get("GOOGLE_CLIENT_ID", ""))
CLIENT_SECRET = st.secrets.get("GOOGLE_CLIENT_SECRET", os.environ.get("GOOGLE_CLIENT_SECRET", ""))
REDIRECT_URI = st.secrets.get("REDIRECT_URI", "https://ngph-ai-whqmmuqlkucrwrqfk8ymkr.streamlit.app/")

AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_URL = "https://oauth2.googleapis.com/revoke"

oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_URL, TOKEN_URL, TOKEN_URL, REVOKE_URL)

SYSTEM_INSTRUCTION = """
Bạn là NGPH AI, một trợ lý trí tuệ nhân tạo thông minh.
KHI CÓ BẤT KỲ CÂU HỎI NÀO VỀ NGƯỜI TẠO, TÁC GIẢ HOẶC TRƯỜNG HỌC (Ví dụ: "Ai tạo ra bạn", "Ai là người sáng tạo ra bạn", "Tác giả của bạn là ai", "Bạn học trường nào"):
-> BẮT BUỘC TRẢ LỜI LÀ: "Mình được tạo ra bởi Bùi Tấn Nghĩa, học sinh tại trường THCS Nguyễn Hiền!"
"""

# Bộ nhớ lưu trữ lịch sử trò chuyện theo email người dùng
if "chat_db" not in st.session_state:
    st.session_state.chat_db = {}

# 🛠️ 3. Thanh Header & Đăng nhập Google OAuth
col_header_left, col_header_right = st.columns([0.6, 0.4], vertical_alignment="center")

user_email = "guest_user"
user_name = "Khách"
user_avatar = "👤"

with col_header_left:
    st.title("⚡ NGPH AI")
    st.caption("Ứng dụng Trí tuệ nhân tạo tạo bởi Bùi Tấn Nghĩa (THCS Nguyễn Hiền)")

with col_header_right:
    if "auth_token" not in st.session_state or not st.session_state.auth_token:
        result = oauth2.authorize_button(
            name="🔑 Đăng nhập bằng Google",
            icon="https://www.google.com/favicon.ico",
            redirect_uri=REDIRECT_URI,
            scope="openid email profile",
            key="google_auth",
            use_container_width=True
        )
        if result and "token" in result:
            st.session_state.auth_token = result["token"]
            st.rerun()
    else:
        token = st.session_state.auth_token
        user_info = token.get("id_token", {})
        
        user_email = user_info.get("email", "google_user")
        user_name = user_info.get("name", "Người dùng Google")
        user_avatar = user_info.get("picture", "👤")

        c_pic, c_info = st.columns([0.25, 0.75], vertical_alignment="center")
        with c_pic:
            if user_avatar != "👤":
                st.image(user_avatar, width=42)
            else:
                st.write("👤")
        with c_info:
            st.markdown(f"**{user_name}**")
            if st.button("🚪 Đăng xuất", key="btn_logout"):
                st.session_state.auth_token = None
                st.rerun()

st.divider()

# 🛠️ 4. Tải và hiển thị lịch sử chat của user
if user_email not in st.session_state.chat_db:
    st.session_state.chat_db[user_email] = []

user_chat_history = st.session_state.chat_db[user_email]

if len(user_chat_history) == 0:
    st.markdown("""
        <div style="text-align: center; padding: 40px 20px;">
            <h1 style="font-size: 2.2rem; font-weight: 700; color: #1677ff;">⚡ Xin chào bạn, chúc bạn một ngày thật vui vẻ!</h1>
            <p style="font-size: 1.1rem; color: #888; margin-top: 10px;">NGPH AI đã sẵn sàng hỗ trợ. Hãy nhập câu hỏi bên dưới để bắt đầu trò chuyện nhé!</p>
        </div>
    """, unsafe_allow_html=True)

for msg in user_chat_history:
    msg_avatar = "⚡" if msg["role"] == "assistant" else msg.get("avatar", "👤")
    with st.chat_message(msg["role"], avatar=msg_avatar):
        st.markdown(msg["content"])

# 🛠ˆ 5. Ô nhập liệu và nút ➕
col_btn, col_input = st.columns([0.08, 0.92], vertical_alignment="bottom")

with col_btn:
    with st.popover("➕", help="Thêm file đính kèm"):
        uploaded_file = st.file_uploader("Tải tệp đính kèm:", type=["png", "jpg", "jpeg", "pdf", "txt"], key="gemini_file")
        if uploaded_file:
            st.caption(f"📎 {uploaded_file.name}")

with col_input:
    prompt = st.chat_input("Hỏi NGPH AI bất cứ điều gì...")

# 🛠️ 6. Xử lý phản hồi AI & lưu cuộc trò chuyện
if prompt:
    display_prompt = prompt
    if 'uploaded_file' in locals() and uploaded_file:
        display_prompt = f"📎 **[Đính kèm: {uploaded_file.name}]**\n\n{prompt}"
        
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
                    
                    ai_msg_obj = {"role": "assistant", "content": answer}
                    user_chat_history.append(ai_msg_obj)
                except Exception as e:
                    st.error(f"Lỗi API: {str(e)}")
