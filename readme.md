# 貪食蛇走迷宮
## 硬體組裝
1. 材料
	+ raspberry pico 
	+ 按鈕*3
	+ 有源蜂鳴器
	+ OLED 0.96":I2C(VCC - GND - SCL - SDA)
	+ M2 , M3 螺絲 = 6 , 4
1. 組裝 <iframe width="725" height="453" src="https://www.tinkercad.com/embed/jjDYlHlW5t2?editbtn=1" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>
## 課程流程
1. 嘗試作一個類似貪食蛇的遊戲
2. 按鈕只有兩顆時，利用一個 thread 讀取方向、主 main 進行移動
	1. 利用按鈕增加數值資料
	2. 根據 %4 的結果判斷方向
3. OLED 若沒刷新，螢幕的點不消失，把軌跡存成 list，如果新的點在 list 中，則停止遊戲
4. 讓起始點隨機開始
5. 呈現分數後要能自動重來
	1. 軟體方式
	2. 硬體按鈕接線 run pin
6. 利用檔案生成迷宮
	1. google 試算表繪圖、複製座標資料
	2. 第一列資料包括預設方向、起始點座標、終點座標（好幾個）....
	3. 用 readlines 讀取剩餘資料，str 轉為 int , 存為 list 為 path 軌跡資料，用以產生碰撞時、跟自己的軌跡合併 
7. 計算分數
	1. 當座標所在 in path:
		1. 蜂鳴器叫
		2. 算分數
		3. 遊戲結束
	2. 當作標抵達終點：
		1. 好棒棒
8. 不只一個迷宮時，使用 for 迴圈直接按順序下去
	1. 設定迷宮初始檔名值
	2. 沒抵達終點時，使用 contiune，進行下一次迭代繼續重複
	3. (若抵達才開始進行)，這裡不縮行，進行蜂鳴、算分數、跑過關動畫、進入下一關 maze
