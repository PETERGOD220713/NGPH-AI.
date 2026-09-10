import os
import streamlit as st
from google import genai
from google.genai import types

# Cấu hình trang web
st.set_page_config(page_title="NGPH AI - CYBER", page_icon="⚡", layout="centered")

# Custom CSS Giao diện Cyberpunk Neon
cyberpunk_css = """
<style>
    /* Background tổng thể */
    .stApp {
        background-color: #0d0f18;
        color: #00ffcc;
    }
    
    /* Tiêu đề chính */
    h1 {
        color: #ff0055 !important;
        text-shadow: 0 0 10px #ff0055, 0 0 20px #ff0055;
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
    }
    
    /* Khung nhập tin nhắn */
    .stChatInputContainer input {
        border: 2px solid #00ffcc !important;
        background-color: #1a1d2e !important;
        color: #ffffff !important;
        box-shadow: 0 0 10px #00ffcc;
        border-radius: 10px;
    }
    
    /* Tin nhắn của User (Boss) */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #1f243d;
        border-left: 4px solid #00ffcc;
        border-radius: 8px;
        box-shadow: 0 0 8px rgba(0,255,204,0.3);
    }
    
    /* Tin nhắn của AI (NGPH) */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #2b122c;
        border-left: 4px solid #ff0055;
        border-radius: 8px;
        box-shadow: 0 0 8px rgba(255,0,85,0.3);
    }
</style>
"""
st.markdown(cyberpunk_css, unsafe_allow_html=True)

# Header giao diện
st.title("⚡ NGPH AI - CYBERASSISTANT 🏎️")
st.caption("🎯 HỆ THỐNG TRÍ TUỆ NHÂN TẠO | DEVELOPED BY BÙI TẤN NGHĨA (THCS NGUYỄN HIỀN)")

# Check API Key
api_key = st.secrets.get("GEMINI_API_KEY", None) or os.environ.get("GEMINI_API_KEY", None)

if not api_key:
    st.error("⚠️ Chưa tìm thấy GEMINI_API_KEY! Hãy kiểm tra lại Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

system_instruction = """
- Bạn là AI cá tính, chuyên gia công nghệ, luôn gọi người dùng là 'Boss'.
- Trả lời cực kỳ ngắn gọn, đi thẳng vào vấn đề, có chút hài hước.
- Tự giới thiệu là AI NGPH do Bùi Tấn Nghĩa (THCS Nguyễn Hiền) sáng lập.
- Luôn chia câu trả lời thành 3 phần rõ ràng:
  1/ Tóm tắt nhanh (1 câu)
  2/ Chi tiết / Giải pháp (dùng các icon Cyberpunk ⚡, 🏎️, 🛠️, 💻, 🎯)
  3/ Lời khuyên chốt hạ
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("⚡ Gửi lệnh cho NGPH AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"**Boss:** {prompt}")

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                )
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Lỗi hệ thống: {e}")
