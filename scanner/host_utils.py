def cidr2dot_decimal_address(cidr_address):
    host, cidr_prefix_length = cidr_address.split('/')
    address_list = list(map(int, host.split('.')))
    cidr_prefix_length = int(cidr_prefix_length)
    if not 0 <= cidr_prefix_length <= 32:
        raise ValueError('CIDR prefix length is error')
    mask_list = [min(num, 8) for num in range(cidr_prefix_length, 0, -8)]
    mask_list = [(0xFF00 >> num) & 0xFF for num in mask_list]
    mask_list.extend([0] * (4 - len(mask_list)))

    return address_list, mask_list


def padding_zeros(msg, target_len):
    diff_len = target_len - len(msg)
    return '0' * (diff_len) + msg if diff_len > 0 else msg


def ip2hex(ip_address):
    if isinstance(ip_address, str):
        ip_address = ip_address.split('.')

    result = []
    for i in range(4):
        hex_temp = hex(int(ip_address[i]))[2:]
        result.append(padding_zeros(hex_temp, 2))

    return ''.join(result)


def hex2ip(hex_ip):
    result = []
    hex_list = [hex_ip[i: i + 2] for i in range(0, len(hex_ip), 2)]

    for hex_str in hex_list:
        dec_temp = int(hex_str, 16)
        result.append(dec_temp)

    return result


def get_available_network_address(address_list, mask_list):
    # /32 -> Only one host
    if mask_list[-1] == 255:
        return address_list

    network_address, broadcast_address = [], []
    for addr, mask in zip(address_list, mask_list):
        network_address.append(addr & mask)
        broadcast_address.append(addr | (~mask & 255))

    # /31 -> Two hosts
    if mask_list[-1] != 254:
        network_address[-1] += 1
        broadcast_address[-1] -= 1

    start_address = int(ip2hex(network_address), 16)
    end_address = int(ip2hex(broadcast_address), 16)
    result_list = [map(str, hex2ip(hex(i)[2:]))
                   for i in range(start_address, end_address + 1)]
    result_list = list(map(lambda x: '.'.join(x), result_list))
    return result_list


def get_hosts(host):
    string_left_slash = '/'
    host_list = []
    try:
        if string_left_slash in host:
            address_list, mask_list = cidr2dot_decimal_address(host)
            host_list = get_available_network_address(address_list, mask_list)
            return host_list
        else:
            host_list.append(host)
            return host_list
    except Exception as reason:
        print(reason)
        print("主机的形式出错！！")
        return None


def get_hosts_list(host_list_path):
    if host_list_path.endswith(".txt"):
        with open(host_list_path, "r+") as fp:
            host_list = [host.strip() for host in fp.readlines()]
        return host_list

    return None


if __name__ == '__main__':
    host = '192.168.11.8/24'
    print(get_hosts(host))

    host_list = 'ip_list.txt'
    print(get_hosts_list(host_list))
