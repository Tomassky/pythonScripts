import socket
import _thread
import time

sl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # 使用UDP传输协议
sl.bind(('127.0.0.1',8888))
print("UDP监听信息已启动，等待连接......")
time.sleep(5)
print('可以发送信息了\n')

def listen_func(threadName, delay):
	while True:
		# 将socket对象绑定到指定的地址
		recv_data = sl.recvfrom(1024)
		recv_msg = recv_data[0] # 信息内容
		send_addr = recv_data[1] # 信息地址
		print('\n收到的信息：%s' % recv_msg.decode('utf-8'))
		time.sleep(delay)		

def send_func(threadName, delay):
	while True:
		ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # 使用UDP传输协议
		str1 = input("我：")
		ss.sendto(str1.encode('utf-8'), ('127.0.0.1',8088))
		time.sleep(delay)
		ss.close()
while True:
	try:
		_thread.start_new_thread(listen_func,("Thread-1",1,))
		_thread.start_new_thread(send_func,("Thread-2",1,))
		time.sleep(2)
	except:
		print("Error: unable to start thread")


sl.close()
	
