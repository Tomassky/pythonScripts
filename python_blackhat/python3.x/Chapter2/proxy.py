import sys
import socket
import threading

# 对目标是远程主机的请求进行修改
def request_handler(buffer):
	# 执行包修改
	return buffer

# 对目标是本机主机的响应进行修改
def response_handler(buffer):
	# 执行包修改
	return buffer


def hexdump(src,length = 16):
	result = []
	digits = 2 if isinstance(src,str) else 4
	for i in range(0,len(src),length):
		s = src[i:i+length]
		hexa = ' '.join(["%0*X" % (digits,ord(x)) for x in s])
		text = ''.join([x if 0x20 <= ord(x) < 0x7f else b'.' for x in s])
		result.append("%04X  %-*s  %s" % (i,length*(digits + 1),hexa,text))
	for i in result:
		print(i)


def receive_from(connection):
	buffer = ""
	# 我们设置了两秒的超时，这取决于目标的情况，可能需要调整
	# connection.settimeout(4)
	try:
	# 持续从缓存中读取数据直到没有数据或者超时
		while True:
			data = str(connection.recv(4096))
			data = ((data[2:])[:-1])
			if not data:
				break
			buffer += data
			return buffer
	except:
		print("ERROR")
	

def proxy_handler(client_socket,remote_host,remote_port,receive_first):
	# 连接远程主机
	remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	remote_socket.connect((remote_host,remote_port))
	# 如果必要从远程主机接受数据
	if receive_first:
		remote_buffer = receive_from(remote_socket)
		hexdump(remote_buffer)
		#发送给我们的响应处理
		remote_buffer = response_handler(remote_buffer)
		# 如果我们有数据传递给本地客户端，发送它
		if len(remote_buffer):
			print("[<==] Send %d bytes to localhost." % len(remote_buffer))
			client_socket.send(remote_buffer.encode('utf-8'))
	# 现在我们从本地循环读取数据，发送给远程主机和本地主机
	while True:
		# 从本地读取数据
		local_buffer =  receive_from(client_socket)
		if len(local_buffer):
			print("[==>] Received %d bytes from localhost." % len(local_buffer))
			hexdump(local_buffer)
			# 发送给我们的本地请求
			local_buffer = request_handler(local_buffer)
			# 向远程主机发送数据
			remote_socket.send(local_buffer.encode('utf-8'))
			print("[==>] Send to remote.")
		# 接收响应的数据
		remote_buffer = receive_from(remote_socket)
		if len(remote_buffer):
			print("[<==] Received %d bytes from remote." % len(remote_buffer))
			hexdump(remote_buffer)
			# 发送到响应处理函数
			remote_buffer = response_handler(remote_buffer)
			# 将响应发送给本地socket
			client_socket.send(remote_buffer.encode('utf-8'))
			print("[<==] Sent to localhost")
		# 如果两边都没有数据，关闭连接
		if not len(local_buffer) or not len(remote_buffer):
			client_socket.close()
			remote_socket.close()
			print("[*] No more data. Closing connections")
			break


def server_loop(local_host,local_port,remote_host,remote_port,receive_first):
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		server.bind((local_host,local_port))
	except:
		print("[!!] Failed to listen on %s:%d" % (local_host,local_port))
		print("[!!] Check for other listening sockets or corret permissions")
		sys.exit()
	print("[*] Listening on %s:%d" % (local_host,local_port))
	server.listen(5)
	while True:
		client_socket,client_address = server.accept()
		# 打印出本地连接信息
		print("[==>] Received incoming connection from %s:%d" % (client_address[0],client_address[1]))
		# 开启一个线程与远程主机通信
		proxy_thread = threading.Thread(target=proxy_handler,args=(client_socket,remote_host,remote_port,receive_first))
		proxy_thread.start()



def main():
	# 没有华丽的命令行解析
	if len(sys.argv[1:]) != 5:
		print("Usage: python proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
		print("Example: python proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
		sys.exit()
	# 设置本地监听参数
	local_host = sys.argv[1]
	local_port = int(sys.argv[2])
	# 设置远程目标
	remote_host = sys.argv[3]
	remote_port = int(sys.argv[4])
	# 告诉代理在发送给远程主机之前连接和接受数据
	receive_first = sys.argv[5]
	if "True" in receive_first:
		receive_first = True
	else:
		receive_first = False
	# 现在设置好我们的监听socket
	server_loop(local_host,local_port,remote_host,remote_port,receive_first)


main()