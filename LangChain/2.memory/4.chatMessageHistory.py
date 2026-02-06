from callfunction import *
#추가 (X)->MessagePlaceholder=>ChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory #대화기록 관리해주는 클래스
from langchain_openai import OpenAI

#1.LLM 초기화
llm = OpenAI(temperature=0.5)#평범

#대화 기록 객체 생성
history = ChatMessageHistory()

#기능=>함수(=직원)=>데이터를 출력용
#
# 1.매개변수 X    반환값 X =>단순,반복적인 일
# 1.매개변수 O    반환값 X(보고 X)=>데이터 저장 목적,계산목적(재정=>금액) return X
# 1.매개변수 O    반환값 O =>계산목적(=보고) return 보고서
def show_history(): #def 함수명() or (매개변수명,,): =>work function()=>협업=>함수들이 순서따라서 호출->실행(Agent)
    """현재까지의 대화기록을 보기 좋게 출력"""
    print("\n==대화기록===")
    #for 출력변수 in 출력대상자(=객체):
    for msg in history.messages: #저장된 데이터 출력
        #구분
        role = "사용자" if msg.type == "human" else "AI" #메시지타입을 구분 human=>사용자, 아니면 AI
        print(f"{role}: {msg.content}")
    print("======================\n") #경계선
    
def main(): #caller function(업무를 지시하는 직장상사)=>직원명(매개변수명,,,,)으로 호출=>입력받아서 저장
    print("대화를 시작합니다.'exit' 입력시 종료됩니다.")
    while True:
        user_input = input(">>>")
        if user_input.lower() == "exit":
            print("프로그램을 종료합니다.")
            break
        #사용자 메시지 기록
        history.add_user_message(user_input)
        
        #LLM 응답생성
        ai_response = llm.invoke(user_input)
        
        #AI 메시지 기록
        history.add_ai_message(ai_response)
        
        #응답출력
        print(f"AI: {ai_response}")
        
        #대화 기록 출력
        show_history()
        
# 함수가 없는경우=>그냥 실행 OK
# 함수가 있는경우=>모듈형태로 많이 사용한다.->1.현재파일에서 실행시키는 경우    2.외부에서 모듈로 사용하는 경우 
# #현재 파일에서 main()함수를 부른다면=>외부에서 부르는경우 X 
if __name__ == "__main__":  # from chat~  import main,show_history =>__name__ =X __main__
    main() 
    print('__name__=>',__name__) #exit할때 main()함수가 종료가 되어야 그 다음문장을 실행
    