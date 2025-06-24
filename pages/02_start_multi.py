import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 제목과 서브헤더
st.title("나의 첫 Streamlit 앱")
st.subheader("여기 서브헤더")

# 텍스트 출력
st.write("안녕하세요! 이것은 간단한 Streamlit 애플리케이션입니다.")
st.write("안녕! 반갑다")

# 숫자 입력 받기
number1 = st.number_input("행 갯수 입력",
                   min_value=0, max_value=100, value=50)
number2 = st.number_input("열 갯수 입력",
                   min_value=1, max_value=9, value=2)

st.write(f"입력한 숫자: {number1}")
st.write(f"입력한 숫자: {number2}")

# 버튼 만들기
if st.button("버튼 클릭"):
    st.write("버튼이 클릭되었습니다!")
if st.button("다시 클릭"):
    st.write("다시 버튼이 클릭되었습니다!")
if st.button("마지막 클릭"):
    st.write("마지막 버튼이 클릭되었습니다!")

st.divider()  # 구분선 추가
# 2x2 버튼 격자 레이아웃
# 첫 번째 행
col1, col2 = st.columns(2)
with col1:
    st.button("버튼1")
with col2:
    st.button("버튼2")
# 두 번째 행
col3, col4 = st.columns(2)
with col3:
    st.button("버튼3")
with col4:
    st.button("버튼4")

st.divider()  # 구분선 추가
# 셀렉트 박스
option = st.selectbox("옵션을 선택", ["안녕", "강녕", "하이", "반갑"])
st.write(f"선택한 인사: {option}")

st.divider()  # 구분선 추가
# 데이터 생성
data = pd.DataFrame(
    np.random.randn(number1, number2),
    columns=[f"col_{i+1}" for i in range(number2)]
)

# 라인 차트 컬럼 선택
st.subheader("라인 차트 컬럼 선택")
all_columns = data.columns.tolist()
selected_columns = []

st.write("차트에 표시할 컬럼을 선택하세요:")
for col in all_columns:
    # 각 컬럼에 대한 고유한 체크박스를 생성합니다.
    # 기본적으로 모든 컬럼이 선택되도록 초기값을 True로 설정합니다.
    # Streamlit 위젯에 고유한 key를 부여하는 것이 중요합니다.
    if st.checkbox(col, value=True, key=f"line_chart_checkbox_{col}"):
        selected_columns.append(col)


# 선택된 컬럼으로 라인 차트 그리기
if selected_columns:
    st.line_chart(data[selected_columns])
else:
    st.info("차트에 표시할 컬럼을 하나 이상 선택해주세요.")

# 체크박스
if st.checkbox("데이터 표시"):
    st.write("데이터가 표시됩니다:")  # 이 체크박스는 차트와는 별개입니다.
if st.checkbox("데이터 다시 표시"):
    st.write("데이터가 다시 표시됩니다:")

slider_option = st.slider("슬라이더 옵션", 1, 5)
st.write(f"선택한 슬라이더 옵션: {slider_option}")

level = st.slider("레벨을 선택하세요", number2, number1)
st.write(f"선택한 레벨: {level}")

# 사이드바에 데이터 표시
st.sidebar.write("여기에 생성된 데이터가 표시됩니다.")
st.sidebar.write(data)
