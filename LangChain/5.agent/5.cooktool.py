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
    """ 식재료의 현재 시장 가격을 조회합니다. 식재료 이름이 입력되어야 합니다."""
    #함수의 기능
    return f" {item_name} 의 가격은 오늘 시세로 5,000원 입니다."

#2.요리조리법
@tool
def get_recipe(food_name : str):
    """ 특정 음식의 조리법(레시피)를 검색합니다. 음식이름이 입력되어야 합니다."""  # 전체적인 기능을 언급 뒤에 매개변수로써 어떠한것인지?
    return f" {food_name} 레시피:먼저 재료를 손질하고 냄비에 넣으세요..."

#3.칼갈기 도구(직원)
@tool
def sharpen_knife(knife_type: str):
    """ 잘 들지 않은 칼을 날카롭게 가는 역할을 하는 직원입니다. 칼의종류(식칼,과도등)를 알려주시면 더 좋습니다."""
    return f"{knife_type}을 아주 날카롭게 갈아줍니다.이제 요리 준비가 끝났습니다."

#2단계 요리사(LLM) 준비
llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)#정확성이 명확(0~0.3 실무)

#binding(요리사(LLM)알려줌(직원 3명있다는것을 알려주는 역할))
#추가
tools_list = [check_ingredient_price,get_recipe,sharpen_knife]
chef_with_tools = llm.bind_tools(tools_list) # 연결시켜주는 구문 (수동호출(X))

#웹에 출력
st.title("요리사의 판단 연습(새로운 칼 갈기 테스트)")
st.write("요리사에게 '칼이 너무 무뎌졌어'라고 말해보거나 '고기 가격 알려줘' 라고 해보세요")
order = st.text_input("요리사에게 할 말을 입력하세:")

if order:
    #요리사가 판단(고민 (invoke))
    response = chef_with_tools.invoke(order)
    #어떤 도구를 호출(=어떤 직원을 호출)
    if response.tool_calls:
        chosen_tool = response.tool_calls[0]['name'] #내부적으로 자동호출된 직원의 이
        st.success(f"요리사의 판단: 지금 필요로 한건 '{chosen_tool}' 직원을 호출하면 되겠군요")
        st.json(response.tool_calls) #AI가 내부적으로 만든 '실행계획서'를 보여준다.(json파일로 출력이 되는지도 확인)
    else:
        st.info("요리사의 판단: 이건 그냥 대화로 충분해. 직원을 부를 필요는 없구나!")
        st.write(response.content)

# 요리도구를 하나 추가(칼 갈기 도구,,,,)