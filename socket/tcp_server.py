import socket
import time
import threading
import _thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # 使用ipv4通信，使用TCP传输协议
s.bind(('127.0.0.1', 8088))       # 将socket对象s绑定到指定的地址
s.listen(5)                     # 开始监听TCP连接
print("服务器已启动，等待连接......")

sockets = []

def handle_client(client_socket,sockets):
	while 1:
		data = client_socket.recv(1024)      # 一次最多接收1024B
		if len(data) > 0:
			for socket in sockets:
				if socket != client_socket:
					socket.send(data)
		if data == 'exit':
			conn.close()
			break


while True:
	try:
		(client_socket,client_address) = s.accept()
		sockets.append(client_socket)
		client_handler = threading.Thread(target = handle_client,args=(client_socket,sockets,))
		client_handler.start()
	except:
		print("Error: unable to start thread")


s.close()
