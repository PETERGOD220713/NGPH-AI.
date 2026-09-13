import streamlit as st

st.set_page_config(page_title="NGPH AI", page_icon="⚡", layout="wide")

# 1. Kiểm tra nếu CHƯA đăng nhập -> Hiện nút login và DỪNG script ngay lập tức (st.stop)
if not st.user.is_logged_in:
    st.title("⚡ NGPH AI")
    st.write("Vui lòng đăng nhập tài khoản Google để trải nghiệm hệ thống.")
    
    # Dùng callback on_click=st.login để giữ phiên đăng nhập chuẩn OIDC
    st.button("🔑 Đăng nhập bằng Google", type="primary", on_click=st.login)
    st.stop()

# 2. Sau khi ĐÃ đăng nhập thành công -> Lấy thông tin user
user_name = st.user.name if hasattr(st.user, "name") else "Boss"
user_email = st.user.email if hasattr(st.user, "email") else ""
user_avatar = st.user.picture if hasattr(st.user, "picture") else ""

# Thanh Sidebar
with st.sidebar:
    st.write("### Profile")
    if user_avatar:
        st.image(user_avatar, width=80)
    st.markdown(f"**{user_name}**")
    st.caption(user_email)
    
    st.divider()
    st.button("🚪 Đăng xuất", on_click=st.logout)

# Giao diện chính của NGPH AI
st.title("⚡ NGPH AI")
st.write(f"Xin chào boss **{user_name}**! Hệ thống đã sẵn sàng.")

if prompt := st.chat_input("Hỏi NGPH AI bất cứ điều gì..."):
    with st.chat_message("user", avatar=user_avatar if user_avatar else "👤"):
        st.write(prompt)
    with st.chat_message("assistant", avatar="⚡"):
        st.write("NGPH AI đã nhận phản hồi từ boss!")
