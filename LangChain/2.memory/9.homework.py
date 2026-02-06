
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate #대화
from langchain_core.output_parsers import StrOutputParser #문자형태로 출력

#apikey
import dotenv #환경변수 =>블럭지정한 후 ctrl+/
dotenv.load_dotenv()#모듈명.호출할 함수명(=직원) =>인증키

#1.모델 설정(안정적인 gtp-4o-mini)
model = ChatOpenAI(model="gpt-4o-mini",temperature=0.7)# 

chat_history="사용자:내이름은 '테스트김'야.\n AI: 반가워요 테스트님!" #미리 언급한 문장을 저장

prompt = ChatPromptTemplate.from_template(
    "system": {}
    "user": {}
    "AI"
    "이전 대화:{history} \n 질문: {input}")
chain = prompt | model | StrOutputParser() 

#과거 내역을 함꺼번에 보냄->이름을 물어보기 전에 누구인지 미리 전의 데이터값을 전달
result = chain.invoke({"history":chat_history,"input": "내이름이 뭔지알아요?"})
print(f"수동 메모리 응답:{result}")









