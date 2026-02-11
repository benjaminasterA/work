'''
4.cookplan.py(요리사=>요리를 어떻게 결정해서 요리?)
'''
#1.요리사가 사용할 수 있는 도구들의 사용설명서

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

#1.요리재료 가격?
@tool
def check_ingredient_price(item_name : str):
    """ 재료의 시장 가격을 조회합니다. 식재료 이름이 필요합니다."""
    #함수의 기능
    return " 이 도구는 가격 조회용입니다."

#2.요리조리법
@tool
def get_recipe(food_name : str):
    """ 음식의 조리법(레시피)를 알려줍니다. 음식이름이 필요합니다."""  # 전체적인 기능을 언급 뒤에 매개변수로써 어떠한것인지?
    return "이 도구는 레시피 검색용입니다."

#2단계 요리사(LLM) 준비
llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)#정확성이 명확

#binding
chef_with_tools = llm.bind_tools([check_ingredient_price,get_recipe])
#웹에 출력
st.title("요리사의 판단 연습")

order = st.text_input("요리사에게 질문해보세요(예:고등어 가격 얼마에요? 혹은 김치찌개 어떻게 만드나요?)")

if order:
    #요리사가 판단
    response = chef_with_tools.invoke(order)
    #어떤 도구를 호출(=어떤 직원을 호출)
    if response.tool_calls:
        st.success(f"요리사의 판단: '{response.tool_calls[0]['name']}' 직원을 호출하면 되겠군요")
        st.json(response.tool_calls) #AI가 내부적으로 만든 '실행계획서'를 보여준다.
    else:
        st.info("요리사의 판단: 이건 그냥 대화로 충분해. 직원을 부를 필요는 없구나!")
        st.write(response.content)

# 요리도구를 하나 추가(칼 갈기 도구,,,,)