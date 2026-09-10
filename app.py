import os
import streamlit as st
from google import genai
from google.genai import types

# Cấu hình trang web với Icon Sao 4 Cánh ✦
st.set_page_config(page_title="NGPH AI - CYBER", page_icon="✦", layout="centered")

# Custom CSS Giao diện Cyberpunk & Mưa Sao Băng
cyberpunk_css = """
<style>
    /* Background tổng thể */
    .stApp {
        background: linear-gradient(180deg, #05050a 0%, #0d0f18 100%);
        color: #00ffcc;
    }
    
    /* Tiêu đề chính */
    h1 {
        color: #00f0ff !important;
        text-shadow: 0 0 10px #00f0ff, 0 0 20px #7000ff;
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
    }
    
    /* Khung nhập tin nhắn */
    .stChatInputContainer input {
        border: 2px solid #00f0ff !important;
        background-color: #121526 !important;
        color: #ffffff !important;
        box-shadow: 0 0 12px #00f0ff;
        border-radius: 12px;
    }
    
    /* Tin nhắn của Boss */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #1a1e36;
        border-left: 4px solid #00ffcc;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,255,204,0.2);
    }
    
    /* Tin nhắn của NGPH AI (Có Sao 4 cánh) */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #261333;
        border-left: 4px solid #b026ff;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(176,38,255,0.3);
    }
</style>
"""
st.markdown(cyberpunk_css, unsafe_allow_html=True)

# Header giao diện với Sao 4 Cánh
st.title("✦ NGPH AI - CYBERASSISTANT 🌠")
st.caption("🎯 TRÍ TUỆ NHÂN TẠO SAO BĂNG | DEVELOPED BY BÙI TẤN NGHĨA (THCS NGUYỄN HIỀN)")

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
  2/ Chi tiết / Giải pháp (dùng các icon Cyberpunk ✦, 🌠, ⚡, 🏎️, 🛠️, 💻, 🎯)
  3/ Lời khuyên chốt hạ
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat với Icon Sao 4 cánh ✦
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "✦"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("🌠 Bấm gửi lệnh sao băng cho NGPH AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(f"**Boss:** {prompt}")

    with st.chat_message("assistant", avatar="✦"):
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
