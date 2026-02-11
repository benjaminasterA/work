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

