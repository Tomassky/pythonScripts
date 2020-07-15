import sys

def choice_host(host):
	string_point = '.'
	string_left_slash = '/'
	host_list = []
	try:
		if host.find(string_point) != -1 and host[-3:] == 'txt':
			fp = open(host)
			for host in fp.readlines():
				host_list.append(str(host).strip())
				fp.close()
			return host_list
		elif (host.find(string_left_slash) != -1):
			host_prefix = host.split(".")[0] + "." + host.split(".")[1] + "."+ host.split(".")[2] + "."
			for number in range(0,255):
				host_list.append(str(host_prefix + str(number)))
			return host_list
		else:
			host = host.split(".")[0] + "." + host.split(".")[1] + "."+ host.split(".")[2] + "." + host.split(".")[3]
			host_list.append(host)
			return host_list
	except Exception as reason:
		print(reason)
		print("主机的形式出错！！")
		sys.exit()

# host = 'ip_list.txt'
# print(choice_host(host))