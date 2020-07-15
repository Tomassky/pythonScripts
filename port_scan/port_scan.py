import time
import socket
import sys
import os
import pickle
from scapy.all import *

if len(sys.argv)!=4:
	print("--------------------------------------------------------------------")
	print("[Usage]")
	print("	python port_scan.py [Target IP] [Target Port] [Scan Type] ")
	print("	python port_scan.py 192.168.100.1 1-200 -sy")
	print("--------------------------------------------------------------------")
	print("[Value]")
	print("	IP 	single ip")
	print("	Port 	port1 | port1-port2 | port1,port2,port3 | port.txt")
	print("	Type 	-su | -sy | -st | -ss | -sn | -sf | -sx | -sc")
	print("--------------------------------------------------------------------")
	sys.exit()

ip = sys.argv[1]
port = sys.argv[2]
form = sys.argv[3]


def detection(port_list=[],start_port=0,end_port=0):
	
	if start_port != 0 or end_port != 0:
		if start_port > end_port:
			print("start_port must smaller than end_port")
			sys.exit()
		for port in range(start_port,end_port):	
			port_list.append(port)
	for port in port_list:
		if int(port) > 65535 or int(port) < 0:
			print("port must be 0-65535")
			sys.exit()
	return port_list


def choice_port():
	global port
	string_line = '-'
	string_comma = ','
	string_point = '.'
	port_list = []
	try:
		# IP地址段的判断，以横线为基准
		if (port.find(string_line) != -1):
			port = port.split("-")
			start_port = int(port[0])
			end_port = int(port[1]) + 1
			port_list = detection(port_list,start_port,end_port)
			return port_list
		# 多IP地址的判断，以逗号为就基准
		elif (port.find(string_comma) != -1):
			port_list_tmp = port.split(",")
			post_list_tmp = detection(port_list_tmp)
			for port in port_list_tmp:
				port_list.append(int(port))
			return port_list
		# ip列表的判断，以点和txt后缀为基准
		elif port.find(string_point) != -1 and port[-3:] == 'txt':
			fp = open(port)
			for port in fp.readlines():
				port_list.append(int(port))
				fp.close()
			detection(port_list)
			return port_list
		# 单地址IP的判断，以及其他情况的判断
		else:
			start_port = int(port)
			end_port = int(port) + 1
			port_list = detection(port_list,start_port,end_port)
			return port_list	
	except Exception as reason:
		print(reason)
		sys.exit()
	# 缺乏对打开文件的关闭操作
	# finally:
		# if fp == True:
			# fp.close()
	

def port_scan():
	global ip,form
	port_list = choice_port()
	(role,scan_type) = form.split('-',1)
	scan_type = scan_type.lower()
	try:
		if scan_type == 'sy':
			# syn 扫描
			for port in port_list:
				response = sr1(IP(dst=ip)/TCP(dport=port),timeout=1,verbose=0)
				if response == None:
					pass
				elif int(response[TCP].flags) == 18:
					print("%d [OPEN]" % port)
				else:
					pass
		elif scan_type == 'st':
			# tcp 扫描
			for port in port_list:
				response = sr1(IP(dst=ip)/TCP(dport=port,flags="S"),timeout=1,verbose=0)
				if response == None:
					pass
				elif int(response[TCP].flags) == 18:
					response = sr1(IP(dst=ip)/TCP(dport=port,flags="A",ack=(response[TCP].seq+1)),timeout=1,verbose=0)
					print("%d [OPEN]" % port)
				else:
					pass
		elif scan_type == 'su':
			# udp 扫描
			for port in port_list:
				response = sr1(IP(dst=ip)/UDP(dport=port),timeout=5,verbose=0)
				time.sleep(0.5)
				if response == None:
					print("%d [OPEN]" % port)
				else:
					pass
		elif scan_type == 'ss':
			# socket 扫描
			for port in port_list:
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.settimeout(2)
				result_code = s.connect_ex((ip,port))
				if result_code == 0:
					print("%d [OPEN]" % port)
				else:
					continue
				s.close()
		elif scan_type == 'sc':
			# 常用端口扫描
			pickle_file = open('common_port_list.pkl','rb')
			port_list = pickle.load(pickle_file)
			for port in port_list:
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.settimeout(2)
				result_code = s.connect_ex((ip,port))
				if result_code == 0:
					print("%d [OPEN]" % port)
				else:
					continue
				s.close()
		elif scan_type == 'sn':
			# NULL扫描
			for port in port_list:
				response = sr1(IP(dst=ip)/TCP(dport=port,flags=""),timeout=5,verbose=0)
				time.sleep(0.5)
				if response == None:
					pass
				elif int(response[TCP].flags) == 4:
					print("%d [OPEN]" % port)
				else:
					pass
		elif scan_type == 'sf':
			# Fin扫描
			for port in port_list:
				response = sr1(IP(dst=ip)/TCP(dport=port,flags="F"),timeout=5,verbose=0)
				time.sleep(3)
				if response == None:
					pass
				elif int(response[TCP].flags) == 4:
					print("%d [OPEN]" % port)
				else:
					pass
		elif scan_type == 'sx':
			# Xmas扫描
			for port in port_list:
				response = sr1(IP(dst=ip)/TCP(dport=port,flags="UPF"),timeout=5,verbose=0)
				time.sleep(0.5)
				if response == None:
					pass
				elif int(response[TCP].flags) == 4:
					print("%d [OPEN]" % port)
				else:
					pass	
		else:
			print("参数存在问题")
			sys.exit()
	except Exception as reason:
		print(reason)
	# 缺乏对socket的关闭操作
	# finally:
		#s.close()				


port_scan()