'''
[]->list , () ->tuple
{}->set
순서,중복된 데이터 저장 불가
형식) 변수={값1,값2,,,,}
'''
a={1,2,3,1}
print(a)#{1, 2, 3}
print(len(a))#3
#리스트+리스트2+,,,
b={3,4}
print(a.union(b))#{1, 2, 3, 4}
print(a.intersection(b))#교집합 {3}
print(a-b,a | b,a & b)
#a | b->union, a & b->interseciton
#{1, 2} {1, 2, 3, 4} {3}
#print(b[0])
#set->indexing 불가
#TypeError: 'set' object does not 
#support indexing
#b={3,4}

#{1, 2, 3, 4}
#{3}
#{1, 2} {1, 2, 3, 4} or조건 합침 {3} and조건 모두만족(3)

#형식) set객체명.update(데이터항목)
#{3, 4, 6, 7, 8, 9}
#{3, 4, 6, 7, 8, 9}
b.update({6,7})
print(b)#{3, 4, 6, 7}
b.update([8,9])#리스트형태로 값저장 가능
b.update((8,9))#튜플도 가능
print(b)

#{3, 4, 6, 7, 8, 9}
#{3, 4, 6, 7, 8, 9}

b.add(10) #set객체명.add(추가할 항목)

#set->데이터 삭제->discard(삭제할 항목)
b.discard(7)
b.remove(6)
print(b)#{3, 4, 8, 9, 10}
#변수명=[], 변수명=set()

c=set()#c는 자료형은 set타입
c=b;print(c)#{3, 4, 8, 9, 10}
c.clear();print(c);#전체 지워짐

#{3, 4, 8, 9, 10}
#set()

#리스트 내부에 중복된 데이터가 많으면
# list->set->list
li=[1,2,3,1]#->(1,2,3)->[1,2,3]
print(li)

#set으로 변경시켜주는 함수->set(대상객체명)
s=set(li)
print('set으로 변경(s)',s)
li=list(s)
print('list으로 최종변경(li)',li)

#set으로 변경(s) {1, 2, 3}
#list으로 최종변경(li) [1, 2, 3]