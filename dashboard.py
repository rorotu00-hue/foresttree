import streamlit as st
import pandas as pd
import plotly.express as px
from garak_api import get_garak_price

st.set_page_config(
    page_title="Foresttree 통합 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        min-width: 260px !important;
        width: 260px !important;
    }
</style>
""", unsafe_allow_html=True)

menu_list = ["가락시장 경매시세", "매출 분석", "미수 관리", "플랫폼 가격 비교"]

if "menu" not in st.session_state:
    st.session_state.menu = menu_list[0]

with st.sidebar:
    st.title("📋 메뉴")
    st.write("원하는 메뉴를 선택하세요.")
    selected_sidebar = st.radio(
        "메뉴 선택",
        menu_list,
        index=menu_list.index(st.session_state.menu),
        key="sidebar_menu"
    )
    st.session_state.menu = selected_sidebar

st.title("📊 Foresttree 통합 대시보드")
st.caption("사이드바가 안 보이면 아래 본문 메뉴로도 이동할 수 있습니다.")

selected_main = st.selectbox(
    "본문 메뉴 선택",
    menu_list,
    index=menu_list.index(st.session_state.menu),
    key="main_menu"
)

if selected_main != st.session_state.menu:
    st.session_state.menu = selected_main
    st.rerun()

menu = st.session_state.menu

st.divider()

if menu == "가락시장 경매시세":
    st.header("가락시장 경매시세")

    col1, col2 = st.columns([2, 1])

    with col1:
        item = st.text_input("품목 검색", value="대파")

    with col2:
        search_button = st.button("가격 조회", use_container_width=True)

    if search_button or item:
        df = get_garak_price(item)

        if df.empty:
            st.warning("조회된 데이터가 없습니다.")
        else:
            st.subheader(f"'{item}' 조회 결과")

            st.dataframe(df, use_container_width=True)

            if "등급" in df.columns and "가격" in df.columns:
                chart_df = df.copy()
                chart_df["가격"] = pd.to_numeric(chart_df["가격"], errors="coerce")
                chart_df = chart_df.dropna(subset=["가격"])

                if not chart_df.empty:
                    fig = px.bar(
                        chart_df,
                        x="등급",
                        y="가격",
                        text="가격",
                        title=f"{item} 등급별 가격"
                    )
                    fig.update_traces(textposition="outside")
                    st.plotly_chart(fig, use_container_width=True)

            st.subheader("요약 정보")

            summary_col1, summary_col2, summary_col3 = st.columns(3)

            price_series = pd.to_numeric(df["가격"], errors="coerce")

            with summary_col1:
                if not price_series.dropna().empty:
                    st.metric("최고가", f"{int(price_series.max()):,}원")
                else:
                    st.metric("최고가", "-")

            with summary_col2:
                if not price_series.dropna().empty:
                    st.metric("최저가", f"{int(price_series.min()):,}원")
                else:
                    st.metric("최저가", "-")

            with summary_col3:
                if not price_series.dropna().empty:
                    st.metric("평균가", f"{int(price_series.mean()):,}원")
                else:
                    st.metric("평균가", "-")

elif menu == "매출 분석":
    st.header("매출 분석")
    st.write("여기에 매출 분석 내용을 표시합니다.")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("이번 달 매출", "0원")
    with col2:
        st.metric("전월 대비", "0%")

    sample_sales = pd.DataFrame({
        "월": ["1월", "2월", "3월", "4월", "5월"],
        "매출": [100, 140, 120, 180, 160]
    })

    fig = px.line(sample_sales, x="월", y="매출", markers=True, title="월별 매출 추이")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "미수 관리":
    st.header("미수 관리")
    st.write("여기에 미수 관리 내용을 표시합니다.")

    sample_unpaid = pd.DataFrame({
        "거래처": ["A업체", "B업체", "C업체"],
        "미수금": [1200000, 850000, 430000]
    })

    st.dataframe(sample_unpaid, use_container_width=True)

elif menu == "플랫폼 가격 비교":
    st.header("플랫폼 가격 비교")
    st.write("여기에 플랫폼 가격 비교 내용을 표시합니다.")

    sample_compare = pd.DataFrame({
        "품목": ["대파", "양파", "감자"],
        "자사": [3200, 2800, 4500],
        "쿠팡": [3300, 2750, 4700],
        "스마트스토어": [3250, 2900, 4600]
    })

    st.dataframe(sample_compare, use_container_width=True)
