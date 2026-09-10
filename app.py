import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="NGPH AI", page_icon="⚡", layout="centered")

st.title("⚡ NGPH AI - CYBERASSISTANT")
st.caption("Chủ sở hữu: Bùi Tấn Nghĩa | THCS Nguyễn Hiền")

# Lấy API Key từ Secrets hoặc biến môi trường
api_key = st.secrets.get("GEMINI_API_KEY", None) or os.environ.get("GEMINI_API_KEY", None)

if not api_key:
    st.error("⚠️ Chưa tìm thấy GEMINI_API_KEY! Hãy kiểm tra lại cấu hình Secrets.")
    st.stop()

# Khởi tạo Client với API Key
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

if prompt := st.chat_input("Hỏi NGPH AI bất cứ điều gì..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                )
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Lỗi kết nối API: {e}")
