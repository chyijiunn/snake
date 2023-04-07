# 貪食蛇走迷宮
課程出發點為利用 OLED 點亮後，不進行刷新。記錄軌跡後存成 list 格式，若碰觸到自己軌跡則遊戲結束，並且計算走過軌跡點之數量，學習檔案存取。於課程第二階段加入迷宮繪製，將迷宮併入軌跡，以條件式判斷點是否位於 list 中。將來課程可發展成專案，改為兩個玩家同時進行，各自操控所屬進行對戰。

## 硬體組裝
1. 材料
	+ raspberry pico 
	+ OLED 0.96":I2C(VCC - GND - SCL - SDA)
	+ 按鈕*3
	+ 有源蜂鳴器
	+ M2 , M3 螺絲 = 8 , 4
1. 配置
	1. 根據接線圖銲接 OLED 與 pico
		+ 接線圖 ![pin](/media/RetroBoy.png)
	1. 放按鈕、蜂鳴器於下層壓克力板
	1. 放上pico板、銲接按鈕與蜂鳴器、鎖 M2 螺絲 4 個
	1. 鎖 OLED 與上層壓克力的 M2 螺絲 4 個
	1. 鎖上下層壓克力間 M3 螺絲 4 個

	1. 組裝圖 ![TinkerCAD](https://csg.tinkercad.com/things/jjDYlHlW5t2/t725.png?rev=1680768604343000000&s=&v=1)<https://www.tinkercad.com/things/jjDYlHlW5t2>
## 流程
1. pinTest 硬體測試
	+ OLED 管理套件 - 安裝 ssd1306(micropython-ssd1306)
	+ 按鈕
	+ 蜂鳴器
1. button_thread，雙執行緒：按鈕只兩個，利用一個 thread 讀取方向、主程式顯示方向
	1. 利用按鈕決定方向
		+ 先設定方向 = 0 (0,1,2,3 = 右,下,左,上)
		+ 如果按鈕 == 0 , 則 方向值加減 1
			+ 右按鈕 ,  方向 + 1
			+ 左按鈕 ,  方向 - 1
	2. 主程式
		+ 根據 %4 的結果判斷方向，如果餘數 == 0 ,1 , 2 , 3 ，則 螢幕呈現各方向
		+ 加上一個兩個按鈕同時按就停止的條件式
1. 改成會跑的點
	+ 方向 0 , x + 1
	+ 方向 1 , y + 1
	+ 另外兩個怎麼設計呢？
1. 保留軌跡
	+ OLED 不刷新，螢幕點不消失
	+ 跑到邊緣後要能跳到螢幕另一側
		+ x > 127 , x = 0
		+ x < 0 , x = 127
		+ y 要怎麼改呢？
	+ 把軌跡存成 list
1. 如果在軌跡內，則....
1. 失敗了。就爆炸吧。
	+ 定義函式
	+ 繪圖
		+ [圖檔範例](gg.gg/picocamp)		
		+ 讀取檔案
		+ 把每一個座標抓出後繪點陣圖
	+ break
1. 利用檔案生成迷宮
	1. google 試算表繪圖、複製座標資料
	2. 第一列資料包括預設方向、起始點座標、終點座標（好幾個）....
	3. 用 readlines 讀取剩餘資料，str 轉為 int , 存為 list 為 path 軌跡資料，用以產生碰撞時、跟自己的軌跡合併 
1. 計算分數
	1. 當座標所在 in path:
		1. 蜂鳴器叫
		2. 算分數
		3. 遊戲結束
	2. 當作標抵達終點：
		1. 好棒棒
1. 不只一個迷宮時，使用 for 迴圈直接按順序下去
	1. 設定迷宮初始檔名值
	2. 沒抵達終點時，使用 contiune，進行下一次迭代繼續重複
	3. (若抵達才開始進行)，這裡不縮行，進行蜂鳴、算分數、跑過關動畫、進入下一關 maze
