import requests
from lxml import etree
from requests.packages import urllib3
import random,time


urllib3.disable_warnings()


def spider(pages, max_change_porxies_times=300):
	"""
	抓取 XiciDaili.com 的 http类型-代理ip-和端口号

	将所有抓取的ip存入 raw_ips.csv 待处理, 可用 check_proxies() 检查爬取到的代理ip是否可用
	-----
	:param pages:要抓取多少页
	:return:无返回
	"""
	s = requests.session()
	s.trust_env = True
	s.verify = False
	urls = 'https://www.kuaidaili.com/free/intr/{}'
	proxies = {}
	try_times = 0
	for i in range(pages):
		url = urls.format(i + 1)
		s.headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Connection': 'keep-alive',
			'Referer': urls.format(i if i > 0 else ''),
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}  
		while True:
			content = s.get(url, headers=s.headers, proxies=proxies)
			# print(content.text)
			time.sleep(random.uniform(1.5, 4))  # 每读取一次页面暂停一会,否则会被封
			if content.status_code == 503:  # 如果503则ip被封,就更换ip
				proxies = get_proxies()
				try_times += 1
				print(f'第{str(try_times):0>3s}次变更,当前{proxies}')
				if try_times > max_change_porxies_times:
					print('超过最大尝试次数,连接失败!')
					return -1
				continue
			else:
				break  # 如果返回码是200 ,就跳出while循环,对爬取的页面进行处理

		print(f'正在抓取第{i+1}页数据,共{pages}页')
		for j in range(1, 10):  # 用简单的xpath提取http,host和port
			tree = etree.HTML(content.text)
			http = tree.xpath(f'//table[@class="table table-bordered table-striped"]/tbody/tr[{j}]/td[4]/text()')[0].lower()
			host = tree.xpath(f'//table[@class="table table-bordered table-striped"]/tbody/tr[{j}]/td[1]/text()')[0]
			#print(host)
			port = tree.xpath(f'//table[@class="table table-bordered table-striped"]/tbody/tr[{j}]/td[2]/text()')[0]
			check_proxies(http, host, port)  # 检查提取的代理ip是否可用


def check_proxies(http, host, port, test_url='http://www.baidu.com'):
	"""
	检测给定的ip信息是否可用

	根据http,host,port组成proxies,对test_url进行连接测试,如果通过,则保存在 ips_pool.csv 中
	:param http: 传输协议类型
	:param host: 主机
	:param port: 端口号
	:param test_url: 测试ip
	:return: None
	"""
	proxies = {http : host + ':' + port}
	try:
		res = requests.get(test_url, proxies=proxies, timeout=3)
		# print(res.text)
		if res.status_code == 200:
			print(f'{proxies}检测通过')
			with open('ips_pool.csv', 'a+') as f:
				f.write(','.join([http, host, port]) + '\n')
	except Exception as e:  # 检测不通过,就不保存,别让报错打断程序
		#print(e)
		pass


def check_local_ip(fn, test_url):
	"""
	检查存放在本地ip池的代理ip是否可用

	通过读取fn内容,加载每一条ip对test_url进行连接测试,链接成功则储存在 ips_pool.csv 文件中
	:param fn: filename,储存代理ip的文件名
	:param test_url: 要进行测试的ip
	:return: None
	"""
	print("*************二次检查获得的代理IP****************")
	with open(fn, 'r') as f:
		datas = f.readlines()
		ip_pools = []
	for data in datas:
		# time.sleep(1)
		ip_msg = data.strip().split(',')
		http = ip_msg[0]
		host = ip_msg[1]
		port = ip_msg[2]
		proxies = {http: host + ':' + port}
		try:
			res = requests.get(test_url, proxies=proxies, timeout=3)
			if res.status_code == 200:
				ip_pools.append(data)
				print(f'{proxies}检测通过')
				with open('ips_pool.csv', 'a+') as f:
					f.write('二次检查成功的IP\n')
					f.write(','.join([http, host, port]) + '\n')
		except Exception as e:
			# print(e)
			continue


def get_proxies(ip_pool_name='ips_pool.csv'):
	"""
	从ip池获得一个随机的代理ip
	:param ip_pool_name: str,存放ip池的文件名,
	:return: 返回一个proxies字典,形如:{'HTTPS': '106.12.7.54:8118'}
	"""
	with open(ip_pool_name, 'r') as f:
		datas = f.readlines()
	ran_num = random.choice(datas)
	ip = ran_num.strip().split(',')
	proxies = {ip[0]: ip[1] + ':' + ip[2]}
	return proxies


if __name__ == '__main__':
	t1 = time.time()
	spider(pages=10)
	t2 = time.time()
	print('抓取完毕,时间:', t2 - t1)
	check_local_ip('ips_pool.csv','http://www.baidu.com')