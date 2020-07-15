from tkinter import *
from datetime import datetime
from tkinter.messagebox import *


class TestTime(object):
	def __init__(self, master=None):
		self.root = master
		self.root.geometry('200x350')
		self.root.resizable(width=False, height=False)
		self.updatetime()

	def updatetime(self):
		self.labelA = Label(self.root, text='当前本地时间为：\t\t')
		self.labelA.pack()
		self.labelB = Label(self.root, text="")
		self.labelB.pack()
		self.labelC = Label(self.root, text='\n今日倒计时：\t\t')
		self.labelC.pack()
		self.labelD = Label(self.root, text="")
		self.labelD.pack()
		# self.labelE = Label(self.root, text='\n距离今天下班还有：\t\t')
		# self.labelE.pack()
		# self.labelF = Label(self.root, text="")
		# self.labelF.pack()
		self.labelG = Label(self.root, text="\n行程安排：\t\t")
		self.labelG.pack()
		self.labelH = Label(self.root, text="7月15日  数据安全考试")
		self.labelH.pack()
		self.labelL = Label(self.root, text="7月19日  微机系统考试")
		self.labelL.pack()
		self.labelM = Label(self.root, text="7月21日  52破解论坛注册")
		self.labelM.pack()
		self.labelN = Label(self.root, text="8月28日  回校报道注册")
		self.labelN.pack()
		self.labelO = Label(self.root, text="\n今日任务：\t\t")
		self.labelO.pack()
		self.labelP = Label(self.root, text="协议层的解析")
		self.labelP.pack()

		self.updateA()
		self.updateB()
		# self.updateC()

	def updateA(self):
		self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		self.labelB.configure(text=self.now)
		self.root.after(1000, self.updateA)

	def updateB(self):
		# 获取当日日期，不包含时间，str
		self.nowday = datetime.now().strftime("%Y-%m-%d")
        # 字符串拼接，组成当日12点
		a = self.nowday + ' 23:59:59'
		self.newtime = datetime.strptime(a, "%Y-%m-%d %H:%M:%S")
		p = str(self.newtime - datetime.now()).split('.')[0].split(':')
		if "-1 day" in str(self.newtime - datetime.now()):
			test = '今天过完了，明天加把劲吧！'
			showinfo(title='一天过去了', message='该睡觉了，兄弟！！！！')
		else:
			test = "%s 小时 %s分钟 %s 秒" % (p[0], p[1], p[2])
		self.labelD.configure(text=test)
		self.root.after(1000, self.updateB)


if __name__ == '__main__':
	root = Tk()
	root.title('计时小界面')
	# 窗口置顶.
	root.wm_attributes('-topmost', 1)
	TestTime(root)
	root.mainloop()