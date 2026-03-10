#class5_is.py(상속)->save as =>class6_inheritence.py(다중 상속)
'''
 다중상속=>동시에 한개 이상의 부모클래스로부터 상속을 받는 경우(ex 외모,성격)
    ㄴ 만약에 두 부모의 동일한 기능을 가진 클래스가 존재한다면 어떻게 될까?
'''
class Person:  #부모(포괄적)
    name = ''
    age = 17
    
    def greeting(self):
        print('안녕하세요')

#부모 클래스 추가  =>다중상속->동시에 상속->같은 메서드가 중복=>자식에서는 어떻게 되는가?(복잡)
#                    ㄴ자바(다중상속 X)=>프로그램이 복잡해지기 때문
class University:
    def manage_credit(self):
        print('학점관리')
    #추가
    def greeting(self):
        print('반가워요')
        
#class 자식클래스명(부모1,부모2)
#상속받은 부모클래스의 첫번째와 두번째에서 중복된 메서드가 존재하면 첫번째 상속받은 부모것을 상속O
class Student(University,Person):  #University의 greeting()상속받음.
#class Student(Person,University):  
    def study(self):
        print('열심히 공부하기')
    
james = Student()
james.name = '제임스'
print(james.name,james.age)#제임스,17
james.greeting()# 안녕하세요 
james.study()#자기클래스의 메서드 호출(열심히 공부하기)
#추가2
james.manage_credit()#학점관리