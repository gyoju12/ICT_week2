import streamlit as st

st.title("ICT 2025년도 2기 강좌 실습")
st.subheader("Streamlit 실습")

st.set_page_config(
    page_title="Main Page",
    page_icon="👋",
)

st.sidebar.success("위에서 페이지를 선택하세요.")

st.markdown(
    """
    이것은 Streamlit 멀티페이지 앱의 메인 페이지입니다.\n
    왼쪽 사이드바에서 다른 페이지로 이동할 수 있습니다.
    """
)
