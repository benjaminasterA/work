#1.plantest.py# 어떤 요리 기획?
import streamlit as st #django=>웹프로그래밍(파이썬으로 되어있다.)
from typing import Annotated,TypedDict #데이터 타입 정의 도구 =>모든 부서가 공통으로 사용하는 메세지들
# 요리점->공용게시판(주문내역(1번,2번,,,,))

import operator # 주문내역의 메세지들을 차곡차곡 (누적해서 쌓아준다.)+ 연산 
from langgraph.graph import StateGraph,END # 부서들간의 흐름도(시작->부서의 이동->종료(END))

#1단계.공용게시판(State) 만들기(모든 부서가 같이 보고 내용을 적는 공유 문서 (회사))->데이터 저장,저장확인
# 상속(속성과메서드를 상속받음=>소유권 이전) =>정확하게 원하는 데이터저장? 확인가능
# TypedDict=>1.타입 명확성,2.타입검사 3.상태(State)데이터의 일관성 보장
class ChefState(TypedDict): # class 사용자정의 자료형(=클래스이름)(상속받을 부모클래스명)
    #속성값 or 메서드명       #클래스를 작성하는 이유->객체를 생성하기위해 ->1.데이터저장 목적
    messages:Annotated[list[str],operator.add]#문자형의 데이터를 차곡차곡 쌓아서 저장                                                              2.메서드 호출
    
#2단계.각 부서(=Node)의 업무 정의하기

#1.기획부
def planning_department(state : ChefState): #변수명:자료형(=어떤 데이터 종류(float)와 범위(소수점)를 지정)
    """[기획부서] 사용자의 요청을 보고 무엇을 할지 계획을 세웁니다. """
    st.write(" **[기획부]** 손님이 다양한 케이크를 원하시네,레시피를 찾아야겠다.")
    #게시판에 기획 완료 메세지를 추가
    return {"messages":["기획부:고구마 케이크 레시피 찾기 계획 수립"]}

#2.제작부서
def cooking_department(state : ChefState): 
    """[제작부서] 기획서가 넘어오면 실제로 요리(실행)를 합니다. """
    st.write(" **[제작부]** 기획서 확인 완료! 지금 바로 케이크를 만듭니다.")
    #게시판에 제작 완료 메세지를 추가
    return {"messages":["제작부:달콤한 고구마 케이크 완성!!!"]}

#3단계 부서 배치 및 결재 라인(=Graph) 연결

#1.우리 식당의 업무 지도(Graph)를 그리기 시작
workflow = StateGraph(ChefState)

#2.식당에 부서들을 배치합니다.(Node 추가(=부서 추가))
workflow.add_node("planner",planning_department)#(부서를 의미 키를 부여,함수이름(부서))
workflow.add_node("cook",cooking_department) # 제작부 배치

#3.부서간의 이동 경로를 설정한다.(=Edge 연결)
workflow.set_entry_point("planner")# 모든일은 '기획부'에서 시작한다.
workflow.add_edge("planner","cook")# (1.지금 시작하는 부서명,다음에 시작할 부서명)
workflow.add_edge("cook",END)# 제작이 끝나면 그 다음부서가 없으면 END(업무 종료)

#4.설계도를 실제 실행 가능한 앱으로 만든다.
app = workflow.compile()

#4.실제로 시스템 가동하기
st.title("분업 시스템(LangGraph)")

if st.button("협업 시스템 가동!"):
    #초기 게시판의 내용을 비워서 업무를 시작
    initial_state = {"messages":[]}
    
    #지도를 따라서 부서별로 일이 진행되게 한다.
    final_outcome = app.invoke(initial_state)
    
    st.divider() #경계선
    st.subheader("공용 게시판 최종 기록")
    #모든 부서가 기록한 내용을 화면에 출력
    for msg in final_outcome["messages"]:
        st.write(msg)
 #streamlit run 1.plantest.py       