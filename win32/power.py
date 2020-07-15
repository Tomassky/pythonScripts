import time
import win32api
import win32gui
import win32con
import pickle
import smtplib
import sys
from email.mime.text import MIMEText
from email.utils import formataddr

def open_software_qq():
	pickle_file = open('password.pkl','rb')
	dict = pickle.load(pickle_file)
	# QQ软件启动
	win32api.ShellExecute(0, 'open', r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\腾讯软件\QQ\腾讯QQ.lnk', '','',1)
	time.sleep(15)
	# 鼠标聚焦
	win32api.SetCursorPos((880,586))
	# 鼠标左键按下
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,880,586)
	# 鼠标左键拾起
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,880,586)
	# 模拟键盘输入密码
	for i in range(1,16):
		win32api.keybd_event(dict[i],0,0,0)
		win32api.keybd_event(dict[i],0,win32con.KEYEVENTF_KEYUP,0)
	win32api.keybd_event(0xA0,0,0,0)         
	win32api.keybd_event(0x32,0,0,0)  
	win32api.keybd_event(0x32,0,win32con.KEYEVENTF_KEYUP,0)
	win32api.keybd_event(0xA0,0,win32con.KEYEVENTF_KEYUP,0)
	time.sleep(0.5)
	win32api.keybd_event(13,0,0,0)
	win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
	time.sleep(15)
	# 获取句柄
	hwnd = win32gui.FindWindow(None,u"QQ")
	if hwnd != 0:
		print("QQ打开成功")
	    # 隐藏窗口
		win32gui.ShowWindow(hwnd,win32con.SW_HIDE)
	else:
		print("QQ打开失败了")

def open_software_tickeys():
	win32api.ShellExecute(0, 'open', r'E:\Tickeys1.1.1\Release\TicKeys.exe', '','',1)
	time.sleep(15)
	# 获取句柄
	hwnd = win32gui.FindWindow(None,u"Tickeys")
	if hwnd != 0:
		print("Tickeys打开成功")
	    # 隐藏窗口
		win32gui.ShowWindow(hwnd,win32con.SW_HIDE)
	else:
		print("Tickeys打开失败了")


def open_software_weixin():
	# 通过Classname去获取
	win32api.ShellExecute(0, 'open', r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\微信\微信.lnk', '','',1)
	time.sleep(15)
	# 获取登录框的句柄
	hwnd = win32gui.FindWindow("WeChatLoginWndForPC",None)
	# 移动窗口并重绘
	win32gui.MoveWindow(hwnd,820,340,280,400,True)
	# 焦点关注
	win32gui.SetForegroundWindow(hwnd)
	# 鼠标聚焦
	win32api.SetCursorPos((968,615))
	# 鼠标左键按下
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,958,615)
	# 鼠标左键拾起
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,958,615)
	time.sleep(30)
	# 获取登陆后的句柄
	hwnd = win32gui.FindWindow("WeChatMainWndForPC",None)
	if hwnd != 0:
		print("微信打开成功")
	    # 隐藏窗口
		win32gui.ShowWindow(hwnd,win32con.SW_HIDE)
	else:
		print("微信打开失败了")


def sendsms():
	sender = '643008933@qq.com' # 发件人邮箱账号
	sender_pass = 'ikjdvqecdovibcba' # 发件人邮箱密码
	receiver = '643008933@qq.com' # 收件人邮箱账号
	content = '开机操作已完成'
 
	try:
		msg = MIMEText(content, 'plain', 'utf-8')
		msg['From'] = formataddr(["开机提醒", sender]) # 括号里的对应发件人邮箱昵称、发件人邮箱账号
		msg['To'] = formataddr(["", receiver]) # 括号里的对应收件人邮箱昵称、收件人邮箱账号
		msg['Subject'] = "Python 开机提醒" # 邮件的主题，也可以说是标题
 
		server = smtplib.SMTP_SSL("smtp.qq.com", 465)
		server.login(sender, sender_pass) # 括号中对应的是发件人邮箱账号、邮箱密码
		server.sendmail(sender, [receiver, ], msg.as_string()) # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
		server.quit() # 关闭连接
		print("邮件发送成功")
	except Exception:
		print("邮件发送失败")


time.sleep(60)
open_software_tickeys()
time.sleep(15)
open_software_qq()
time.sleep(15)
open_software_weixin()
time.sleep(15)
sendsms()
time.sleep(30)
sys.exit(0)

