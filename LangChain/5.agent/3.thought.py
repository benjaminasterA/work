'''
1.cal.py
=>함수(=기능)을 호출=>개발자가 임의로(=필요로할때 마다) 호출(수동 호출)
=>함수 호출=>AI가 스스로 판단해서 스스로 호출한다.(자동 호출 =>연결시켜주는 (binding)) =>tools(=도구들)
'''

from langchain_core.tools import tool

#사용자로부터 값을 입력(매개변수)->계산=>부탁(결과값(=반환값(=return)))

@tool  # @tool ->데코레이트 1.@tool 붙어있다. =>함수의 역할문자열을 AI에게 전달하는 역할을 한다.=>LLM과 호출(자동)
def multiply(a : int,b : int):  # 자료형 변수=>py 변수: 자료형,,, =>자동으로 AI가 호출할 수 있도록 만들겠다.@tool
    """ 두 정수를 곱하는 도구 입니다. """
    #처리해야할 업무
    return a * b #실제 곱셈

#반환값 = 함수명(매개변수1,매개변수2) =>print(반환값)
#su = multiply(3,4) #수동 호출 
#print('su=>',su)
print(f"도구 이름:{multiply.name}") # 도구이름을 출력(도구=함수이름)
print(f"도구 설명:{multiply.description}")

#함수 작성--->연결(binding)->자동호출
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)
#LLM에게 우리가 만든 에이전트(=도구)가 있다는것을 알려준다. 형식) ~.bind_tools([호출할함수명,,,,,])
llm_with_tools = llm.bind_tools([multiply]) # LLM이 누가 호출할 대상자인지를  알려준다.

#테스트 호출
res = llm_with_tools.invoke("5 곱하기 3은 ?")
print(res.tool_calls)#LLM이 multiply 도구(=에이전트)를 쓰겠다고 결정한것을 볼 수가 있다.=>LLM이 누구를 호출할때 결정(내부적)
# [{'name': 'multiply', 'args': {'a': 5, 'b': 3}, 'id': 'call_bjFuYpJKwbT2jk2qTA3NG2HH', 'type': 'tool_call'}]

#3.thought Loop

from langchain.agents import AgentExecutor,create_openai_functions_agent #호출
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

#에이전트가 생각할 수 있는 가이드 라인 설정
prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 계산을 도와주는 유능한 AI 조수입니다."),
    ("human","{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"), # AI의 '생각의 흔적을 담는 공간'
])
#3.에이전트 조립(아직 실행 X =>내부적으로 결정(확인))
agent = create_openai_functions_agent(llm,[multiply],prompt) #1.LLM객체  2.tools[호출할 함수명], 3.prompt(user가 전달할값)

#4.실행(에이전트 실행기(Executor))=>Loop 핵심(1.에이전트 정보 ,2 tools=[처리할 함수명],3.verbose=Ture) #처리과정(내부)(디버깅)
agent_executor = AgentExecutor(agent=agent,tools=[multiply],verbose=True)
agent_executor.invoke({"input": "123 곱하기 456을 계산좀 부탁드립니다."}) # print(multiply(123,456)) 수동호출

#bind_tools([호출할함수명,,,,]) =>나중에 필요에 따라서 호출할 함수목록을 알려주는역할
#create_openai_functions_agent(llm,[multiply],prompt)=>누가(llm),prompt(어떤방식으로 ) 직접대상자호출(에이전트)
