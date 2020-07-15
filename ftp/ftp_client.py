import sys
from ftplib import FTP

command_list = []

def ftp_connect(host,port,username,password):
    ftp = FTP()
    ftp.connect(host,port)
    ftp.login(username, password)
    ftp.getwelcome()
    return ftp

def ftp_download(ftp,remotefile,localfile):
    f = open(localfile, 'wb')
    ftp.retrbinary('RETR ' + remotefile,f.write)
    f.close()
def ftp_upload(ftp,remotefile, localfile):
    bufsize = 1024
    fp = open(localfile, 'rb')
    ftp.storbinary('STOR ' + remotefile,fp,bufsize)
    fp.close()

host = input("> Please input the host: ")
port = int(input("> Please input the port: "))
username = input("> Please input the username: ")
password = input("> Please input the password:")

ftp = ftp_connect(host,port,username,password)


while True:
	command = input("ftp>")
	command_list = command.split()
	if command_list[0] == 'get':
		try:
			ftp_download(ftp, command_list[1], command_list[1])
			print("<<<<< Download Done")
		except Exception as reason:
			print(reason)
	elif command_list[0] == 'put':
		try:
			ftp_upload(ftp, command_list[1], command_list[1])
			print(">>>>> Upload Done")
		except Exception as reason:
			print(reason)
	elif command_list[0] == 'dir':
		try:
			file_list = ftp.nlst()
			for file in file_list:
				print("\t" + file)
		except Exception as reason:
			print(reason)
	elif command_list[0] == 'quit':
		try:
			ftp.quit()
			sys.exit(0)
		except Exception as reason:
			print(reason)
	elif command_list[0] == 'cd':
		try:
			ftp.cwd(command_list[1])
		except Exception as reason:
			print(reason)
	else:
		print("Invaid Arguments")

ftp.quit()
