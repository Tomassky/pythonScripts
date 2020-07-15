from host_type import *
from scapy.all import *

class host_scan:
	def __init__(self,host_list=None):
		self.host_list = host_list
	def ping_host_scan(self):
		try:
			for addr in self.host_list:
				response = sr1(IP(dst = addr)/ICMP(),timeout = 0.1,verbose = 0)
				if response == None:
					pass
				else:
					print("%s [UP]" % (addr))
		except Exception as reason:
			print(reason)
	def arp_host_scan(self):
		try:
			for addr in self.host_list:
				response = sr1(ARP(pdst = addr),timeout = 0.1,verbose = 0)
				if response == None:
					pass
				else:
					print("%s [UP]" % (addr))
		except Exception as reason:
			print(reason)
	def ack_host_scan(self):
		try:
			for addr in self.host_list:
				response = sr1(IP(dst = addr)/TCP(dport = 2222,flags = 'A'),timeout = 0.1,verbose = 0)
				try:
					if int(response[TCP].flags) == 4:
						print("%s [UP]" % (addr))
				except:
					pass
		except Exception as reason:
			print(reason)
	def udp_host_scan(self):
		try:
			for addr in self.host_list:
				response = sr1(IP(dst = addr)/UDP(dport = 33333),timeout = 0.1,verbose = 0)
				try:
					if int(response[IP].proto) == 1:
						print("%s [UP]" % (addr))
				except:
					pass
		except Exception as reason:
			print(reason)