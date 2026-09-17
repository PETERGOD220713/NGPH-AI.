import streamlit as st
from authlib.integrations.streamlit_client import OAuth

# 🛠️ 1. Cấu hình trang & Session State
st.set_page_config(page_title="NGPH AI", page_icon="⚡", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

# 🛠️ 2. Khởi tạo OAuth Client (Authlib)
oauth = OAuth()
oauth.register(
    name="google",
    client_id=st.secrets.get("GOOGLE_CLIENT_ID", ""),
    client_secret=st.secrets.get("GOOGLE_CLIENT_SECRET", ""),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# 🛠️ 3. Hàm xử lý đăng nhập / đăng xuất
def login():
    # Điêu hướng tới luồng OAuth
    st.login("google")

def logout():
    st.session_state.user = None
    st.rerun()

# 🛠️ 4. Tinh chỉnh Sidebar Interface
with st.sidebar:
    st.title("💻 NGPH AI Control")
    if st.session_state.user:
        st.write(f"👤 **User:** {st.session_state.user.get('name', 'Boss')}")
        st.write(f"📧 **Email:** {st.session_state.user.get('email', '')}")
        st.button("🚪 Đăng xuất", on_click=logout, use_container_width=True)
    else:
        st.warning("🔒 Chưa đăng nhập")
        if st.button("🔑 Đăng nhập bằng Google", use_container_width=True):
            login()

# 🛠️ 5. Giao diện Chat chính
st.header("⚡ PETERGOD Chat Interface")

if not st.session_state.user:
    st.info("🎯 Boss vui lòng đăng nhập ở thanh bên (Sidebar) để bắt đầu chat!")
else:
    # Luồng Chat chính
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Nhập câu hỏi tại đây..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Trả lời từ AI
        response = f"🤖 [NGPH AI]: Đã nhận lệnh từ Boss: '{prompt}'"
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
