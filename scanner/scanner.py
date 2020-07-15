import time
import os
import time
import sys
import getopt
from host_scan import *
from port_scan import *

# 定义全局变量
port_scan_type_opts = ["sy","su","st","ss","sc","sn","sf","sx"]
host_scan_type_opts = ["pa","pp","pt","pu"]
post_list = []
host_list = []
host_count = 0

def usage():
	print("\n")
	print("\t\t\t---------------------------------------------------------------------------------")
	print("\t\t\t|[Usage]									|")
	print("\t\t\t	python scanner.py -i 192.168.0.1 -p 80 -t sy ")
	print("\t\t\t|	python scanner.py -i 192.168.0.0/24 -t pa 				|")
	print("\t\t\t---------------------------------------------------------------------------------")
	print("\t\t\t|[Value]									|")
	print("\t\t\t	IP 		-i 	192.168.0.1 | 192.168.0.0/24 | ip_list.txt")
	print("\t\t\t|	Port 	-p 	port1 | port1-port2 | port1,port2,port3 | port.txt	|")
	print("\t\t\t	Port_scan 	-t 	su | sy | st | ss | sn | sf | sx | sc")
	print("\t\t\t|	Host_scan 	-t 	pp | pa | pn | pt 				|")
	print("\t\t\t---------------------------------------------------------------------------------")
	print("\n")
	sys.exit()

def main():
	global port_scan_type_opts
	global host_scan_type_opts
	global post_list
	global host_list
	global host_count

	# 定义局部变量
	port_scan_type = ""
	host_scan_type = ""
	scan_ip = ""

	if not len(sys.argv[1:]):
		usage()

	try:
		opts,args = getopt.getopt(sys.argv[1:],"hi:p:t:",["help","port","type"])
	except getopt.GetoptError as err:
		print(err)
		usage()

	for o,a in opts:
		if o in ("-h","--help"):
			usage()
		elif o in ("-i","--ip"):
			host_list = choice_host(a)
			if len(host_list) == 1:
				host_count = 1
				scan_ip = host_list[0]
			else:
				host_count = 0
		elif o in ("-p","--port"):
			port_list = choice_port(a) 
		elif o in ("-t","--type"):
			if a in port_scan_type_opts:
				port_scan_type = a
				break
			elif a in host_scan_type_opts:
				host_scan_type = a
				break
		else:
			print("Unhanled Option")

	if host_count == 1 and port_list and port_scan_type and host_list and not host_scan_type:
		scan_port = port_scan(scan_ip = scan_ip,port_list = port_list)
		if port_scan_type == 'sy':
			scan_port.syn_port_scan()
		elif port_scan_type == 'st':
			scan_port.tcp_port_scan()
		elif port_scan_type == 'su':
			scan_port.udp_port_scan()
		elif port_scan_type == 'ss':
			scan_port.socket_port_scan()
		elif port_scan_type == 'sc':
			scan_port.common_list_port_scan()
		elif port_scan_type == 'sn':
			scan_port.null_port_scan()
		elif port_scan_type == 'sf':
			scan_port.fin_port_scan()
		elif port_scan_type == 'sx':
			scan_port.xmas_port_scan()
	if host_count == 0 and host_list and host_scan_type and not port_scan_type:
		scan_host = host_scan(host_list=host_list)
		if host_scan_type == 'pp':
			scan_host.ping_host_scan()
		elif host_scan_type == 'pa':
			scan_host.arp_host_scan()
		elif host_scan_type == 'pu':
			scan_host.udp_host_scan()
		elif host_scan_type == 'pt':
			scan_host.ack_host_scan()

main()