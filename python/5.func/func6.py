#클로저 함수=>중첩함수(함수내부에 또 다른 함수)
'''
함수 내부의 변수값을 계속해서 참조(=외부에서 불러다 사용)하고 싶을때 사용
=>한번 불러와서 끝이 아니라 계속해서 누적해서 값을 불러오고 싶을때 사용

1.중첩함수를 작성
2.안쪽함수=>계산식을 사용
3.안쪽함수의 결과값을 밖에서 참조할 수 있도록 해주기 위해서는 밖의함수의 결과값(=안쪽함수의 이름)
'''

def out():
    count = 0 #지역변수
    def inn():
    #안쪽의 함수에서는 밖의 함수의 지역변수값을 가져올 수 가 없다.
    #가져오기 위해서는 nonlocal 부모의 변수을 선언해야 가져올 수 가 있다.
        nonlocal count
        count+=1 #count = count+1
        return count
    print(inn())
#UnboundLocalError: local variable 'count' referenced before assignment
out()  #1
out()  #1 =>호출해도 안쪽에서 count=0으로 새로 초기화
print('========클로저를 사용해 보자===')
def outer():
    count = 0 #지역변수
    def inner():
    #안쪽의 함수에서는 밖의 함수의 지역변수값을 가져올 수 가 없다.
    #가져오기 위해서는 nonlocal 부모의 변수을 선언해야 가져올 수 가 있다.
        nonlocal count
        count+=1 #count = count+1
        return count
    #print(inner()) =>내부함수를 반환=>클로저
    return inner #왜 내부함수이름을 알려줄까요? 안쪽함수의 주소값을 알려줄까요?
    #count가 저장된 위치를  알고 있는 함수->내부함수명

add1 = outer()#주소를 전달->inner
print('add1()=>',add1())#add1() =>inner()호출하는것과 동일한 효과 1
print('add1()=>',add1())#2
print('add1()=>',add1())#3
print('add1()=>',add1())#4
#새로운 변수에 값(주소)를 받게 되면 완전히 초기화
add2 = outer()
print('add2()=>',add2())#5X ->1부터 시작 add2()=> 1

print('수량*단가 세금 결과 출력')
def outer2(tax):
    def inner2(su,dan):
        price = su * dan * tax
        return price
    return inner2 #결과값을 내부 함수로 리턴시켜서 외부에서 누적된 계산값을 가능하게해주는 함수=>클로저
r = outer2(0.1)#세율 0.1 =>r=>inner2(주소 공유)
re = r(3,25000)#r->inner2
print('re=>',re)#re=> 7500.0
#closure => 함수형 언어에만 있음=>파이썬,자바스크립트
# 람다함수,재귀함수 =>func7.py