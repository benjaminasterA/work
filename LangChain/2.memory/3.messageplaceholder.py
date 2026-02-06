#from callfunction import ChatOpenAI,ChatPromptTemplate,StrOutputParser =>3가지만 불러온다.
#from 모듈명
from callfunction import * #모듈내에 들어가 있는 모든요소(클래스,함수,,,)

# 다른 모듈
from langchain_core.prompts import MessagesPlaceholder #여러 메세지를 한꺼번에 삽입하는 역할
from langchain_core.messages import HumanMessage,AIMessage

#1.모델 설정(안정적인 gtp-4o-mini)
model = ChatOpenAI(model="gpt-4o-mini")# 

# 프롬프트 설계
prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 사용자의 이전 대화를 기억하는 전문 비서입니다."),
    MessagesPlaceholder(variable_name="chat_history"),#chat_history라는 변수에 들어있는 다양한 메세지리스트들을 위치에 넣어줌
    ("user","{input}") #현재 사용자 입력자리
])
chain = prompt | model | StrOutputParser() 

#대화 기록 저장 리스트->exit문자열을 만나기 전까지 계속해서 저장
chat_history = [] #HumanMessage,AIMessage

print("대화를 시작합니다. 종료할려면 exit를 입력요망")
while True:  #들여쓰기=>제어문과 함수, 클래스 작성할때 자동으로 들여쓰기가 필요
    user_input = input("사용자: ") #input함수 이용
    
    if user_input.lower() == "exit":  # "exit" 객체명.호출할 메서드명() =>파이썬에서는 모든것이 거의 객체입니다.(문자열도 객체다)
        break #탈출문
    response = chain.invoke({
        "input":user_input, #현재 질문
        "chat_history":chat_history #이전 대화 전체 전달
    })
    print("AI:",response) 
    
    #대화기록 누적=>사용자가 물어보는 질문과 AI 대답하는 문자열을 구분해서 저장=>꺼내올때도 구분해서 받아올 수 있다.
    Hu = HumanMessage(content=user_input)
    chat_history.append(Hu)
    
    Ai = AIMessage(content=response)
    chat_history.append(Ai)
    
    #chat_history.append(HumanMessage(content=user_input)) #축약형(익명객체형태로 값을 저장시킨 방법) it is->it's
    #chat_history.append(AIMessage(content=response))
    '''
    대화를 시작합니다. 종료할려면 exit를 입력요망
사용자: 내이름은 테스트김이야
AI: 안녕 테스트김! 어떤 도움이 필요하신가요?
사용자: 다음주 주말에 갈 좋은 여행지를 추천해줘
AI: 다음주 주말 여행으로 추천할 만한 몇 가지 장소를 소개할게요.

1. **강릉** - 아름다운 바다와 커피 거리로 유명한 강릉은 해변에서의 휴식과 맛있는 커피를 즐기기에 좋습니다. 경포대와 주문진 해수욕 장도 꼭 방문해 보세요.

2. **제주도** - 자연경관이 아름답고 다양한 액티비티를 즐길 수 있는 제주도는 주말 여행에 최적입니다. 한라산 등반, 성산 일출봉, 그리고 올레길 트래킹을 추천합니다.

3. **여수** - 아름다운 해안선과 맛있는 해산물로 유명한 여수는 낭만적인 여행지입니다. 오동도와 여수 밤바다를 만끽해 보세요.        

4. **가평** - 자연을 만끽하며 힐링할 수 있는 가평은 남이섬과 쁘띠프랑스 등이 있어 가족 단위 여행으로 좋습니다.

5. **부산** - 해운대와 광안리 해수욕장을 비롯해 맛있는 음식과 다양한 볼거리가 많은 부산은 주말 여행에 안성맞춤입니다.

어떤 곳이 마음에 드시나요? 추가적인 정보가 필요하시면 말씀해 주세요!
사용자: 그런제 전에 얘기했던 내이름은 알고있어요?
AI: 죄송하지만, 사용자의 이름이나 개인 정보를 기억하고 있지는 않습니다. 이전 대화 내용을 기억하지 못하기 때문에 이름이나 다른 정보를 알 수 없습니다. 하지만 다른 질문이나 요청이 있으시면 도와드릴 수 있습니다!
사용자: exit

(.venv) C:\workAI\work>C:/workAI/work/.venv/Scripts/python.exe c:/workAI/work/LangChain/2.memory/3.messageplaceholder.py
대화를 시작합니다. 종료할려면 exit를 입력요망
사용자: 내이름은 테스트김이야
AI: 안녕하세요, 테스트김님! 어떻게 도와드릴까요?
사용자: 이번주에 갈만한 여행지 추천해줘
AI: 어디로 여행을 가고 싶은지에 따라 다르겠지만, 몇 가지 추천해드릴게요. 

1. **제주도**: 아름다운 자연경관과 맛있는 음식, 다양한 액티비티가 있어 주말 여행으로 적합합니다. 한라산 등반이나 해변에서의 힐링을 즐길 수 있습니다.

2. **부산**: 해운대와 광안리 해수욕장이 유명하고, 신선한 해산물을 맛볼 수 있는 좋은 장소입니다. 태종대나 감천문화마을도 추천합니다.

3. **경주**: 역사적인 유적과 볼거리가 많은 도시로, 불국사와 석굴암, 천마총 등 다양한 문화재를 탐방할 수 있습니다.

4. **강릉**: 바다와 산이 어우러져 있어 힐링 여행에 좋습니다. 커피와 음식도 유명하고, 경포대에서 일몰을 보며 여유를 즐길 수 있습니 다.

어떤 여행지를 더 선호하시나요?
사용자: 그런데 내이름은 알고있어?
AI: 네, 테스트김님! 이전에 말씀해주신 이름을 기억하고 있습니다. 다른 질문이나 요청이 있으시면 언제든지 말씀해 주세요!
사용자: exit

(.venv) C:\workAI\work>C:/workAI/work/.venv/Scripts/python.exe c:/workAI/work/LangChain/2.memory/3.messageplaceholder.py
대화를 시작합니다. 종료할려면 exit를 입력요망
사용자: 내이름은 테스트김입니다.
AI: 안녕하세요, 테스트김님! 무엇을 도와드릴까요?
사용자: 이번주 주말에 놀러가기 좋은 장소 좀 추천부탁해요
AI: 물론입니다! 주말에 놀러가기 좋은 장소는 여러 가지가 있습니다. 어떤 종류의 활동을 선호하시는지에 따라 추천을 다르게 할 수 있는 데요. 예를 들어:

1. **자연과 함께하는 곳**: 근처 산이나 공원에서 하이킹이나 피크닉을 즐기실 수 있어요. 예를 들어, 국립공원이나 유명한 트레일 등.   

2. **문화 체험**: 박물관이나 미술관, 전시회 등을 방문해 보는 것도 좋습니다. 지역에서 열리는 특별 전시나 공연이 있을 수도 있으니 확인해 보세요.

3. **도시 탐방**: 맛집 탐방이나 쇼핑을 위해 인근 도시를 방문해보는 것도 재밌겠죠. 유명한 거리나 시장을 둘러보는 것도 추천합니다.  

4. **해변이나 호수**: 날씨가 좋다면 해변이나 호수에서 수영, 자전거 타기, 바베큐를 즐길 수 있습니다.

특정 지역에 대한 정보가 필요하시면 알려주세요. 보다 구체적인 추천을 드릴 수 있습니다!
사용자: 내 이름은 혹시 알아요?
AI: 네, 테스트김님이라고 하셨죠! 혹시 다른 이름을 사용하시거나 부르고 싶은 이름이 있으시면 말씀해 주세요.
사용자: exit
    '''

    
    
    











