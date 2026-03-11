import streamlit as st

st.set_page_config(
    page_title="Foresttree 대시보드",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Foresttree 통합 대시보드")
st.markdown("---")

st.subheader("메뉴 안내")
st.write("왼쪽 사이드바에서 원하는 메뉴를 선택하세요.")

st.markdown(
"""
### 메뉴
- 가락시장 경매시세
- 매출 분석
- 미수 관리
- 플랫폼 가격 비교
"""
)