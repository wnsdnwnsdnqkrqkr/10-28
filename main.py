import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="MBTI 국가 분석", layout="wide")

st.title("🌎 MBTI 유형별 국가 분석 대시보드")
st.markdown("특정 MBTI 유형이 높은 국가 TOP 10을 시각적으로 분석합니다.")

# --- 데이터 업로드 ---
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.success("✅ 데이터 업로드 완료!")

    # --- 데이터 확인 ---
    st.subheader("데이터 미리보기")
    st.dataframe(df.head())

    # --- MBTI 유형 선택 ---
    mbti_columns = [col for col in df.columns if col not in ["Country", "Country Code", "Region"]]
    selected_type = st.selectbox("분석할 MBTI 유형을 선택하세요", mbti_columns)

    # --- 상위 10개 국가 ---
    top10 = df.nlargest(10, selected_type)[["Country", selected_type]]

    st.subheader(f"🌟 {selected_type} 유형 비율이 높은 국가 TOP 10")
    
    chart = (
        alt.Chart(top10)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X(selected_type, title=f"{selected_type} 비율"),
            y=alt.Y("Country", sort="-x", title="국가"),
            color=alt.Color(selected_type, scale=alt.Scale(scheme="tealblues")),
            tooltip=["Country", selected_type]
        )
        .properties(height=400)
    )

    st.altair_chart(chart, use_container_width=True)

    # --- 추가 정보 ---
    st.caption("💡 업로드한 CSV 파일에는 'Country'와 MBTI 유형별 비율 컬럼이 포함되어야 합니다.")
else:
    st.info("👆 CSV 파일을 업로드하면 분석이 시작됩니다.")
