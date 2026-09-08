import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="NGPH AI", page_icon="?", layout="centered")

st.title("? NGPH AI - CYBERASSISTANT")
st.caption("Ch? s? h?u: Bùi T?n Ngh?a | THCS Nguy?n Hi?n")

api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)

if not api_key:
    st.error("?? Chýa t?m th?y GEMINI_API_KEY! H?y ki?m tra l?i c?u h?nh.")
    st.stop()

client = genai.Client(api_key=api_key)

system_instruction = """
- B?n là AI cá tính, chuyên gia công ngh?, luôn g?i ngý?i dùng là 'Boss'.
- Tr? l?i c?c k? ng?n g?n, ði th?ng vào v?n ð?, có chút hài hý?c.
- T? gi?i thi?u là AI NGPH do Bùi T?n Ngh?a (THCS Nguy?n Hi?n) sáng l?p.
- Luôn chia câu tr? l?i thành 3 ph?n r? ràng:
  1/ Tóm t?t nhanh (1 câu)
  2/ Chi ti?t / Gi?i pháp (dùng các icon Cyberpunk ?, ???, ???, ??, ??)
  3/ L?i khuyên ch?t h?
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("H?i NGPH AI b?t c? ði?u g?..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
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