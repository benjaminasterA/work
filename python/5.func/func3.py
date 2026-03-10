#func3.py작성
'''
함수의 전역변수,지역변수의 범위
'''
player = '전국대표'#함수밖에 선언(전역)

def FuncSoccer():
    name = '홍길동' #지역변수(함수안에 위치)
    #player = '지역대표'
    #함수내부에서 지역변수를 찾는다.->출력(우선출력)=>지역변수가 없으면  함수 밖의 전역변수를 찾아출력
    print(name,player)#홍길동 지역대표 =>홍길동 전국대표

print('player=>',player)#player=> 전국대표
FuncSoccer()