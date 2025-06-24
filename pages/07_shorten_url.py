import streamlit as st
import pyshorteners

# 앱 제목
st.title('URL Shortener')

# URL 입력 받기
url = st.text_input('줄이고 싶은 URL 주소를 입력해 주세요.')

# URL 단축 버튼
if st.button('Shorten URL'):
    if url:
        # pyshorteners 사용하여 URL 단축
        s = pyshorteners.Shortener()
        short_url = s.tinyurl.short(url)
        st.success(f'Shortened URL: {short_url}')
        pass
    else:
        st.error('Please enter a URL to shorten')
