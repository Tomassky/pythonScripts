import tkinter as tk
from ftplib import FTP
from inspect import getfile
from tkinter import scrolledtext
import tkinter.messagebox as tmb
from tkinter import filedialog
from tkinter.filedialog import askdirectory


def server_con():
    try:
        # 连接信息
        ip_add = var_server_ip.get()
        usr_name = var_username.get()
        usr_pass = var_user_pass.get()
        # ftp = FTP()
        ftp.encoding = 'GB18030'
        ftp.connect(ip_add, 2121)
        ftp.login(usr_name, usr_pass)
        conn_text.insert('insert', '服务器信息：\n' + str(ftp) + '\n')
        conn_text.insert('insert', '*****************\n' + str(ftp.getwelcome()) + '\n')
        conn_text.insert('insert', '*****************\n【Done!Connected!】')
        # Directory
        ftp.cwd("/")
        file_list = []
        # 读取目录下的文件列表
        ftp.retrlines('LIST', file_list.append)
        for f in file_list:
            print(ftp.pwd() + f[10:])
            list_text.insert('insert', ftp.pwd() + f[10:] + '\n')
        return ftp

    except Exception as error:
        tmb.showwarning('错误', str(error))


def download_window():
    def scan_file():
        var_file_list = ftp.nlst()
        for i in range(len(var_file_list)):
            file_list.insert(i, var_file_list[i])

    def download():
        path = askdirectory()
        val = file_list.get(file_list.curselection())
        new_path = path + '/'+val
        try:
            f = open(new_path, 'wb')
            ftp.retrbinary('RETR %s' % val, f.write)
            tmb.showinfo('提示', '下载成功！')
        except Exception as error:
            tmb.showerror('错误', error)

    dow_window = tk.Toplevel(window)
    dow_window.title('下载')
    dow_window.geometry('530x400')
    dow_window.resizable(width=False, height=False)
    tk.LabelFrame(dow_window, text='文件目录', width=520, height=355).place(x=5, y=10)
    #
    file_list = tk.Listbox(dow_window, width=72, height=18)
    file_list.pack()
    file_list.place(x=10, y=30)
    tk.Button(dow_window, text='下载', width=12, command=download).place(x=10, y=365)
    scan_file()
    dow_window.mainloop()


def upload_window():
    def get_file_path():
        fileName = filedialog.askopenfilename()
        file_path.insert('insert', fileName)
        return fileName

    def upload():
        file_Name = file_path.get()
        try:
            f = open(file_Name, 'rb')
            new_name = var_new_name.get()
            ftp.storbinary("STOR %s" % new_name, f)
            tmb.showinfo('提示', '上传成功')
        except Exception as error:
            tmb.showerror('错误', str(error))

    up_window = tk.Toplevel(window)
    up_window.title('上传')
    up_window.geometry('530x230')
    up_window.resizable(width=False, height=False)
    tk.LabelFrame(up_window, text='选择文件', width=520, height=120).place(x=5, y=15)
    file_path = tk.Entry(up_window, width=60)
    file_path.pack()
    file_path.place(x=10, y=85)
    tk.Label(up_window, text='文件路径').place(x=15, y=60)
    tk.Button(up_window, text='选择', width=10, command=get_file_path).place(x=440, y=80)
    var_new_name = tk.StringVar()
    tk.Label(up_window ,text='重命名').place(x=10, y=150)
    tk.Entry(up_window, width=15, textvariable=var_new_name).place(x=55, y=150)
    tk.Button(up_window, text='上传', width=13, command=upload).place(x=170, y=145)
    up_window.mainloop()


if __name__ == "__main__":
    # 主窗口
    ftp = FTP()
    window = tk.Tk()
    window.title("Simple FTP Client")
    window.geometry("600x520")
    window.resizable(width=False, height=False)
    # LabelFrame_server
    eth_lf = tk.LabelFrame(window, text='服务器设置', width=580, height=80).place(x=10, y=10)
    # server ip
    tk.Label(eth_lf, text='服务器位置').place(x=20, y=40)
    var_server_ip = tk.StringVar()
    server_ip = tk.Entry(eth_lf, bd=1, width=15, textvariable=var_server_ip).place(x=90, y=40)
    # username
    tk.Label(eth_lf, text='用户名').place(x=220, y=40)
    var_username = tk.StringVar()
    username = tk.Entry(eth_lf, bd=1, width=15, textvariable=var_username).place(x=268, y=40)
    # user_pass
    tk.Label(eth_lf, text='密码').place(x=395, y=40)
    var_user_pass = tk.StringVar()
    user_pass = tk.Entry(eth_lf, bd=1, width=15, textvariable=var_user_pass, show="*").place(x=430, y=40)
    # LabelFrame_2
    eth_lf_2 = tk.LabelFrame(window, text='连接信息', width=580, height=165).place(x=10, y=100)
    # connect_Text
    conn_text = tk.scrolledtext.ScrolledText(window, width=78, height=10)
    conn_text.pack()
    conn_text.place(x=17, y=120)
    # LabelFrame_3
    list_lf = tk.LabelFrame(window, text='文件目录', width=580, height=200).place(x=10, y=275)
    # scrollText
    list_text = tk.scrolledtext.ScrolledText(window, width=78, height=13)
    list_text.pack()
    list_text.place(x=16, y=293)
    # button:connect
    btn_conn = tk.Button(window, text='连接', width=12, command=server_con).place(x=40, y=480)
    btn_upload = tk.Button(window, text='上传', width=12, command=upload_window).place(x=245, y=480)
    btn_download = tk.Button(window, text='下载', width=12, command=download_window).place(x=435, y=480)
    window.mainloop()
