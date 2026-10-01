import json
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="형사 사건 분석 및 공소장 작성", layout="wide"
)


# 데이터 로드 함수
@st.cache_data
def load_data():
    with open("cases.json", "r", encoding="utf-8") as f:
        return json.load(f)


cases_data = load_data()

# 헤더 영역
st.title("⚖️ 형사 사건 분석 및 공소장 작성 웹앱")
st.caption(
    "진로 분야별 형사 사건을 선택하고 분석하여 공소장을 완성해보세요."
)
st.divider()

# 레이아웃 분할 (좌: 사건 탐색 / 우: 공소장 작성)
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("1. 형사 사건 선택")

    # 카테고리 필터
    categories = list(set(c["category"] for c in cases_data))
    selected_cat = st.selectbox("진로 분야 선택", ["전체"] + categories)

    # 사건 목록 필터링
    filtered_cases = cases_data
    if selected_cat != "전체":
        filtered_cases = [
            c for c in cases_data if c["category"] == selected_cat
        ]

    # 사건 선택
    case_titles = [f"[{c['id']}] {c['title']}" for c in filtered_cases]
    selected_title = st.selectbox("분석할 사건 선택", case_titles)

    # 선택된 사건 가져오기
    selected_id = int(selected_title.split("]")[0].replace("[", ""))
    selected_case = next(c for c in cases_data if c["id"] == selected_id)

    # 사건 상세 안내 카드
    st.info(f"**범죄 개요:**\n{selected_case['summary']}")
    st.warning(f"**💡 참고 법조문 힌트:**\n{selected_case['law_hint']}")

    st.markdown("**🔍 핵심 분석 체크포인트:**")
    for kp in selected_case["key_points"]:
        st.write(f"- {kp}")

with col2:
    st.subheader("2. 공소장 작성 양식")

    # 입력 폼
    student_info = st.text_input(
        "작성자 (학년 반 번호 이름)", placeholder="2학년 1반 00번 홍길동"
    )
    accused_name = st.text_input(
        "피고인 성명/인적사항", placeholder="피고인 A (남, 18세)"
    )
    crime_name = st.text_input(
        "죄명", placeholder="예: 허위영상물유포, 정보통신망법위반(명예훼손)"
    )
    applied_laws = st.text_input("적용법조", value=selected_case["law_hint"])

    facts = st.text_area(
        "범죄사실 (일시, 장소, 범죄 행위 요석을 구체적으로 작성)",
        height=200,
        placeholder="피고인은 2026년 0월 0일경...",
    )

    # 완성된 공소장 텍스트 구성
    indictment_text = f"""[ 공 소 장 ]

1. 작성자: {student_info}
2. 피고인: {accused_name}
3. 죄  명: {crime_name}
4. 적용법조: {applied_laws}

5. 범죄사실:
{facts}
"""

    # 결과 다운로드 버튼
    st.download_button(
        label="📄 공소장 텍스트 파일로 다운로드",
        data=indictment_text,
        file_name=f"공소장_{student_info}.txt",
        mime="text/plain",
    )
