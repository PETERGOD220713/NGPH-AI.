import time

# 🛠️ 6. Xử lý phản hồi AI & lưu cuộc trò chuyện (Chống lỗi 503)
if prompt:
    display_prompt = prompt
    if 'uploaded_file' in locals() and uploaded_file:
        display_prompt = f"📎 **[Đính kèm: {uploaded_file.name}]**\n\n{prompt}"

    user_msg_obj = {"role": "user", "content": display_prompt, "avatar": user_avatar}
    user_chat_history.append(user_msg_obj)

    with st.chat_message("user", avatar=user_avatar):
        st.markdown(display_prompt)

    with st.chat_message("assistant", avatar="⚡"):
        if not client:
            st.error("Chưa cấu hình GEMINI_API_KEY trong Secrets!")
        else:
            with st.spinner("⚡ **NGPH AI đang suy nghĩ...**"):
                full_content = f"{SYSTEM_INSTRUCTION}\n\nNgười dùng hỏi: {prompt}"
                if 'uploaded_file' in locals() and uploaded_file:
                    full_content += f"\n\n[Tệp đính kèm: {uploaded_file.name}]"

                models_to_try = ["gemini-3.6-flash", "gemini-2.5-flash"]
                answer = None
                last_error = None

                for model_name in models_to_try:
                    for attempt in range(2):
                        try:
                            response = client.models.generate_content(
                                model=model_name,
                                contents=full_content
                            )
                            answer = response.text
                            break
                        except Exception as e:
                            last_error = e
                            err_str = str(e)
                            if "503" in err_str or "UNAVAILABLE" in err_str:
                                time.sleep(1.5 * (attempt + 1))
                                continue
                            else:
                                break
                    if answer:
                        break

                if answer:
                    st.toast("⚡ Đã chuẩn bị câu trả lời cho bạn!", icon="⚡")
                    st.markdown(answer)
                    ai_msg_obj = {"role": "assistant", "content": answer}
                    user_chat_history.append(ai_msg_obj)
                else:
                    st.error(f"Máy chủ AI đang quá tải tạm thời, boss thử gửi lại sau vài giây nhé! ({last_error})")
