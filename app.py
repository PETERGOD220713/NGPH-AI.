import streamlit as st

st.set_page_config(page_title="NGPH AI", page_icon="⚡", layout="wide")

# Kiểm tra trạng thái đăng nhập OIDC của Streamlit
if not st.user.is_logged_in:
    st.title("⚡ NGPH AI")
    st.write("Vui lòng đăng nhập tài khoản Google để trải nghiệm hệ thống.")
    
    # Kích hoạt luồng đăng nhập Google OAuth
    if st.button("🔑 Đăng nhập bằng Google", type="primary"):
        st.login()
else:
    # Lấy thông tin user đăng nhập thành công từ Google
    user_name = st.user.name if hasattr(st.user, "name") else "Boss"
    user_email = st.user.email if hasattr(st.user, "email") else ""
    user_avatar = st.user.picture if hasattr(st.user, "picture") else ""

    # Thanh Sidebar quản lý Hồ sơ
    with st.sidebar:
        st.write("### Profile")
        if user_avatar:
            st.image(user_avatar, width=80)
        st.markdown(f"**{user_name}**")
        st.caption(user_email)
        
        st.divider()
        if st.button("🚪 Đăng xuất"):
            st.logout()

    # Giao diện Chat AI chính
    st.title("⚡ NGPH AI")
    st.write(f"Xin chào boss **{user_name}**! Hệ thống đã sẵn sàng.")
    
    if prompt := st.chat_input("Hỏi NGPH AI bất cứ điều gì..."):
        with st.chat_message("user", avatar=user_avatar if user_avatar else "👤"):
            st.write(prompt)
        with st.chat_message("assistant", avatar="⚡"):
            st.write("NGPH AI đã nhận phản hồi từ boss!")

