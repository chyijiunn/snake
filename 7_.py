#direction , start , goal
goal = [ ]
path = [ ]
def maze():
    global direction , start
    data = open('data/maze/maze_03','r')
    head = data.readline().split(',')  #第一行 head 資料 str -> list
    num = len(head)-1                  #計算list內資料量，
    b = head[:num]                     #後皆換行符號，捨棄
    
    direction = int(b[0])           #第 1 碼:方向
    start  =[int(b[1]),int(b[2])]   # 2~3 :start x ,y
    
    for i in range(int((num-3)/2)): # 去掉 b[0]~b[2]，剩下皆為 goal point，計算個數
        goal.append([b[2*i+3],b[2*i+4]])#加入空白 goal
    #以下處理迷宮座標資料，使用 readlines 讀取剩餘資料
    mazelist = data.readlines()
    for line in mazelist:
        a = line.split()
        for i in range(len(a)):
            xAxis = int(a[i].split(',')[0])
            yAxis = int(a[i].split(',')[1])
            #oled.pixel(xAxis,yAxis,1)
            path.append([xAxis,yAxis])
    data.close()

maze()
