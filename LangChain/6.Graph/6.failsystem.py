#1.plantest.py# 어떤 요리 기획?
import streamlit as st #django=>웹프로그래밍(파이썬으로 되어있다.)
from typing import Annotated,TypedDict #데이터 타입 정의 도구 =>모든 부서가 공통으로 사용하는 메세지들
# 요리점->공용게시판(주문내역(1번,2번,,,,))

import operator # 주문내역의 메세지들을 차곡차곡 (누적해서 쌓아준다.)+ 연산 
from langgraph.graph import StateGraph,END # 부서들간의 흐름도(시작->부서의 이동->종료(END))
##################추가############################################
from PIL import Image,ImageDraw,ImageFont #이미지를 파일로 저장할때 사용
from io  import BytesIO #이미지를 메모리상에서 데이터로 변환할때 사용
##################################################################

#1단계.공용게시판(State) 만들기(실행경로(path) 기록하는 칸 추가)->데이터 저장,저장확인

class ChefState(TypedDict): 
    #속성값 or 메서드명       
    messages:Annotated[list[str],operator.add]#문자형의 데이터를 차곡차곡 쌓아서 저장                                                              2.메서드 호출
    # [핵심] 어떤 부서가 방문했는지 '발도장'을 찍어서 기록하는 리스트
    execution_path:Annotated[list[str],operator.add] #CCTV
    # 추가
    scores:Annotated[list[int],operator.add]#int (숫자) =>각 부서 점수 기록
    # 추가2
    errors:Annotated[list[str],operator.add]#에러 발생 기록
    
#2단계.각 부서(=Node)의 업무 정의하기

#1.기획부
def planner_node(state : ChefState): #변수명:자료형(=어떤 데이터 종류(float)와 범위(소수점)를 지정)
    """[기획부] 메뉴 계획을 세우고, 자신이 일했다는 증거(path)를 남깁니다."""
    return {
           "messages":["기획부:오늘의 업무 계획을 세웠습니다."],
           "execution_path":["기획부(Planner)"],
           #추가
           "scores":[10], #기획 점수(내부평가에 의해서 점수가 부여(임의로 준상황))
           "errors":[]    #에러 없음.
           }

#2.제작부
def cook_node(state : ChefState): 
    """[제작부] 요리를 완성하고,자신이 일했다는 증거(path)를 남깁니다. """
    return {
            "messages":["제작부:주문하신 요리를 완성했습니다."],
            "execution_path":["제작부(cook)"],
            "scores":[30], #제작 점수
            "errors":["조리 실패: 재료 부족"] #에러 발생 예시 
           }

# - 검수부
def reviewer_node(state : ChefState): 
    """[검수부] 최종 확인(check)을 하고,마지막 발자취를 남깁니다. """
    return {
        "messages":["검수부:품질 검사를 마쳤습니다. 완벽합니다."],
        "execution_path":["검수부(Reviewer)"], #마지막 검수 완료 기록
        "scores":[20], #검수 점수
        "errors":[]    #에러 없음.
        }
    
##########################################################################
# 위기 관리부 성격(=error_handler_node)
def error_handler_node(state: ChefState):
    """[에러 처리부] 에러가 발생했을때 처리하는 부서"""
    return {
        "messages":["시스템 알림: 에러가 발생하여 작업을 중단합니다."],
        "execution_path":["에러 처리(Error Handler)"], # 에러 처리 경로 기록
        "scores":[0], # 에러 처리 노드는 점수는 없음
        "errors": state["errors"] #기존 에러 기록 전달
    }
############################################################################   
#어떤부서가 방문했는지 화면에 출력->매개변수 X   반환값 X ->단순,반복
# 3단계                             매개변수(부서명) 반환값 O =>입력을 받아서 처리하는 경우(계산,저장)

def draw_path_map(path_list,score_list,error_list): #error_list 추가
    """ 부서 경로와 점수를 함께 시각화 (에러메세지도 박스 안에 표시)"""
    
    #1.도화지(800*150) color (흰색)
    img = Image.new('RGB',(1000,250),color=(255,255,255))
    d = ImageDraw.Draw(img) #붓
    #2.한글이 깨지지 않도록 폰트 설정
    try:
            font = ImageFont.truetype("./font/NotoSansCJKkr-Regular.otf")
    except:
            font = ImageFont.load_default()
            
    x = 50 #첫번째 상자를 그릴 시작 위치 (가로:좌표)
    for i,node_name in enumerate(path_list):
        # 1.부서이름이 들어갈 네모 상자를 그린다.(x=50,y=50,width=200,h=100)
        d.rectangle([x,50,x+200,130],outline=(0,0,0),width=2) #굵기
        # 2.상자안에 부서 이름을 써야된다.(x좌표만 이동하고 y좌표는 고정)
        d.text((x+20,55),f"{i+1},{node_name}",font=font,fill=(0,0,0))
        #############################################################
        # 추가(점수를 출력)
        if i < len(score_list):
            d.text((x+20,75),f"점수:{score_list[i]}",font=font,fill=(0,0,255))
        ##############################################################
        # 에러메세지 출력(에러가 있을 경우에만 박스안에 표시)
        if i < len(error_list) and error_list[i]:
            d.text((x+20,95),f"에러:{error_list[i]}",font=font,fill=(255,0,0))
        ##############################################################
        #빨간색 화살표 그리기(if 다른 부서가 있다면)
        if i < len(path_list) - 1: #맨마지막 상자뒤에는 화살표그릴 수 없기때문에 -1(0<2,1<2,2<2(X))
            d.line([x+200,90,x+240,90],fill=(255,0,0),width=3)
        x += 240 #다음 상자를 위해 가로 위치를 옆으로 이동한다. 
        
    #완성된 이미지를 컴퓨터가 읽을 수 있은 바이트 데이터로 변환
    buf = BytesIO()
    img.save(buf,format="PNG")
    return buf.getvalue() #그림 데이터를 반환
            
#4단계 부서 배치(=Graph) 연결

#1.우리 식당의 업무 지도(Graph)를 그리기 시작
workflow = StateGraph(ChefState)

#2.식당에 부서들을 배치합니다.(Node 추가(=부서 추가))
workflow.add_node("planner",planner_node)#(부서를 의미 키를 부여,함수이름(부서))
workflow.add_node("cook",cook_node) # 제작부 배치
workflow.add_node("reviewer",reviewer_node) # 검수부 (새로 추가된 부서)
workflow.add_node("error_handler",error_handler_node)

#3.부서간의 이동 경로를 설정한다.(=Edge 연결)
workflow.set_entry_point("planner")# 모든일은 '기획부'에서 시작한다.
workflow.add_edge("planner","cook")# (1.지금 시작하는 부서명,다음에 시작할 부서명)
#workflow.add_edge("cook","reviewer")# 제작이 끝나면 reviewer로 업무이동(=전이)->조건분기가 X

# def get_role(state):
#     if state["errors"]: #에러가 발생이 되면
#         return "error_handler" 반환값
#     else:
#         return "reviewer" #정상이라면
#조건부 분기:cook에서 에러 발생시 error_handler로 or reviewer  lamda 매개변수명: 참 if 조건식 거짓
workflow.add_conditional_edges("cook",lambda state: "error_handler" if state["errors"] else "reviewer")
#########################################################
workflow.add_edge("reviewer",END) # 일반적인 일처리 -> 종료(종)
#추가
workflow.add_edge("error_handler",END) # 에러 처리 ->종료(비정상)

#4.설계도를 실제 실행 가능한 앱으로 만든다.
app = workflow.compile()

#4.실제로 시스템 가동하기
st.title("에이전트 실패 처리 시스템(에러 박스안 표시)")
st.write("멀티 에이전트의 협업과정을 로드맵으로 확인해보세요")

if st.button("전 부서 대기 시스템 가동!"):
    #초기 게시판의 내용을 비워서 업무를 시작################################추가##########
    initial_state = {"messages":[],"execution_path":[],"scores":[],"errors":[]}
    
    #지도를 따라서 부서별로 일이 진행되게 한다.
    result = app.invoke(initial_state)
    ################################################
    #1.텍스트로 된 업무 기록 출력
    st.subheader("업무 기록 일지")
    for msg in result["messages"]:
        st.info(msg)
    
    if result["errors"]:
        st.subheader("에러 로그")
        for err in result["errors"]:
            st.error(err)
    ################################################
    st.divider() #경계선
    st.subheader("실시간 협업 로드")
    #게시판에 기록된 'execution_path'를 가져와서 그림을 그림
    path_img_data = draw_path_map(result["execution_path"],result["scores"],
                                  result["errors"])#keyerror(오류)
    st.image(path_img_data) #화면에 로드맵 표시
    
    #사용자가 로드맵을 소장할 수 있도록 다운로드 기능
    st.download_button(
        label='협업 로드맵 저장하기',
        data = path_img_data,
        file_name = "collaboration_map.png",
        mime = "image/png"
    )
    #streamlit run 6.failsystem.py
          