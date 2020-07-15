import socket
import paramiko
import threading
import sys

# 使用 Paramiko 示例文件的密钥
host_key = paramiko.RSAKey(filename='test_rsa.key')
class Server(paramiko.ServerInterface):
	def _init_(self):
		self.event = threading.Event()
	def check_channel_request(self,kind,chanid):
		if kind == 'session':
			return paramiko.OPEN_SUCCEEDED
		return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
	def check_auth_password(self,username,password):
		if (username == 'tomas') and (password == 'root'):
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED

server = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	sock.bind((server,ssh_port))
	sock.listen(100)
	print('[+] Listening for connection ...')
	client,addr = sock.accept()
except Exception as e:
	print('[-] Listen failed: ' + str(e))
	sys.exit(1)
print('[+] Got a connection')

try:
	tomas_session = paramiko.Transport(client)
	tomas_session.add_server_key(host_key)
	server = Server()
	try:
		tomas_session.start_server(server=server)
	except paramiko.SSHException as sx:
		print('[-] SSH negotiation failed.')
	chan = tomas_session.accept(20)
	print('[+] Authenticated!')
	print(str(chan.recv(1024)))
	chan.send(('Welcome to tomas_ssh').encode('utf-8'))
	while True:
		try:
			command = input("Enter command: ").strip('\n')
			if command != 'exit':
				chan.send(command.encode('utf-8'))
				print(str(chan.recv(4096)))
			else:
				chan.send('exit'.encode('utf-8'))
				print('exiting')
				tomas_session.close()
				raise Exception ('exit')
		except KeyboardInterrupt:
			tomas_session.close()
except Exception as e:
	print('[-] Caught exception: '+str(e))
	try:
		tomas_session.close()
	except:
		pass
	sys.exit(1)