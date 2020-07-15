import threading
import paramiko
import subprocess

def ssh_command(ip,user,passwd,command):
	client = paramiko.SSHClient()
	# 目的是接受不在本地Known_host文件下的主机
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip,username=user,password=passwd)
	#  取底层的 transport 对象, 用于执行低级的任务 open_channel() session 的简写
	ssh_session = client.get_transport().open_session()
	if ssh_session.active:
		ssh_session.exec_command(command)
		print(ssh_session.recv(1024))

while True:
	command = input("请输入命令：")
	ssh_command('192.168.0.111','tomas','root',command)
