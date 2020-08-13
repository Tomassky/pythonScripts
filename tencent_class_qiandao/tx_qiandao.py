import win32gui
import win32con
import win32api
import time

# 获取句柄
hwnd = win32gui.FindWindow(None,u"腾讯课堂")
count = 0
while(1):
	# 显示隐藏窗口
	win32gui.ShowWindow(hwnd,win32con.SW_RESTORE)
	time.sleep(0.5)
	# 移动窗口并重绘
	win32gui.MoveWindow(hwnd,262,112,1248,780,True)
	# 焦点关注
	win32gui.SetForegroundWindow(hwnd)
	#获取当前鼠标焦点
	POS = win32gui. GetCursorPos()
	POS = list(POS)
    # 鼠标聚焦
	win32api.SetCursorPos((1103, 784))
	# 鼠标左键按下
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,1103,784)
	# 鼠标左键拾起
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,1103,784)
	# 计算点击次数
	count += 1
	print("执行次数----",count)
	# 隐藏窗口
	win32gui.ShowWindow(hwnd,win32con.SW_HIDE)
	# 还原鼠标位置
	win32api.SetCursorPos((POS[0], POS[1]))
	time.sleep(5)









