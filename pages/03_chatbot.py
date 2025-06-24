import streamlit as st
from openai import OpenAI
import os
import matplotlib.pyplot as plt
import re
from collections import Counter
import matplotlib.font_manager as fm
import platform

# 한글 폰트 설정
def set_korean_font():
    """시스템에 따라 한글 폰트를 설정합니다."""
    if platform.system() == 'Windows':
        font_name = 'Malgun Gothic'
    elif platform.system() == 'Darwin':  # macOS
        font_name = 'AppleGothic'
    else:  # Linux
        font_name = 'DejaVu Sans'
    
    try:
        plt.rcParams['font.family'] = font_name
    except:
        plt.rcParams['font.family'] = 'DejaVu Sans'
    
    plt.rcParams['axes.unicode_minus'] = False

def analyze_conversation(messages):
    """대화 내용을 분석하여 많이 사용된 단어 10개를 반환합니다."""
    # 모든 메시지 내용을 합치기
    all_text = ""
    for message in messages:
        if message["role"] in ["user", "assistant"]:
            all_text += message["content"] + " "
    
    if not all_text.strip():
        return None, "분석할 대화 내용이 없습니다."
    
    # 텍스트 전처리
    # 특수문자 제거 및 소문자 변환
    text = re.sub(r'[^\w\s가-힣]', ' ', all_text)
    text = text.lower()
    
    # 단어 분리
    words = text.split()
    
    # 불용어 제거 (한국어 및 영어 기본 불용어)
    stop_words = {
        '이것', '그것', '저것', '이', '그', '저', '의', '가', '을', '를', '에', '로', '으로', 
        '과', '와', '도', '만', '에서', '부터', '까지', '한', '하는', '하고', '할', '합니다',
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does',
        'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must'
    }
    
    # 길이가 2 이상인 단어만 필터링하고 불용어 제거
    filtered_words = [word for word in words if len(word) >= 2 and word not in stop_words]
    
    if not filtered_words:
        return None, "분석할 유의미한 단어가 없습니다."
    
    # 단어 빈도 계산
    word_counts = Counter(filtered_words)
    
    # 가장 많이 사용된 단어 10개 추출
    most_common_words = word_counts.most_common(10)
    
    return most_common_words, None

def create_word_frequency_chart(word_counts):
    """단어 빈도 차트를 생성합니다."""
    words, counts = zip(*word_counts)
    
    plt.figure(figsize=(12, 8))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('빈도수')
    plt.title('가장 많이 사용된 단어 10개')
    
    # 한글 폰트 설정
    set_korean_font()
    
    return plt

# Streamlit app
st.title("ChatGPT와 대화하기")

# 오른쪽 사이드바에 OpenAI API 키 입력란 추가
st.sidebar.title("설정")
openai_api_key = st.sidebar.text_input(
    "OpenAI API 키를 입력하세요", 
    type="password"
)

if not openai_api_key:
    st.sidebar.warning("OpenAI API 키를 입력하세요.")
    st.stop()

client = OpenAI(api_key = openai_api_key)

# 초기 대화 상태 설정
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사용자 입력
user_input = st.text_input("당신:", key="user_input")

if st.button("전송") and user_input:
    if user_input.strip() == "\분석":
        # 대화 내용 분석
        word_counts, error_message = analyze_conversation(st.session_state.messages)
        
        if error_message:
            st.error(error_message)
        else:
            # 단어 빈도 차트 생성
            chart = create_word_frequency_chart(word_counts)
            analysis_text = "📊 **대화 분석 결과**\n\n가장 많이 사용된 단어 TOP 10:\n"
            for i, (word, count) in enumerate(word_counts, 1):
                    analysis_text += f"{i}. **{word}** ({count}회)\n"

            with st.chat_message("assistant"):
                st.pyplot(chart)
                st.markdown(analysis_text)

            # 분석 결과를 세션 상태에 저장 (특별한 형태로)
            st.session_state.messages.append({
                "role": "system", 
                "content": analysis_text,
                "word_analysis": True,
                "chart": chart
            })
    else:
        # 사용자 메시지 추가
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

    # OpenAI API 호출
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = st.session_state.messages,
        # n = 2,  # 응답 개수
        temperature = 0.7,  # 창의성 조절
    )

    # OpenAI 응답 추가
    response_message = response.choices[0].message.content
    st.session_state.messages.append(
        {"role": "assistant", "content": response_message}
    )

    # 사용자 입력 초기화
    user_input = ""

# 대화 내용 표시
for message in st.session_state.messages:
    role = "🧑" if message["role"] == "user" else "🤖"
    st.markdown(f"{role}: {message['content']}")
