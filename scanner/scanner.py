import click

from host_utils import get_hosts, get_hosts_list
from port_utils import get_ports, get_ports_list
from host_scan import *
from port_scan import *

CONTEXT_SETTINGS = dict(help_option_names = ['-h', '--help'])

PORT_SCAN_TYPE = ["sy", "su", "st", "ss", "sc", "sn", "sf", "sx"]
HOST_SCAN_TYPE = ["pa", "pp", "pt", "pu"]


@click.command(context_settings = CONTEXT_SETTINGS, no_args_is_help = True)
@click.option('--ip', '-i',help = 'Specifies the target IP address.',
              metavar = '<ip>')
@click.option('--ip-list', '-il',
              type = click.Path(exists=True),
              help = 'Specifies the target IP addresses list file path.',
              metavar = '<ip-list>')
@click.option('--port', '-p', help = 'Specifies the target port or ports range.',
              metavar = '<port>')
@click.option('--port-list', '-pl', help = 'Specifies the target ports list file path.',
              type = click.Path(exists=True),
              metavar = '<port-list>')
@click.option('--scan-type', '-t', help = 'Specifies the scan type.',
              type = click.Choice(PORT_SCAN_TYPE + HOST_SCAN_TYPE), 
              metavar = '<scan-type>')
def scanner(ip, ip_list, port, port_list, scan_type):
    """A simple scanner tool
    
    [Usage]
        python scanner.py -i 192.168.0.1 -p 80 -t sy
        python scanner.py -i 192.168.0.1 -pl port_list.txt -t sy
        python scanner.py -i 192.168.0.0/24 -t pa
        python scanner.py -il ip_list.txt -t pa
    [Value]
       IP                  -i      192.168.0.1 | 192.168.0.0/24
       IP list             -il     ip_list.txt
       Port                -p      port1 | port1-port2 | port1,port2,port3
       Port List           -pl     port_list.txt
       Port scan type      -t      su | sy | st | ss | sn | sf | sx | sc
       Host scan type      -t      pp | pa | pn | pt
    """
    ports_list = []
    hosts_list = []
    is_host_scan = True

    # 定义局部变量
    port_scan_type = ''
    host_scan_type = ''
    scan_ip = ''
    if ip:
        hosts_list = get_hosts(ip)
        if len(hosts_list) == 1:
            scan_ip = hosts_list[0]
            is_host_scan = False
    elif ip_list:
        hosts_list = get_hosts_list(ip_list)
    if port:
        ports_list = get_ports(port)
    elif port_list:
        ports_list = get_ports_list(port_list)
    if scan_type:
        if scan_type in PORT_SCAN_TYPE:
            port_scan_type = scan_type
        if scan_type in HOST_SCAN_TYPE:
            host_scan_type = scan_type

    if not is_host_scan and port_scan_type and ports_list and scan_ip:
        scan_port = PortScanner(scan_ip = scan_ip, port_list = ports_list)
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

    if is_host_scan and host_scan_type and hosts_list:
        scan_host = HostScanner(host_list = hosts_list)
        if host_scan_type == 'pp':
            scan_host.ping_host_scan()
        elif host_scan_type == 'pa':
            scan_host.arp_host_scan()
        elif host_scan_type == 'pu':
            scan_host.udp_host_scan()
        elif host_scan_type == 'pt':
            scan_host.ack_host_scan()

if __name__ == '__main__':
    scanner()
