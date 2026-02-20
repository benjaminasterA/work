import streamlit as st  # 웹 페이지 UI 구성을 위한 메인 라이브러리
import operator  # 데이터를 누적(더하기)할 때 사용하는 연산 도구
from typing import Annotated, TypedDict  # 데이터 타입을 엄격하게 정의하는 도구
from langgraph.graph import StateGraph, END  # 랭그래프의 그래프 구조와 종료 지점
from PIL import Image, ImageDraw, ImageFont  # 이미지를 생성하고 글씨/도형을 그리는 도구
from io import BytesIO  # 이미지를 메모리 상에서 데이터로 변환할 때 사용

# --- [1단계] 공용 게시판(State) 정의 ---
class ChefState(TypedDict):
    """모든 부서가 공유하는 업무 일지입니다."""
    messages: Annotated[list[str], operator.add]        # 대화 기록을 누적 저장
    execution_path: Annotated[list[str], operator.add]  # 어떤 부서를 거쳤는지 기록
    scores: Annotated[list[int], operator.add]          # 각 부서가 남긴 점수 기록
    errors: Annotated[list[str], operator.add]          # 에러 발생 기록도 누적 저장

# --- [2단계] 각 부서(Node) 정의 ---
def planner_node(state: ChefState):
    """[기획부] 메뉴 계획을 세우는 부서"""
    return {
        "messages": ["기획부: 오늘의 업무 계획을 세웠습니다."],
        "execution_path": ["기획부(Planner)"],  # 경로 기록
        "scores": [10],   # 기획 점수
        "errors": [""]    # 에러 없음 → 빈 문자열로 기록 (인덱스 맞추기 위해)
    }

def cook_node(state: ChefState):
    """[제작부] 요리를 담당하는 부서"""
    return {
        "messages": ["제작부: 주문하신 요리를 완성했습니다."],
        "execution_path": ["제작부(Cook)"],  # 경로 기록
        "scores": [30],   # 조리 점수
        "errors": ["조리 실패: 재료 부족"]  # 에러 발생 예시
    }

def reviewer_node(state: ChefState):
    """[검수부] 최종 품질 검사를 담당하는 부서"""
    return {
        "messages": ["검수부: 품질 검사를 마쳤습니다. 완벽합니다!"],
        "execution_path": ["검수부(Reviewer)"],  # 경로 기록
        "scores": [20],   # 검수 점수
        "errors": [""]    # 에러 없음
    }

def error_handler_node(state: ChefState):
    """[에러 처리부] 에러가 발생했을 때 처리하는 부서"""
    return {
        "messages": ["⚠️ 시스템 알림: 에러가 발생하여 작업을 중단합니다."],
        "execution_path": ["에러 처리(Error Handler)"],  # 에러 처리 경로 기록
        "scores": [0],    # 에러 처리 노드는 점수 없음
        "errors": [""]    # 여기서는 새로운 에러를 추가하지 않음 (중복 방지)
    }

# --- [3단계] 시각화 함수 ---
def draw_path_map(path_list, score_list, error_list):
    """부서 경로와 점수를 함께 시각화 (에러 메시지도 박스 안에 표시)"""
    img = Image.new('RGB', (1000, 250), color=(255, 255, 255))  # 도화지 생성
    d = ImageDraw.Draw(img)  # 붓 준비
    
    # 한글 폰트 설정
    try: 
        font = ImageFont.truetype("./font/NotoSansCJKkr-Regular.otf", 15)
    except: 
        font = ImageFont.load_default()

    x = 50  # 첫 번째 상자 시작 위치
    for i, node_name in enumerate(path_list):
        # 네모 상자 그리기
        d.rectangle([x, 50, x+200, 130], outline=(0,0,0), width=2)
        
        # 부서 이름 출력
        d.text((x+20, 55), f"{i+1}. {node_name}", font=font, fill=(0,0,0))
        
        # 점수 출력
        if i < len(score_list):
            d.text((x+20, 75), f"점수: {score_list[i]}", font=font, fill=(0,0,255))
        
        # 에러 메시지 출력
        if i < len(error_list) and error_list[i]:
            d.text((x+20, 95), f"에러: {error_list[i]}", font=font, fill=(255,0,0))
        
        # 화살표 연결
        if i < len(path_list) - 1:
            d.line([x+200, 90, x+240, 90], fill=(255,0,0), width=3)
        
        x += 240  # 다음 상자 위치 이동

    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# --- [4단계] 워크플로우 구성 ---
workflow = StateGraph(ChefState)  # 워크플로우 선언
workflow.add_node("planner", planner_node)
workflow.add_node("cook", cook_node)
workflow.add_node("reviewer", reviewer_node)
workflow.add_node("error_handler", error_handler_node)

workflow.set_entry_point("planner")  # 시작은 기획부
workflow.add_edge("planner", "cook")  # 기획 → 조리

# 조건부 분기: cook에서 에러 발생 시 error_handler로, 아니면 reviewer로
workflow.add_conditional_edges("cook", lambda state: "error_handler" if any(state["errors"]) else "reviewer")

workflow.add_edge("reviewer", END)          # 검수 → 종료
workflow.add_edge("error_handler", END)     # 에러 처리 → 종료

app = workflow.compile()  # 실행 가능한 앱으로 컴파일

# --- [5단계] Streamlit 출력 ---
st.title("⚠️ 에이전트 실패 처리 시스템 (에러 박스 안 표시)")
if st.button("시스템 가동"):
    # scores와 errors 모두 초기화
    result = app.invoke({"messages": [], "execution_path": [], "scores": [], "errors": []})

    st.subheader("📝 업무 기록")
    for msg in result["messages"]:
        st.info(msg)

    # 에러 로그는 중복 없이 실제 에러만 출력
    if any(result["errors"]):
        st.subheader("❌ 에러 로그")
        for err in result["errors"]:
            if err:  # 빈 문자열은 출력하지 않음
                st.error(err)

    st.subheader("🗺️ 협업 로드맵 (점수 + 에러 포함)")
    path_img_data = draw_path_map(result["execution_path"], result["scores"], result["errors"])
    st.image(path_img_data)

    st.download_button(
        label="📂 협업 로드맵 저장하기",
        data=path_img_data,
        file_name="collaboration_map.png",
        mime="image/png"
    )
