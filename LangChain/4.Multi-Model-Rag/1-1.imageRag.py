from sentence_transformers import SentenceTransformer

from PIL import Image
import faiss
import numpy as np
import os


os.chdir("C:/workAI/work/LangChain/4.Multi-Model-Rag")

model = SentenceTransformer("clip-Vit-B-32")

image=Image.open("./images/cat.jpg").convert("RGB")

vector = model.encode([image])

vector.astype("float32")

dimension = vector.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(vector)

print("벡터 차원:",vector.shape)
print("현재 인덱스에 저장 된 벡터 갯수",index.ntotal)
print("정상적으로 완료")


