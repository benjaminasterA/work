#class5_is.py(상속)->save as =>class6_inheritence.py(다중 상속)
'''
상속의 장점=>1.부모의 멤버변수,메서드를 상속 받음=>새로 작성할 필요X(소스코드 절약)->개발시간 단축
              ->복붙=>라인수가 증가 (A 1000라인 코딩) => B(700라인(중복코딩))+300라인
              ->복붙->1000라인 그대로 상속->300라인만 코딩
           2.재사용성 때문에 필요(모듈 작성->불러오기)
    ㄴ오버라이딩 기법(자식입장에서 부모의 메서드의 내용만 수정해서 호출하는 기법)
'''
class Person:  #부모(포괄적)
    name = ''
    age = 17
    
    def greeting(self):
        print('안녕하세요')

# is a 관계->상속   p(자식)->q(부모) (O)  q->p(X)  class Employee(부모)   class Manager(자식)
#                                                  직원                      팀장
#  팀장은 그 회사의 직원이다.(O)  그 직원은 그회사의 팀장이다.(X)
#  학생은 그 사람이다.   그 사람은 학생이다.(X)
# class 자식클래스명(부모클래스명)
class Student(Person):  #class Student extends Person (java)
    def study(self):
        print('열심히 공부하기')
    #추가
    def greeting(self):
        print('반갑습니다.제임스라고 합니다.')#내용만 변경하는 기법(overriding)

james = Student()
james.name = '제임스'
print(james.name,james.age)#제임스,17
james.greeting()# 안녕하세요 =>부모로부터 물려받은 메서드를 호출->반갑습니다.제임스라고 합니다.
james.study()#자기클래스의 메서드 호출(열심히 공부하기)