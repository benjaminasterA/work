#func7.py=>람다함수,재귀함수
#익명함수->함수의 이름이 없는 축약형태의 함수
print('축약함수(Lambda)')
#     function 함수명 (값1,값2,,,)
#형식 lambda 인자:표현식(구문)(값1,값2,,,)
def Hap(x,y=10):
    return x+y

print(Hap(3,4))
print('람다로 표현하면')
print((lambda x,y:x+y)(3,4))#7 =>간단한 한문장 정도의 함수내용
print('\n람다도 가변인수 부여 가능')
#람다함수=>이름이 있는 함수로 변경이 가능? ok
kbs = lambda a,su=10:a+su
print(kbs(5))#5+10
print(kbs(5,6))#11

sbs = lambda a,*tu,**di:print(a,tu,di)#매개변수 O 반환값X
sbs(1,2,3,m=4,n=5)#매개변수명(key)=전달할값(value),,, {'매개변수명':'값'}(X)
#1 (2, 3) {'m': 4, 'n': 5}
print('\n다른함수에서 람다사용하기')
#filter(함수,시컨스자료형(=순서가 있는 자료형))
print(list(filter(lambda a:a<5,range(10))))#0~9 [0,1,2,3,4]
print(list(filter(lambda a:a%2,range(10))))#False [1, 3, 5, 7, 9]
#재귀함수 =>함수호출(caller->worker)
print('\n재귀함수(팩토리얼계산)')#5!=>5*4*3*2*1->0(X)
def fsum(n):
    if n==1: return 1
    return n+fsum(n-1)#5+4+3+2+1
print(fsum(10))#10+fsum(9)(9+fsum(8))=>10+9+8+7+...+1=55

def countDown(n):
    if n==0:  #맨처음에 빠져나갈 조건을 반드시 부여
        print('완료')
    else:
        print(n,end=' ')#5 4 3 2 1
        countDown(n-1) #5 4 3 2 1 완료

countDown(5)