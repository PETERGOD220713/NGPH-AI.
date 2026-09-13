import streamlit as st
from streamlit_google_auth import Authenticate

st.set_page_config(page_title="NGPH AI", page_icon="⚡", layout="wide")

# Khởi tạo Google Auth từ Secrets
authenticator = Authenticate(
    secret_credentials_path={
        "web": {
            "client_id": st.secrets["google_auth"]["client_id"],
            "client_secret": st.secrets["google_auth"]["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [st.secrets["google_auth"]["redirect_uri"]]
        }
    },
    cookie_name='ngph_ai_cookie',
    cookie_key='ngph_ai_secret_key_123',
    redirect_uri=st.secrets["google_auth"]["redirect_uri"]
)

# Kiểm tra trạng thái đăng nhập
authenticator.check_authentification()

# GIAO DIỆN CHƯA ĐĂNG NHẬP
if not st.session_state.get('connected'):
    st.title("⚡ NGPH AI")
    st.write("Vui lòng đăng nhập tài khoản Google để trải nghiệm hệ thống.")
    
    authorization_url = authenticator.get_authorization_url()
    st.link_button("🔑 Đăng nhập bằng Google", authorization_url, type="primary")

# GIAO DIỆN ĐÃ ĐĂNG NHẬP
else:
    user_info = st.session_state.get('user_info', {})
    user_name = user_info.get('name', 'User')
    user_email = user_info.get('email', '')
    user_avatar = user_info.get('picture', '')

    with st.sidebar:
        st.write("### Profile")
        if user_avatar:
            st.image(user_avatar, width=80)
        st.markdown(f"**{user_name}**")
        st.caption(user_email)
        
        st.divider()
        if st.button("🚪 Đăng xuất"):
            authenticator.logout()
            st.rerun()

    st.title("⚡ NGPH AI")
    st.write(f"Chào boss **{user_name}**! Hệ thống đã sẵn sàng.")
    
    # Khung Chat
    if prompt := st.chat_input("Hỏi NGPH AI bất cứ điều gì..."):
        with st.chat_message("user", avatar=user_avatar if user_avatar else "👤"):
            st.write(prompt)
        with st.chat_message("assistant", avatar="⚡"):
            st.write("NGPH AI đã nhận phản hồi từ boss!")
