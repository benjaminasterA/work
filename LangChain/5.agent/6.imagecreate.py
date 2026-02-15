import streamlit as st
#그림을 그려서 보여달라(도화지(Image),붓(ImageDraw),글씨체(ImageFont))
from PIL import Image, ImageDraw, ImageFont
import os

#@tool #<-agent에서 말하는 자동 호출
def draw_card(text):
    """주문 받은 메뉴 이름을 넣어서 예쁜 요리 카드를 만듭니다."""
    #1. 도화지(가로 500, 세로 300) 크기는 RGB
    img = Image.new('RGB',(500,300),color=(255,255,240))
    #2. Drew 객체 생성
    draw = ImageDraw.Draw(img) #도화지에 붓을 쥐고 그림
    #3. 폰트 글꼴선택 : 한글이 깨지지 않게
    font_path = "./font/NotoSansCJKkr-Regular.otf"
    #파일 불러올때 예외처리(1.파일불러오기2.DB연동3.네트웨크프로그래밍)
    try:
        font = ImageFont.truetype(font_path,25) #폰트경로 크기설정
        
    except:
        #폰트없으면 알려주고 기본폰트 사용.
        st.error("폰트화일을 찾을수 없습니다. 경로를 확인해주세요.")
        font = ImageFont.load_default()

    draw.text((50,130),f"오늘의 추천: {text}", font=font,fill=(255,0,0))
    draw.rectangle([10,10,490,290],outline=(100,100,100),width=3)
    file_name = "daily_card.png"
    img.save(file_name)
    return file_name

st.title("요리사의 실제 카드 그리기")
st.write("요리사가 직접 손을 움직여서 화일을 생성하는 단계입니다.")
menu_name = st.text_input("추천할 메뉴 이름을 입력하세요:")

if st.button("요리 카드 제작 시작"):
    #어떤 메뉴 이름이 존재 한다면)
    if menu_name:
        #요리카드 이름을 만들어 줘.
        path = draw_card(menu_name) #수동 함수
        st.image(path,caption="요리사가 방금 그린 따끈따끈한 카드")
        if os.path.exists(path):
            st.success(f"성공! '{path}' 파일이 서버 폴더에 생성 되었습니다.")
    else:
        st.warning("메뉴 이름을 먼저 입력 해주세요!")
        
