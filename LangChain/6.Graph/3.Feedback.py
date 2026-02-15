#1.plantest.py# 어떤 요리 기획?
import streamlit as st #django=>웹프로그래밍(파이썬으로 되어있다.)
from typing import Annotated,TypedDict #데이터 타입 정의 도구 =>모든 부서가 공통으로 사용하는 메세지들
# 요리점->공용게시판(주문내역(1번,2번,,,,))
import random # 검수 통과 여부를 무작위로 결정하기위해서 필요
import operator # 주문내역의 메세지들을 차곡차곡 (누적해서 쌓아준다.)+ 연산 
from langgraph.graph import StateGraph,END # 부서들간의 흐름도(시작->부서의 이동->종료(END))

#1단계.공용게시판(State) 만들기(모든 부서가 같이 보고 내용을 적는 공유 문서 (회사))->데이터 저장,저장확인
# 상속(속성과메서드를 상속받음=>소유권 이전) =>정확하게 원하는 데이터저장? 확인가능
# TypedDict=>1.타입 명확성,2.타입검사 3.상태(State)데이터의 일관성 보장
class ChefState(TypedDict): # class 사용자정의 자료형(=클래스이름)(상속받을 부모클래스명)
    """ 부서원들이 공유하는 업무 일지입니다."""
    #속성값 or 메서드명       #클래스를 작성하는 이유->객체를 생성하기위해 ->1.데이터저장 목적
    messages:Annotated[list[str],operator.add]#문자형의 데이터를 차곡차곡 쌓아서 저장                                                              2.메서드 호출
    # 요리를 몇 번 다시 시도했는지 숫자로 기록하여 무한 루프를 방지합니다.
    attempts:int
    
    
#2단계.각 부서(=Node)의 업무 정의하기

#1.기획부
def planning_department(state : ChefState): #변수명:자료형(=어떤 데이터 종류(float)와 범위(소수점)를 지정)
    """[기획부] 메뉴를 정하고 업무를 시작합니다. """
    st.write(" **[기획부]** 오늘의 메뉴는 '매운 떡볶이' 입니다.")
    #게시판에 기획 완료를 적고,시도 횟수를 0으로 초기화하여 전달합니다.
    return {"messages":["기획:매운 떡볶이 기획 완료"],"attempts":0}

#2.제작부서
def cooking_department(state : ChefState): 
    """[제작부] 기획서나 지배인의 피드백을 보고 요리를 만듭니다. """
    #현재 게시판에 적힌 시도 회수를 가져와서 1을 더합니다.
    current_attempt = state.get("attempts",0)+1 #매개변수(객체).get("속성명")=>값을 가져옴
    st.write(f" **[제작부]** {current_attempt}번째 떡볶이를 열심히 만들고 있습니다.")
    #요리한 결과 메세지와 업데이트된 시도 횟수를 게시판에 적습니다.
    return {"messages":[f"제작부: {current_attempt}차 떡볶이 조리 완료!!!"],
            "attempts":current_attempt}

#[신규부서] - 검수 부서
def reviewer_department(state : ChefState): 
    """[검수부] 완성된 요리를 먹어보고 품질을 평가합니다. """
    st.write(" **[검수부]** 지배인님이 맛을 보는 중입니다....")
    #검수했다는 사실만 게시판에 기록합니다. 통과 여부는 다음 단계에서 설정
    return {"messages":["검수:지배인님이 시식함!!!"]}

# 길을 건너가는 신호등 함수(중요!!)
def should_continue(state : ChefState):
    """ 지배인의 판단에 따라 다음 부서로 보낼지,일을 끝낼지 결정합니다."""
    #Random함수를 이용 True(합격),False(불합격)=>횟수가 3번이상면 통과
    quality_pass = random.choice([True,False])
    # 3번이상이면 통과
    if state["attempts"] >=3 :
        st.warning("(지배인):시간이 너무 지체됐군요. 이번에는 그냥 손님에게 드려주세요")
        return "finish" # 'finish' 라는 신호를 보냅니다.
    
    #품질 검사를 통과하는경우
    if quality_pass: # == True와 동일(생략)
        st.success("(지배인) : 맛이 훌륭합니다.! 퇴근하세요 ")
        return "finish"
    else:
        st.error("(지배인) : 너무 짜요! 다시 만들어 오세요!")
        return "retry" #프로젝트할때 항상(전날) 백업
    

#3단계 부서 배치 및 결재 라인(=Graph) 연결

#1.우리 식당의 업무 지도(Graph)를 그리기 시작
workflow = StateGraph(ChefState)

#2.식당에 부서들을 배치합니다.(Node 추가(=부서 추가))
workflow.add_node("planner",planning_department)#(부서를 의미 키를 부여,함수이름(부서))
workflow.add_node("cook",cooking_department) # 제작부 배치
workflow.add_node("reviewer",reviewer_department) # 검수부 (새로 추가된 부서)
#추가(배달)
#3.부서간의 이동 경로를 설정한다.(=Edge 연결)
workflow.set_entry_point("planner")# 모든일은 '기획부'에서 시작한다.
workflow.add_edge("planner","cook")# (1.지금 시작하는 부서명,다음에 시작할 부서명)
workflow.add_edge("cook","reviewer")# 제작이 끝나면 reviewer로 업무이동(=전이)
workflow.add_edge("reviewer",END)

#[핵심] 검수부에서 다음에는 조건에 따라 조건에 따라 분기(갈라지는 부분)=>기획-cook
workflow.add_conditional_edges(
    "reviewer",  #출발지:검수부=>1.조건을 검사하는 부서명
    should_continue,  #2.조건을 검사하는 함수명
    {
        "retry":"cook", #함수가 'retry'를 반환하면 조리부(cook)로 복귀
        "finish":END   #함수가 'finish'를 반환하면 업무종료(END)
    } 
)
#4.설계도를 실제 실행 가능한 앱으로 만든다.
app = workflow.compile()

#4.실제로 시스템 가동하기
st.title("조건부 이동(Loop & Feedback)")
st.write("기획부 -> 제작부 ->검수부로 이어지는 '멀티 에이전트'의 흐름을 확인해보세요")

if st.button("협업 주방 가동!"):
    #초기 게시판의 내용을 비워서 업무를 시작
    initial_state = {"messages":[],"attempts":0}
    
    #지도를 따라서 부서별로 일이 진행되게 한다.
    final_result = app.invoke(initial_state)#~invoke({"messages":[],"attempts":0})
    
    st.divider() #경계선
    st.subheader("최종 업무 히스토리")
    #모든 부서가 기록한 내용을 화면에 출력
    for i,msg in enumerate(final_result["messages"]):
        st.write(f"{i+1}단계:{msg}")
 #streamlit run 3.Feedback.py       