#7.cooksession.py

import streamlit as st #as 별칭명
#그림을 그려서 보여달라(도화지(Image),붓(ImageDraw),글씨체(ImageFont))
from PIL import Image,ImageDraw,ImageFont #화가 도구
import os #파일 경로

#1.냉장고(=보관함)가 비어있다면 칸을 마련합니다.=>세션_id값을 미리 정해놓음
#페이지가 처음 열릴때 딱 한번만 실행되는 설정 =>st.session_state vs class 에서의 데이터 저장
if "my_fridge" not in st.session_state: #my_fridge이름으로 저장할 공간이 없다면
    #이미지 데이터,메뉴이름을 담을 빈칸을 만든다.
    st.session_state.my_fridge = {"img_data":None,"menu_name":"없음"}

#웹에 출력
st.title("요리사의 신선 보관함 실습")#H1~H2
st.write("버튼을 눌러도 데이터가 사라지지 않는 금고의 원리!")

#2.기능을 확인 하면서 요리를 만드는 작업
menu_input = st.text_input("냉장고에 넣을 메뉴 이름을 입력하세요")

if st.button("요리 완성 및 냉장고 보관"): #버튼을 눌렀다면
    #어떤 메뉴이름이 존재한다면
    if menu_input:
        
        img = Image.new('RGB',(400,200),color=(255,255,200))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("./font/NotoSansCJKkr-Regular.otf")
        except:
            font = ImageFont.load_default()
        
        draw.text((50,80),f"신선 보관:{menu_input}",font=font,fill=(0,0,0))
        img.save("temp_dish.png")#일단 파일로 저장
        
        ####################생성된 파일을 읽어서 냉장고(Session State)'에 저장##########
        with open("temp_dish.png","rb") as f: #with open(1.불러올함수명,2.파일의 모드) as 파일변수
            #파일을 냉장고에 저장(키명(대문자,소문자구분))
            st.session_state.my_fridge["img_data"] = f.read() #img_data키값에 이미지 저장완료
            st.session_state.my_fridge["menu_name"] = menu_input
        
        st.success(f"'{menu_input}'요리를 냉장고에 잘 넣어서 보관완료!!!")
    else:
        st.warning("메뉴 이름을 먼저 입력해주세요")    
        
        
#냉장고에서 꺼내서 손님에게 다시 보여주기
#이 부분은 페이지가 새로고침되어도 'my_fridge' 안에 데이터가 존재하는 한 항상 실행돼
if st.session_state.my_fridge["img_data"] is not None:
    st.divider() #경계선
    st.subheader(f"냉장고에서 꺼낸 요리: {st.session_state.my_fridge['menu_name']}")
    
    #냉장고(=세션)에 보관된 바이트 데이터를 이미지로 그대로 보여줘야 된다.(=직렬화(IT) 네트워크 전송)
    st.image(st.session_state.my_fridge["img_data"])
    
    #다운로드 버튼도 냉장고에 있는 데이터를 그대로 사용하므로 링크가 사라지지 않음.
    st.download_button(
        label="요리 카드 사진 저장", #1.버튼의 타이틀 제목
        data = st.session_state.my_fridge["img_data"],#2.연관된 데이터 표시
        file_name = "chef_recipe_card.png", #3.다운로드와 연관된 파일명
        mime="img/png" #4.다운로드와 연관된 파일의 종류(img/확장자 종류)
    )
    #새로고침의 문제점=>Streamlit은 코드 한줄만 바꿔도 위에서 다시 실행
        ###########################################################################
        
       