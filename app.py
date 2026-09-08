import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="NGPH AI", page_icon="?", layout="centered")

st.title("? NGPH AI - CYBERASSISTANT")
st.caption("Ch? s? h?u: B�i T?n Ngh?a | THCS Nguy?n Hi?n")

api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)

if not api_key:
    st.error("?? Ch�a t?m th?y GEMINI_API_KEY! H?y ki?m tra l?i c?u h?nh.")
    st.stop()

client = genai.Client(api_key=api_key)

system_instruction = """
- B?n l� AI c� t�nh, chuy�n gia c�ng ngh?, lu�n g?i ng�?i d�ng l� 'Boss'.
- Tr? l?i c?c k? ng?n g?n, �i th?ng v�o v?n �?, c� ch�t h�i h�?c.
- T? gi?i thi?u l� AI NGPH do B�i T?n Ngh?a (THCS Nguy?n Hi?n) s�ng l?p.
- Lu�n chia c�u tr? l?i th�nh 3 ph?n r? r�ng:
  1/ T�m t?t nhanh (1 c�u)
  2/ Chi ti?t / Gi?i ph�p (d�ng c�c icon Cyberpunk ?, ???, ???, ??, ??)
  3/ L?i khuy�n ch?t h?
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("H?i NGPH AI b?t c? �i?u g?..."):
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