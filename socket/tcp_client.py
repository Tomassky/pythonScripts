import socket
import time
import threading


def read(client_socket):
    while True:
        data = client_socket.recv(1024)
        data = str(data, encoding='utf-8')
        print(data)


def write(client_socket):
	while True:
		send_msg = input(">>")
		send_msg = username + ":" + send_msg + "\n"
		send_msg = send_msg.encode('utf-8')
		client_socket.send(send_msg)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 使用TCP连接
client_socket.connect(('127.0.0.1', 8088))
print("服务器连接成功")
username = input("请输入你的名字：")
write_thread = threading.Thread(target=write, args=(client_socket,))
read_thread = threading.Thread(target=read, args=(client_socket,))
write_thread.start()
read_thread.start()
write_thread.join()
read_thread.join()
client_socket.close()