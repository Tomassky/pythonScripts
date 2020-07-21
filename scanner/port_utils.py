def check_port_list_avaliable(port_list):
    port_list = list(filter(lambda x: 0 <= x <= 65535, map(int, port_list)))
    return port_list


def generate_ports_in_range(start_port, end_port):
    if start_port > end_port:
        print("start_port must smaller than end_port")
        return None
    return [port for port in range(int(start_port), int(end_port) + 1)]


def get_ports(port):
    string_line = '-'
    string_comma = ','
    port_list = []
    try:
        if port.find(string_line) != -1:
            start_port, end_port = port.split("-")
            port_list = generate_ports_in_range(start_port, end_port)
            port_list = check_port_list_avaliable(port_list)
            return port_list
        elif port.find(string_comma) != -1:
            port_list = port.split(",")
            port_list = check_port_list_avaliable(port_list)
            return port_list
        else:
            port_list = generate_ports_in_range(port, port)
            port_list = check_port_list_avaliable(port_list)
            return port_list
    except Exception as reason:
        raise reason
        print("端口的形式出错！！")
        return None


def get_ports_list(port_list_path):
    if port_list_path.endswith(".txt"):
        with open(port_list_path, "r+") as fp:
            port_list = [int(port.strip()) for port in fp.readlines()]
        return port_list

    return None


if __name__ == '__main__':
    port = '805'
    print(get_ports(port))

    port_list = 'port_list.txt'
    print(get_ports_list(port_list))
