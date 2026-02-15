# text를 가지고 검색 한다.
from sentence_transformers import SentenceTransformer

from PIL import Image
import faiss
import numpy as np
import os


os.chdir("C:/workAI/work/LangChain/4.Multi-Model-Rag")
print('os.getcwd()=>', os.getcwd())

model = SentenceTransformer("clip-Vit-B-32")

image=Image.open("./images/cat.jpg").convert("RGB")

vector = model.encode([image])

vector.astype("float32") # 검색이 수월하다고 해서 사용

dimension = vector.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(vector)

query_text = "a cute cat"
text_vector = model.encode([query_text])
text_vector = text_vector.astype("float32")

distances,indices = index.search(text_vector, k=1)


print("벡거리값:",distances)
print("검색된 인덱스",indices)
print("정상적으로 완료")


