import streamlit as st

st.set_page_config(
    page_title="Contact",
    page_icon="📧",
)

st.title("Contact 페이지")
st.write("연락처 정보 페이지입니다.")

with st.form("contact_form"):
    name = st.text_input("이름")
    email = st.text_input("이메일")
    message = st.text_area("메시지")
    submitted = st.form_submit_button("제출")
    if submitted:
        st.success(f"{name}님, 메시지가 성공적으로 전송되었습니다.")