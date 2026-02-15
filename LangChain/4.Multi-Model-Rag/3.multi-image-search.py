# text를 가지고 검색 한다.
from sentence_transformers import SentenceTransformer

from PIL import Image
import faiss
import numpy as np
import os


os.chdir("C:/workAI/work/LangChain/4.Multi-Model-Rag")
print('os.getcwd()=>', os.getcwd())

model = SentenceTransformer("clip-Vit-B-32")

# 4 이미지 멀티 처리 ##################################
image_paths = [
    "./images/cat.jpg",
    "./images/dog.png",
    "./images/car.png"
]

images = []

for path in image_paths:
    img=Image.open(path).convert("RGB")
    images.append(img)
# image 전용 vector
image_vector = model.encode(images) #{} 사용 안함<-자체가 리스트이기에

image_vector.astype("float32") # 검색이 수월하다고 해서 사용

################################

dimension = image_vector.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(image_vector)

query = "a running dog"
# 객체명->연다라 함수 메서드가 나오는 방법 -> 체인메소드
query_vector = model.encode([query]).astype("float32")

distances,indices = index.search(query_vector, k=1)

print("가장 유사한 이미지:",image_paths[indices[0][0]])
print("거리값",indices[0][0])
print("정상적으로 임무 완수")
