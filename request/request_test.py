import requests
# 修改访问的UA信息
header = {"User-Agent":"sqli-test"}
data = {"id":"2"}
url = "http://192.168.78.232:9002/Less-1/"
try:
	res = requests.get(url,headers=header,params=data,timeout=3)
	# POST型提交数据
	# res = requests.post(url,headers=header,params=data,timeout=3)
	# 获取网页的内容
	print(res.content.decode("utf-8"))
	print("*************************")
	# 获取提交的头信息
	print(res.request.headers)
	print("*************************")
	# 获取返回的头信息
	print(res.headers)
	print("*************************")
	# 获取提交的网址
	print(res.url)
	print("*************************")
except Exception as e:
	print("Timeout!!")

#  文件上传
# import requests
# url = "http://xxxx.com/xxx.php"
# upload_file = {"file":open("123.txt",'rb')}
# datas = {"submit":"submit"}
# res = requests.post(url,files = upload_file,data = datas)
# print(res.content.decode("utf-8"))

