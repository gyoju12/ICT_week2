import streamlit as st
from openai import OpenAI
import os
import requests # 이미지 다운로드를 위해 requests 라이브러리 추가
from io import BytesIO # 바이트 데이터를 다루기 위해 BytesIO 추가

# Streamlit app
st.title("ChatGPT 이미지 생성하기")

# 오른쪽 사이드바에 OpenAI API 키 입력란 추가
st.sidebar.title("설정")
openai_api_key = st.sidebar.text_input(
    "OpenAI API 키를 입력하세요", 
    type="password"
)
st.sidebar.divider()

if not openai_api_key:
    st.sidebar.warning("OpenAI API 키를 입력하세요.")
    st.stop()

client = OpenAI(api_key = openai_api_key)

prompt = st.text_input("이미지 생성 프롬프트를 입력하세요", "A cute Cat")
style = st.sidebar.selectbox(
    "스타일을 선택하세요",
    ["vivid", "natural", "Realistic", "Cartoon", "Fantasy", "Abstract"],
    index=0 # 기본값으로 "vivid" 선택
)
size = st.sidebar.selectbox(
    "이미지 크기를 선택하세요",
    ["1024x1024", "1792x1024", "1024x1792"], # DALL-E 3가 지원하는 크기로 수정
    index=2 # 기본값으로 "1024x1024" 선택
)
quality = st.sidebar.selectbox(
    "이미지 품질을 선택하세요",
    ["standard", "hd"], # 품질 옵션 추가
    index=0 # 기본값으로 "standard" 선택
)

if st.button("이미지 생성"):
    # API 호출을 위한 인자 딕셔너리 준비
    api_kwargs = {
        "model": "dall-e-3",
        "n": 1,
        "size": size,
        "quality": quality
    }

    # 삼항 연산자를 사용하여 프롬프트 설정
    # 'vivid'나 'natural'이 아닐 경우에만 프롬프트에 스타일을 추가합니다.
    final_prompt = prompt if style in ["vivid", "natural"] else f"{prompt} in a {style} style"
    api_kwargs["prompt"] = final_prompt

    # 'vivid' 또는 'natural'일 경우에만 style 파라미터를 API 호출에 추가합니다.
    if style in ["vivid", "natural"]:
        api_kwargs["style"] = style

    st.write(f"전송된 프롬프트: {api_kwargs['prompt']}")
    st.write(f"적용된 API 스타일: {api_kwargs.get('style', 'vivid (기본값)')}")

    # 2개의 이미지를 생성하여 나란히 표시
    col1, col2 = st.columns(2)

    with col1:
        with st.spinner("이미지 1 생성 중..."):
            try:
                response1 = client.images.generate(**api_kwargs)
                st.image(response1.data[0].url, caption="생성된 이미지 1", use_container_width=True)
                
                # 이미지 다운로드 버튼 추가 (이미지 1)
                image1_url = response1.data[0].url
                image1_data = requests.get(image1_url).content
                st.download_button(
                    label="이미지 1 다운로드",
                    data=image1_data,
                    file_name="generated_image_1.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"이미지 1 생성에 실패했습니다: {e}")
    
    with col2:
        with st.spinner("이미지 2 생성 중..."):
            try:
                response2 = client.images.generate(**api_kwargs)
                st.image(response2.data[0].url, caption="생성된 이미지 2", use_container_width=True)
                
                # 이미지 다운로드 버튼 추가 (이미지 2)
                image2_url = response2.data[0].url
                image2_data = requests.get(image2_url).content
                st.download_button(
                    label="이미지 2 다운로드",
                    data=image2_data,
                    file_name="generated_image_2.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"이미지 2 생성에 실패했습니다: {e}")
