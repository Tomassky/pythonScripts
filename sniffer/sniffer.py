import socket
import os
import struct
import threading
import time
from ctypes import *

# 监听的主机
host = "192.168.0.104"

# IP头定义
class IP(Structure):
	_fields_ = [
		("ihl",			c_ubyte,4),
		("version",		c_ubyte,4),
		("tos",			c_ubyte),
		("len",			c_ushort),
		("id",			c_ushort),
		("offset",		c_ushort),
		("ttl",			c_ubyte),
		("protocol_num",c_ubyte),
		("sum",			c_ushort),
		("src",			c_ulong),
		("dst",			c_ulong)]

	def __new__(self,socket_buffer=None):
		return self.from_buffer_copy(socket_buffer)
	def __init__(self,socket_buffer=None):
		# 协议字段与协议名称对应
		self.protocol_map = {1:"ICMP",6:"TCP",17:"UDP",41:"IPv6",2:"IGMP"}
		# 可读性更强的IP地址
		self.src_address = socket.inet_ntoa(struct.pack("<L",self.src))
		self.dst_address = socket.inet_ntoa(struct.pack("<L",self.dst))
		# 协议类型
		try:
			self.protocol = self.protocol_map[self.protocol_num]
		except:
			self.protocol = str(self.protocol_num)

class TCP(Structure):
	_fields_ = [
		("th_sport",		c_ushort),
		("th_dport",		c_ushort),
		("seq",				c_uint),
		("ack",				c_uint)]
	def __new__(self,socket_buffer):
		return self.from_buffer_copy(socket_buffer)
	def __init__(self,socket_buffer):
		self.src_port = socket.ntohs(self.th_sport)
		self.dst_port = socket.ntohs(self.th_dport)

class UDP(Structure):
	_fields_ = [
		("th_sport",		c_ushort),
		("th_dport",		c_ushort)]
	def __new__(self,socket_buffer):
		return self.from_buffer_copy(socket_buffer)
	def __init__(self,socket_buffer):
		self.src_port = socket.ntohs(self.th_sport)
		self.dst_port = socket.ntohs(self.th_dport)

# 下面的代码类似于之前的例子
if os.name == "nt":
	socket_protocol = socket.IPPROTO_IP
else:
	socket_protocol = socket.IPPROTO_ICMP
sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)
sniffer.bind((host,0))
sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
if os.name == "nt":
	sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)
try:
	while True:
		# 读取数据包
		raw_buffer = sniffer.recvfrom(65565)[0]
		#print(raw_buffer)
		# 将缓冲区的前20个字节按IP头进行解析
		ip_header = IP(raw_buffer[0:20])
		if ip_header.protocol == "TCP":
			tcp_header = TCP(raw_buffer[20:40])
			tls_header = raw_buffer[41:43]
			if (("HTTP").encode('utf-8')) in (raw_buffer[20:]):
				print("Protocol: HTTP %s:%s -> %s:%s" % (ip_header.src_address,tcp_header.src_port,ip_header.dst_address,tcp_header.dst_port))
			elif (("\x03\x03").encode('utf-8')) == tls_header:
				print("Protocol: TLS %s:%s -> %s:%s" % (ip_header.src_address,tcp_header.src_port,ip_header.dst_address,tcp_header.dst_port))
			else:
				print("Protocol: TCP %s:%s -> %s:%s" % (ip_header.src_address,tcp_header.src_port,ip_header.dst_address,tcp_header.dst_port))
		if ip_header.protocol == "UDP":
			udp_header = UDP(raw_buffer[20:40])
			if udp_header.src_port == 53 or udp_header.dst_port == 53:
				print("Protocol: DNS %s:%s -> %s:%s" % (ip_header.src_address,udp_header.src_port,ip_header.dst_address,udp_header.dst_port))
			elif udp_header.src_port == 4002 or udp_header.src_port == 8000 or udp_header.dst_port == 4002 or udp_header.dst_port == 8000:
				print("Protocol: OICQ %s:%s -> %s:%s" % (ip_header.src_address,udp_header.src_port,ip_header.dst_address,udp_header.dst_port))
			elif udp_header.src_port == 1900 or udp_header.dst_port == 1900:
				print("Protocol: SSDP %s:%s -> %s:%s" % (ip_header.src_address,udp_header.src_port,ip_header.dst_address,udp_header.dst_port))
			else:
				print("Protocol: UDP %s:%s -> %s:%s" % (ip_header.src_address,udp_header.src_port,ip_header.dst_address,udp_header.dst_port))
# 处理 CTRL-C
except KeyboardInterrupt:
	# 如果运行在 Windows 上，关闭混杂模式
	if os.name == "nt":
		sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF) 