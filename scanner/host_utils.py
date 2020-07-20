
def get_hosts(host):
    string_point = '.'
    string_left_slash = '/'
    host_list = []
    try:
        if host.find(string_left_slash) != -1:
            host_prefix = host[:host.rfind(string_point) + 1]
            host_list = [host_prefix + str(ip) for ip in range(1, 255)]
            return host_list
        else:
            host_list.append(host)
            return host
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
    host = '192.168.0.0/24'
    print(get_hosts(host))

    host_list = 'ip_list.txt'
    print(get_hosts_list(host_list))
