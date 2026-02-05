from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

#api 키 로드
import dotenv
dotenv.load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7 #0~10 사이의 값, 0에 가까울수록 결정론적 출력
)

# 2. 프롬프트(Prompt) 정의
prompt = ChatPromptTemplate.from_messages([
    ("system", "다음 뉴스 내용을 바탕으로 사람들의 클릭을 유도할 수 있는 '낚시성' 헤드라인 제목을 3개를 작성해줘."),

])
# 사용자 입력을 받을 템플릿을 생성하고 변수 'prompt'에 할당함

# 3. 체인(Chain) 생성 및 실행
chain = prompt | model 
news_contans=" 애플이 새로운 AI 기능을 탑재한 아이폰 18을 출시한다고 발표했습니다."


response = chain.invoke({"contans": news_contans})
print(response.content)
print("=====================================")
print(response)
 