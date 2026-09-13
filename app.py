https://ngph-ai-whqmmuglkucnwrqlkdymkr.streamlit.app/oauth2callback
import streamlit as st

st.set_page_config(page_title="NGPH AI", page_icon="⚡", layout="wide")

# Kiểm tra trạng thái đăng nhập OIDC của Streamlit
if not st.experimental_user.is_logged_in:
    st.title("⚡ NGPH AI")
    st.write("Vui lòng đăng nhập tài khoản Google để trải nghiệm hệ thống.")
    
    # Nút login sử dụng cấu hình [auth] từ Secrets
    if st.button("🔑 Đăng nhập bằng Google", type="primary"):
        st.login("google")
else:
    # Lấy thông tin user đăng nhập thành công
    user = st.experimental_user
    user_name = getattr(user, "name", "Boss")
    user_email = getattr(user, "email", "")
    user_avatar = getattr(user, "picture", "")

    # Thanh Sidebar
    with st.sidebar:
        st.write("### Profile")
        if user_avatar:
            st.image(user_avatar, width=80)
        st.markdown(f"**{user_name}**")
        st.caption(user_email)
        
        st.divider()
        if st.button("🚪 Đăng xuất"):
            st.logout()

    # Giao diện chính
    st.title("⚡ NGPH AI")
    st.write(f"Xin chào boss **{user_name}**! Hệ thống đã sẵn sàng.")
    
    if prompt := st.chat_input("Hỏi NGPH AI bất cứ điều gì..."):
        with st.chat_message("user", avatar=user_avatar if user_avatar else "👤"):
            st.write(prompt)
        with st.chat_message("assistant", avatar="⚡"):
            st.write("NGPH AI đã nhận phản hồi từ boss!")
