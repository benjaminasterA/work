#from callfunction import ChatOpenAI,ChatPromptTemplate,StrOutputParser =>3가지만 불러온다.
#from 모듈명
from callfunction import * #모듈내에 들어가 있는 모든요소(클래스,함수,,,)

# 다른 모듈
from langchain_core.prompts import MessagesPlaceholder #여러 메세지를 한꺼번에 삽입하는 역할
#추가
from langchain.memory import ConversationBufferWindowMemory #대화기록 전체

#1.모델 설정(안정적인 gtp-4o-mini)
llm = ChatOpenAI(model="gpt-4o-mini")# 

#메모리(최근의 대화 3개만 저장)
memory = ConversationBufferWindowMemory(k=2,return_messages=True)#이전대화를 메세지형태로 변환

# 프롬프트 설계(매개변수명은 변경불가)
prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 여행 전문가이야,사용자의 질문에 친절하게 답변해줘요."),
    MessagesPlaceholder(variable_name="history"),#chat_history라는 변수에 들어있는 다양한 메세지리스트들을 위치에 넣어줌
    ("human","{input}") #현재 사용자 입력자리 =>user 대신에 human
])
chain = prompt | llm  #strOutput~()


#연속 대화 시뮬레이션 (사용자 입력을 순차적으로 물어보게 코딩)
inputs=["부산 여행지 추천해줘","대한민국의 수도는 어디야?","서울의 인구는 몇명이?","내가 아까 추천해달라고 한 여행지는 어디야"]#2~3개 임의로(0~4) =>전에 내가 추천요청한 부산여행지 알아요?

for user_input in inputs: #처음에는 꺼내올값X ->두번째 질문부터 전에 저장된값을 계속 꺼내와라
    #메모리에 저장된값을 꺼내와라(매개변수값(딕셔너리객체))->입력받은값이 없다는 표시 ex) {"input":"안녕하세요"}
    #반환받을때 딕셔너리의 키중 하나가 "history"키값으로 저장된 값을 꺼내와라=>ex) 물품보관서(키값)
    history = memory.load_memory_variables({})["history"]
    #
    result = chain.invoke({"history":history,"input":user_input})#새롭게 입력을 받을때마다 전의 저장된 데이터 같이 전달
    #결과출력
    print(f"\n사용자:{user_input}\n 응답:{result.content}")
    #메모리에 저장(현재 입력값과 모델 응답값을 계속해서 요청할때마다 누적해서 저장)
    memory.save_context({"input":user_input},{"output":result.content})#출력문자열만 저장
    
    






