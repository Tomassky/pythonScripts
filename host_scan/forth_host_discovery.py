from scapy.all import *

class ack_host_scan:
	def __init__(self,scan_ip_prefix=None,scan_file_name=None):
		self.scan_ip_prefix = scan_ip_prefix
		self.scan_file_name = scan_file_name
	def scan_host(self):
		for addr in range(0,254):
			response = sr1(IP(dst = (self.scan_ip_prefix + str(addr)))/TCP(dport = 2222,flags = 'A'),timeout = 0.1,verbose = 0)
			try:
				if int(response[TCP].flags) == 4:
					print("%s [UP]" % (self.scan_ip_prefix + str(addr)))
			except:
				pass
	def scan_file(self):
		file = open(self.scan_file_name,"r")
		for addr in file:
			response = sr1(IP(dst = addr.strip())/TCP(dport = 2222,flags = 'A'),timeout = 0.1,verbose = 0)
			try:
				if int(response[TCP].flags) == 4:
					print("%s [UP]" % (addr.strip()))
			except:
				pass

class udp_host_scan:
	def __init__(self,scan_ip_prefix=None,scan_file_name=None):
		self.scan_ip_prefix = scan_ip_prefix
		self.scan_file_name = scan_file_name
	def scan_host(self):
		for addr in range(0,254):
			response = sr1(IP(dst = (self.scan_ip_prefix + str(addr)))/UDP(dport = 33333),timeout = 0.1,verbose = 0)
			try:
				if int(response[IP].proto) == 1:
					print("%s [UP]" % (self.scan_ip_prefix + str(addr)))
			except:
				pass
	def scan_file(self):
		file = open(self.scan_file_name,"r")
		for addr in file:
			response = sr1(IP(dst = addr.strip())/UDP(dport = 33333),timeout = 0.1,verbose = 0)
			try:
				if int(response[IP].proto) == 1:
					print("%s [UP]" % (addr.strip()))
			except:
				pass

# A = udp_scan(scan_ip_prefix="192.168.0.")
# A.scan_host()