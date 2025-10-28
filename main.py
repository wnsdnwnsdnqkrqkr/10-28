import streamlit as st
import pandas as pd
import altair as alt

# 페이지 설정
st.set_page_config(
    page_title="MBTI 유형별 국가 TOP 10",
    page_icon="🌏",
    layout="centered"
)

# 제목
st.title("🌏 MBTI 유형별 국가 TOP 10 분석 대시보드")
st.markdown("#### 특정 MBTI 유형이 특히 높은 나라들을 한눈에 살펴보세요!")

# 데이터 불러오기
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/your-repo/countriesMBTI_16types.csv"
    # 👉 Streamlit Cloud에서는 GitHub URL이나 외부 CSV 링크를 사용해야 합니다.
    # 만약 직접 업로드한다면 아래 코드를 사용하세요:
    # uploaded = st.file_uploader("CSV 파일을 업로드하세요", type="csv")
    # if uploaded:
    #     return pd.read_csv(uploaded)
    return pd.read_csv(url)

df = load_data()

# 국가명 컬럼 확인 및 정리
if "Country" not in df.columns:
    st.error("⚠️ 데이터에 'Country' 열이 없습니다. CSV를 확인해주세요.")
    st.stop()

# MBTI 타입 리스트 추출
mbti_columns = [col for col in df.columns if col != "Country"]

# 선택 박스
selected_type = st.selectbox(
    "분석할 MBTI 유형을 선택하세요 👇",
    mbti_columns,
    index=0
)

# 선택한 MBTI 기준 상위 10개 국가 추출
top10 = df.sort_values(by=selected_type, ascending=False).head(10)

# 시각화
st.subheader(f"🏆 {selected_type} 유형이 높은 TOP 10 국가")

chart = (
    alt.Chart(top10)
    .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
    .encode(
        x=alt.X(f"{selected_type}:Q", title=f"{selected_type} 비율"),
        y=alt.Y("Country:N", sort="-x", title="국가"),
        color=alt.Color(f"{selected_type}:Q", scale=alt.Scale(scheme="blues")),
        tooltip=["Country", selected_type]
    )
    .properties(height=400)
)

# 값 라벨 추가
text = chart.mark_text(
    align='left',
    baseline='middle',
    dx=3,
    color='black'
).encode(
    text=alt.Text(f"{selected_type}:Q", format=".3f")
)

# 그래프 출력
st.altair_chart(chart + text, use_container_width=True)

# 표 보기
with st.expander("📋 상위 10개 데이터 보기"):
    st.dataframe(top10.reset_index(drop=True))

# 추가 설명
st.markdown("---")
st.caption("데이터 출처: countriesMBTI_16types.csv  |  제작: ChatGPT (GPT-5)")
