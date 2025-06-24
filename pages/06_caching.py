import streamlit as st
import pandas as pd

@st.cache_data # 캐시된 데이터 사용
def load_data(url):
    """URL에서 데이터를 로드합니다."""
    df = pd.read_csv(url, nrows=10000)
    st.write(df.shape)
    st.write(df.head())  # 데이터프레임의 첫 5행을 표시
    st.write(f"데이터의 행 수: {len(df)}")
    st.write(f"데이터의 열 수: {len(df.columns)}")
    st.write(f"데이터의 열 이름: {df.columns.tolist()}")
    st.write(f"데이터의 데이터 타입: {df.dtypes.to_dict()}")
    return df

df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")

st.dataframe(df)  # 데이터프레임을 Streamlit 앱에 표시
st.button("Rerun")  # 버튼 클릭 시 페이지 새로고침