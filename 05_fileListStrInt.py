data = open('data/pics/boom','r')
for line in data:
    a = line.split()
    print(a)
    print(type(a))
    print('這行有幾個元素：',len(a))
    print('第一個是',a[0])
    print(a[0].split(','))
    print(a[0].split(',')[0])
    print(a[0].split(',')[1])
    print(type(a[0].split(',')[1]))
    
data.close()