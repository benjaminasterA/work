# txt, pdf file 불러 오기
from langchain_community.document_loaders import PyPDFLoader

import os
print(f"현재 디렉토리 {os.getcwd()} ")

current_dir = os.path.dirname(os.path.abspath(__file__))

loader = PyPDFLoader("./data/Samsung_Card_Manual_Korean_1.3.pdf")

pages=loader.load()      

print('자료형=>',type(pages))
print(f"총 페이지수 : {len(pages)} 쪽")
print(f"1페이지 미리보기: {pages[0].page_content[:500]}")