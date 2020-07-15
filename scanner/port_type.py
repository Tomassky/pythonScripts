import sys

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


def choice_port(port):
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
		print("端口的形式出错！！")
		sys.exit()

# port = 'port_list.txt'
# print(choice_port(port))