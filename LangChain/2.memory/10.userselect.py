from callfunction import *

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


prompt_map = {
    "1": ("요약", "다음 내용을 요약 해 주세요.\n 내용:{text}"),
    "2": ("키워드", "다음 내용에서 핵심 키워드 5개만 뽑아주세요.\n 내용:{text}"),
    "3": ("답변", "다음 질문에 3문장이내로 답변 해주세요.\n 내용:{text}")
}

print("1) 요약")
print("2) 키워드")
print("3) 3문장이내로 답변")

sel = input("선택(1~3): ").strip()
if sel not in prompt_map:
    raise SystemExit("잘못된 선택")

name,template = prompt_map[sel]
prompt = PromptTemplate.from_template(template)
print('name,template->', name,template)

chain = prompt | llm | StrOutputParser() 

text = input(f"[{name}] 입력 :").strip()
print(chain.invoke({"text": text}))
