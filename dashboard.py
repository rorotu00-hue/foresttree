import streamlit as st
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
    st.write("여기에 가락시장 경매시세 데이터를 표시합니다.")
    st.info("다음 단계에서 품목 검색 / 등급별 가격 / 그래프를 붙이면 됩니다.")

elif menu == "매출 분석":
    st.header("매출 분석")
    st.write("여기에 매출 분석 내용을 표시합니다.")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("이번 달 매출", "0원")
    with col2:
        st.metric("전월 대비", "0%")

elif menu == "미수 관리":
    st.header("미수 관리")
    st.write("여기에 미수 관리 내용을 표시합니다.")
    st.warning("미수금 현황 표와 거래처별 미수금 합계를 붙일 수 있습니다.")

elif menu == "플랫폼 가격 비교":
    st.header("플랫폼 가격 비교")
    st.write("여기에 플랫폼 가격 비교 내용을 표시합니다.")
    st.success("스마트스토어 / 쿠팡 / 기타 플랫폼 비교 테이블을 붙일 수 있습니다.")

