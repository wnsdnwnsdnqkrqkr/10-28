import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="세계 행복 지수 다중 요인 분석", layout="wide")

st.title("🌏 세계 행복 지수 다중 요인 분석 대시보드")
st.markdown("""
이 앱은 **World Happiness Report** 데이터를 기반으로  
여러 사회적 요인(GDP, 자유, 기대수명 등)과 **행복 점수의 관계**를 한눈에 비교합니다.  
""")

# --- 데이터 업로드 ---
st.sidebar.header("📂 데이터 업로드")
uploaded_file = st.sidebar.file_uploader("CSV 파일을 업로드하세요 (World Happiness Report 형식)", type=["csv"])

@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    return df

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.success("✅ 데이터 업로드 완료!")
else:
    st.warning("⚠️ CSV 파일을 업로드해주세요. (World Happiness Report 형식)")
    st.stop()

# --- 행복 점수 컬럼 자동 탐색 ---
score_candidates = [col for col in df.columns if "Score" in col or "Happiness" in col]
if len(score_candidates) == 0:
    st.error("❌ 행복 점수 컬럼을 찾을 수 없습니다. (예: 'Happiness score')")
    st.stop()

score_col = st.sidebar.selectbox("행복 점수 컬럼 선택", score_candidates)

# --- 다중 요인 선택 ---
numeric_cols = df.select_dtypes(include=["float", "int"]).columns.tolist()
numeric_cols = [col for col in numeric_cols if col != score_col]

selected_factors = st.sidebar.multiselect(
    "분석할 요인(변수)을 여러 개 선택하세요",
    options=numeric_cols,
    default=numeric_cols[:3],  # 처음엔 3개만 기본으로 보여줌
)

if not selected_factors:
    st.warning("📊 최소 한 개 이상의 요인을 선택하세요.")
    st.stop()

st.subheader(f"💡 '{score_col}'과(와) 선택한 요인들의 관계")

# --- Altair를 이용해 여러 그래프 나란히 표시 ---
charts = []
for factor in selected_factors:
    chart = (
        alt.Chart(df)
        .mark_circle(size=70, opacity=0.7)
        .encode(
            x=alt.X(factor, title=factor),
            y=alt.Y(score_col, title="행복 점수"),
            color=alt.Color(factor, scale=alt.Scale(scheme="blues"), title=factor),
            tooltip=["Country name", score_col, factor],
        )
        .properties(width=300, height=300, title=f"행복 점수 vs {factor}")
        .interactive()
    )
    charts.append(chart)

# --- 여러 그래프를 가로로 합치기 ---
combined_chart = alt.hconcat(*charts)
st.altair_chart(combined_chart, use_container_width=True)

# --- 상위 10개 국가 ---
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

# --- 대륙별 평균 행복 점수 ---
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
