import streamlit as st

st.set_page_config(
    page_title="Help",
    page_icon="❓",
)

st.title("Help 페이지")
st.write("도움말 페이지입니다.")

st.header("자주 묻는 질문 (FAQ)")
st.subheader("Q: 이 앱은 어떻게 사용하나요?")
st.write("A: 왼쪽 사이드바에서 원하는 페이지를 클릭하여 이동할 수 있습니다.")

st.subheader("Q: 페이지를 더 추가할 수 있나요?")
st.write("A: 네, `pages` 디렉토리에 새로운 파이썬 파일을 추가하면 자동으로 사이드바에 표시됩니다.")