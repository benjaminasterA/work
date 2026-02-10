from callfunction import *

# 시나리오 1
prompt = ChatPromptTemplate.from_messages([
    ("system", "그리고 쉬운 비유와 예시를 들어 설명하는 AI 선생님입니다. / "
               "사용자 질문에 다음 세가지 요소를 포함하여 답변 하시요. / "
               "1. 정의, 2. 이유(중요성), 3. 쉬운 예시."),
    ("user", "{question}")
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

parser = StrOutputParser()

chain = prompt | llm | parser
# RestAPI
if __name__ == "__main__":
    input_data = {"question":"REST API란?"}
    response = chain.invoke(input_data)

    print("-"*50)
    print(f"질문:{input_data['question']}")
    print("-"*50)
    print(response)
