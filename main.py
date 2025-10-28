import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="세계 행복 지수 분석", layout="wide")

st.title("🌏 세계 행복 지수 분석 대시보드")
st.markdown("""
이 앱은 **World Happiness Report** 데이터를 기반으로  
각국의 행복 점수와 사회적 요인(GDP, 자유, 기대수명 등)을 시각적으로 분석합니다.
""")

# --- 데이터 업로드 or 샘플 데이터 사용 ---
st.sidebar.header("📂 데이터 업로드")
uploaded_file = st.sidebar.file_uploader("CSV 파일을 업로드하세요 (World Happiness Report 형식)", type=["csv"])

@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()  # 공백 제거
    return df

if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    # 예시 데이터 (2023 World Happiness Report 일부 발췌)
    url = "https://raw.githubusercontent.com/datasets/world-happiness-report/master/data/2023.csv"
    df = pd.read_csv(url)

st.success("✅ 데이터 불러오기 완료!")

# --- 데이터 확인 ---
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# --- 기본 통계 ---
st.subheader("📊 기본 통계 요약")
st.dataframe(df.describe())

# --- 주요 변수 선택 ---
st.sidebar.header("🔍 분석 옵션")
score_col = st.sidebar.selectbox(
    "행복 점수 컬럼 선택",
    [col for col in df.columns if "Score" in col or "score" in col or "Happiness" in col],
)

x_axis = st.sidebar.selectbox(
    "X축 변수 선택", [col for col in df.columns if col != score_col]
)
y_axis = st.sidebar.selectbox(
    "Y축 변수 선택", [col for col in df.columns if col != score_col and col != x_axis]
)

# --- 시각화 1: 행복 점수 vs 선택 변수 ---
st.subheader("💡 행복 점수와 주요 요인 간의 관계")

chart1 = (
    alt.Chart(df)
    .mark_circle(size=80, opacity=0.7)
    .encode(
        x=alt.X(x_axis, title=x_axis),
        y=alt.Y(score_col, title="행복 점수"),
        color=alt.Color(y_axis, scale=alt.Scale(scheme="blues"), title=y_axis),
        tooltip=["Country name", score_col, x_axis, y_axis],
    )
    .interactive()
    .properties(height=450)
)
st.altair_chart(chart1, use_container_width=True)

# --- 시각화 2: 상위 10개 국가 ---
st.subheader("🏆 행복 점수가 높은 국가 TOP 10")

top10 = df.nlargest(10, score_col)[["Country name", score_col]]

chart2 = (
    alt.Chart(top10)
    .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
    .encode(
        y=alt.Y("Country name", sort="-x", title="국가"),
        x=alt.X(score_col, title="행복 점수"),
        color=alt.Color(score_col, scale=alt.Scale(scheme="tealblues")),
        tooltip=["Country name", score_col],
    )
    .properties(height=400)
)
st.altair_chart(chart2, use_container_width=True)

# --- 시각화 3: 대륙별 평균 행복 점수 ---
if "Regional indicator" in df.columns:
    st.subheader("🌍 대륙(지역)별 평균 행복 점수")

    region_mean = (
        df.groupby("Regional indicator")[score_col]
        .mean()
        .reset_index()
        .sort_values(score_col, ascending=False)
    )

    chart3 = (
        alt.Chart(region_mean)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X(score_col, title="평균 행복 점수"),
            y=alt.Y("Regional indicator", sort="-x", title="지역"),
            color=alt.Color(score_col, scale=alt.Scale(scheme="greens")),
            tooltip=["Regional indicator", score_col],
        )
        .properties(height=400)
    )
    st.altair_chart(chart3, use_container_width=True)

st.caption("📘 데이터 출처: World Happiness Report (https://worldhappiness.report)")
