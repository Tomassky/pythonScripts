import pickle
from scapy.all import *


class PortScanner:

    def __init__(self, scan_ip, port_list):
        self.scan_ip = scan_ip
        self.port_list = port_list

    def syn_port_scan(self):
        try:
            for port in self.port_list:
                response = sr1(IP(dst=self.scan_ip) / TCP(dport=port),
                               timeout=1, verbose=0)

                if response:
                    if int(response[TCP].flags) == 18:
                        print("%d [OPEN]" % port)
        except Exception as reason:
            print(reason)

    def tcp_port_scan(self):
        try:
            for port in self.port_list:
                response = sr1(IP(dst=self.scan_ip) / TCP(dport=port, flags="S"),
                               timeout=1, verbose=0)

                if response:
                    if int(response[TCP].flags) == 18:
                        response = sr1(
                            IP(dst=self.scan_ip) / TCP(dport=port,
                                                       flags="A",
                                                       ack=(response[TCP].seq + 1)),
                            timeout=1, verbose=0)

                        print("%d [OPEN]" % port)
        except Exception as reason:
            print(reason)

    def udp_port_scan(self):
        try:
            for port in self.port_list:
                response = sr1(IP(dst=self.scan_ip) / UDP(dport=port),
                               timeout=1, verbose=0)

                time.sleep(0.5)
                if response:
                    print("%d [OPEN]" % port)
        except Exception as reason:
            print(reason)

    def socket_port_scan(self):
        try:
            for port in self.port_list:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                result_code = s.connect_ex((self.scan_ip, port))
                if result_code == 0:
                    print("%d [OPEN]" % port)
                else:
                    continue
                s.close()
        except Exception as reason:
            print(reason)

    def common_list_port_scan(self):
        with open('common_port_list.pkl', 'rb') as pickle_file:
            port_list = pickle.load(pickle_file)
            for port in port_list:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                result_code = s.connect_ex((self.scan_ip, port))
                if result_code == 0:
                    print("%d [OPEN]" % port)
                else:
                    continue

    def null_port_scan(self):
        try:
            for port in self.port_list:
                response = sr1(IP(dst=self.scan_ip) / TCP(dport=port,
                                                          flags=""),
                               timeout=1, verbose=0)
                time.sleep(0.5)
                if response:
                    if int(response[TCP].flags) == 4:
                        print("%d [OPEN]" % port)
        except Exception as reason:
            print(reason)

    def fin_port_scan(self):
        try:
            for port in self.port_list:
                response = sr1(IP(dst=self.scan_ip) / TCP(dport=port,
                                                          flags="F"),
                               timeout=1, verbose=0)
                time.sleep(3)
                if response:
                    if int(response[TCP].flags) == 4:
                        print("%d [OPEN]" % port)
        except Exception as reason:
            print(reason)

    def xmas_port_scan(self):
        try:
            for port in self.port_list:
                response = sr1(IP(dst=self.scan_ip) / TCP(dport=port,
                                                          flags="UPF"),
                               timeout=1, verbose=0)
                time.sleep(0.5)
                if response:
                    if int(response[TCP].flags) == 4:
                        print("%d [OPEN]" % port)
        except Exception as reason:
            print(reason)


if __name__ == '__main__':
    port_list = []
    for port in range(0, 30):
        port_list.append(port)

    A = xmas_port_scan(scan_ip="118.31.72.36", port_list=port_list)
    A.scan()
