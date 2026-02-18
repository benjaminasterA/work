# (pip install streamlit langgraph pillow)
# 웹 페이지 UI 구성을 위한 메인 라이브러리 임포트
import streamlit as st
# 데이터를 누적(더하기)할 때 사용하는 연산 도구 임포트
import operator
# 데이터 타입을 엄격하게 정의하는 도구 임포트
from typing import Annotated, TypedDict
# 랭그래프의 그래프 구조와 종료 지점 임포트
from langgraph.graph import StateGraph, END
# 이미지를 생성하고 글씨/도형을 그리는 도구 임포트
from PIL import Image, ImageDraw, ImageFont
# 이미지를 메모리 상에서 데이터로 변환할 때 사용
from io import BytesIO
# 운영체제(OS) 확인을 위한 모듈 임포트
import platform

# --- [1단계] 공용 게시판(State) 정의 ---
class ChefState(TypedDict):
    # 대화 기록 리스트 누적 저장
    messages: Annotated[list[str], operator.add]
    # 어떤 부서를 거쳤는지 경로 리스트 누적 기록
    execution_path: Annotated[list[str], operator.add]
    # 각 부서가 남긴 점수 리스트 누적 기록
    scores: Annotated[list[int], operator.add]
    # 에러 발생 상황 리스트 누적 기록
    errors: Annotated[list[str], operator.add]

# --- [2단계] 각 부서(Node) 정의 ---
def planner_node(state: ChefState):
    # 기획부 업무 결과 데이터 반환
    return {
        "messages": ["기획부: 오늘의 업무 계획을 세웠습니다."],
        "execution_path": ["기획부(Planner)"],
        "scores": [10],
        "errors": []
    }

def cook_node(state: ChefState):
    # 제작부 업무 결과 데이터 반환
    return {
        "messages": ["제작부: 주문하신 요리를 완성했습니다."],
        "execution_path": ["제작부(Cook)"],
        "scores": [30],
        "errors": []
    }

def marketing_node(state: ChefState):
    # 홍보부 업무 결과 데이터 반환
    return {
        "messages": ["홍보부: 오늘의 메뉴를 SNS에 홍보했습니다."],
        "execution_path": ["홍보부(Marketing)"],
        "scores": [15],
        "errors": []
    }

def reviewer_node(state: ChefState):
    # 검수부 업무 결과 데이터 반환
    return {
        "messages": ["검수부: 품질 검사를 마쳤습니다. 완벽합니다!"],
        "execution_path": ["검수부(Reviewer)"],
        "scores": [20],
        "errors": []
    }

# [신규] 배달부(Delivery) 노드 추가
def delivery_node(state: ChefState):
    # 배달부 업무 결과 데이터 반환
    return {
        "messages": ["배달부: 고객님께 안전하게 배달을 완료했습니다! 🛵"],
        "execution_path": ["배달부(Delivery)"],
        "scores": [25],
        "errors": []
    }

def error_handler_node(state: ChefState):
    # 에러 처리 결과 데이터 반환
    return {
        "messages": ["시스템 알림: 에러가 발생하여 작업을 중단합니다."],
        "execution_path": ["에러 처리(Error Handler)"],
        "scores": [0],
        "errors": state["errors"]
    }

# --- [3단계] 시각화 함수 (한글 폰트 적용) ---
def draw_path_map(path_list, score_list):
    # 노드 증가에 따라 이미지 가로 폭을 1000으로 설정
    img = Image.new('RGB', (1000, 200), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    # OS별 한글 폰트 경로 탐색
    os_name = platform.system()
    font_path = ""
    if os_name == "Windows": font_path = "C:/Windows/Fonts/malgun.ttf"
    elif os_name == "Darwin": font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
    else: font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"

    try: font = ImageFont.truetype(font_path, 15)
    except: font = ImageFont.load_default()

    x = 50
    for i, node_name in enumerate(path_list):
        d.rectangle([x, 50, x+150, 100], outline=(0,0,0), width=2)
        d.text((x+20, 60), f"{i+1}. {node_name}", font=font, fill=(0,0,0))
        if i < len(score_list):
            d.text((x+20, 80), f"점수: {score_list[i]}", font=font, fill=(0,0,255))
        if i < len(path_list) - 1:
            d.line([x+150, 75, x+200, 75], fill=(255,0,0), width=3)
        x += 200

    buf = BytesIO()
    img.save(buf, format="PNG")
    # 이미지 바이너리 데이터 반환
    return buf.getvalue()

# --- [4단계] 워크플로우 구성 ---
workflow = StateGraph(ChefState)
workflow.add_node("planner", planner_node)
workflow.add_node("cook", cook_node)
workflow.add_node("marketing", marketing_node)
workflow.add_node("reviewer", reviewer_node)
workflow.add_node("delivery", delivery_node)
workflow.add_node("error_handler", error_handler_node)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "cook")
workflow.add_edge("planner", "marketing")

workflow.add_conditional_edges("cook", 
                               lambda state: "error_handler" if state["errors"] 
                               else "reviewer")

workflow.add_edge("marketing", "reviewer")
workflow.add_edge("reviewer", "delivery")
workflow.add_edge("delivery", END)
workflow.add_edge("error_handler", END)

app = workflow.compile()

# --- [5단계] Streamlit 출력 및 저장 버튼 ---
st.title("병렬 처리 협업 시스템")
if st.button("시스템 가동"):
    result = app.invoke({"messages": [], "execution_path": [], 
                         "scores": [], "errors": []})

    st.subheader("업무 기록")
    for msg in result["messages"]:
        st.info(msg)

    st.subheader("병렬 협업 로드맵")
    # 시각화 이미지 데이터 생성
    path_img_data = draw_path_map(result["execution_path"], result["scores"])
    # 화면에 이미지 출력
    st.image(path_img_data)

    # [추가] 협업 로드맵 파일 다운로드 버튼
    st.download_button(
        label="협업 로드맵 저장하기",
        data=path_img_data,
        file_name="collaboration_map.png",
        mime="image/png"
    )