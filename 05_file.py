data = open('data/pics/boom','r')
for line in data:
    a = line.split()
    print(a)
    '''
    for i in range(len(a)):
        xAxis = int(a[i].split(',')[0])
        yAxis = int(a[i].split(',')[1])
        print(xAxis,yAxis)
        '''
data.close()