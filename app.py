import os
import time
import streamlit as st
from google import genai
from google.genai import types

# Cấu hình trang chuẩn Gemini
st.set_page_config(page_title="NGPH AI", page_icon="⚡", layout="centered")

# Custom CSS Giao diện chuẩn Gemini Cyberpunk
cyber_css = """
<style>
    /* Background tối kiểu Gemini */
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
    }
    
    /* Cấu hình lại Header */
    h1 {
        color: #7c4dff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        font-weight: 700;
    }
    
    /* Khung nhập liệu tròn mượt chuẩn Gemini */
    .stChatInputContainer input {
        border: 1px solid #444746 !important;
        background-color: #1e1f20 !important;
        color: #e3e3e3 !important;
        border-radius: 28px !important;
        padding: 12px 20px !important;
    }
    
    .stChatInputContainer input:focus {
        border-color: #a8c7fa !important;
        box-shadow: 0 0 10px rgba(168, 199, 250, 0.2);
    }

    /* Đổi icon người dùng thành Avatar Google / User mặc định */
    [data-testid="chatAvatarIcon-user"] {
        background-color: #004a77 !important;
        color: #c2e7ff !important;
    }

    /* Đổi icon AI thành Tia sét xoay tròn */
    [data-testid="chatAvatarIcon-assistant"] {
        background-color: #1e1f20 !important;
        color: #7c4dff !important;
        animation: spin 3s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
"""
st.markdown(cyber_css, unsafe_allow_html=True)

# Trang chủ gọn gàng chuẩn Gemini
st.title("⚡ NGPH AI")

# Check API Key
api_key = st.secrets.get("GEMINI_API_KEY", None) or os.environ.get("GEMINI_API_KEY", None)

if not api_key:
    st.error("⚠️ Chưa tìm thấy GEMINI_API_KEY! Hãy kiểm tra lại Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# System Instruction: Loại bỏ xưng hô Boss & chỉ giới thiệu tác giả khi được hỏi
system_instruction = """
- Bạn là NGPH AI, một trợ lý trí tuệ nhân tạo thông minh, linh hoạt và thân thiện.
- Trả lời rõ ràng, chính xác, khách quan, tự nhiên giống như trợ lý Google Gemini.
- Tuyệt đối KHÔNG gọi người dùng là 'Boss'. Xưng hô lịch sự, phù hợp (ví dụ: bạn / tôi).
- KHÔNG tự động giới thiệu về Bùi Tấn Nghĩa hay THCS Nguyễn Hiền ở mỗi câu trả lời.
- CHỈ khi nào người dùng hỏi trực tiếp như "Ai tạo ra bạn?", "Tác giả là ai?", "Bạn là ai?" thì mới trả lời: "Tôi là NGPH AI, được phát triển bởi Bùi Tấn Nghĩa (học sinh THCS Nguyễn Hiền)".
- Trình bày mạch lạc, dùng các icon công nghệ nhẹ nhàng khi phù hợp.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    avatar = "⚡" if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Xử lý khi người dùng nhập câu hỏi
if prompt := st.chat_input("Hỏi NGPH AI bất cứ điều gì..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚡"):
        # Trạng thái chờ câu trả lời động
        status_placeholder = st.empty()
        status_placeholder.markdown("*⚡ Đang suy nghĩ...*")
        
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                )
            )
            
            status_placeholder.markdown("*⚡ Đã chuẩn bị câu trả lời cho bạn...*")
            time.sleep(0.4)
            status_placeholder.empty()
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            status_placeholder.empty()
            st.error(f"Lỗi hệ thống: {e}")
