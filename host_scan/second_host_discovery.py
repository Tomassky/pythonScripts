from scapy.all import *

class arp_host_scan:
	def __init__(self,scan_ip_prefix=None,scan_file_name=None):
		self.scan_ip_prefix = scan_ip_prefix
		self.scan_file_name = scan_file_name
	def scan_host(self):
		for addr in range(0,254):
			response = sr1(ARP(pds = (self.scan_ip_prefix + str(addr))),timeout = 0.1,verbose = 0)
			if response == None:
				pass
			else:
				print("%s [UP]" % (self.scan_ip_prefix + str(addr)))
	def scan_file(self):
		file = open(self.scan_file_name,"r")
		for addr in file:
			response = sr1(ARP(pdst = addr.strip()),timeout = 0.1,verbose = 0)
			if response == None:
				pass
			else:
				print("%s [UP]" % (addr.strip()))



# A = arp_scan(scan_file_name="iplist.txt")
# A.scan_file()