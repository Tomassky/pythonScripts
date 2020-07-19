import tkinter as tk
from tkinter import messagebox as tmb
from tkinter import scrolledtext
import poplib
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.parser import HeaderParser, Parser
from email.header import decode_header
from email.utils import parseaddr
import sys
from tkinter import filedialog

pop_ser = 'pop.126.com'
smtp_ser = 'smtp.126.com'
pop_pass = 'xxx'
user = 'xxxx'


def decode_str(s):
    (value, charset) = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


'''主窗体部分'''
def main_window():

    '''发送邮件'''
    def send_mail_box():
        def get_file_path():
            fileName = filedialog.askopenfilename() # 获取附件路径
            file_path.insert('insert', fileName)

        def send_mail():
            text = message.get('0.0', 'end')
            rec = var_to.get()
            sender = var_from.get()
            print(sender)
            msgtxt = MIMEText(text, 'plain', 'utf-8')
            send_message = MIMEMultipart()
            send_message.attach(msgtxt)
            send_message['From'] = Header(var_from.get(), 'utf-8')
            send_message['To'] = Header(var_to.get(), 'utf-8')
            send_message['Subject'] = Header(var_subject.get(), 'utf-8')
            att = MIMEText(open(file_path.get(), 'rb').read(), 'base64', 'utf-8')
            att['Content-Type'] = 'application/octet-stream'
            att['Content-Disposition'] = 'attachment; filename="附件"'
            send_message.attach(att)
            try:
                smtp_obj = smtplib.SMTP()
                smtp_obj.connect(smtp_ser, 25)
                smtp_obj.ehlo(smtp_ser)
                smtp_obj.login(user, var_pwd.get())
                smtp_obj.sendmail(sender, rec, send_message.as_string())
                print(smtp_obj)
                tmb.showinfo('通知', '发送成功！')
            except Exception as error:
                tmb.showerror('错误', error)
                print(error)

        sendBox = tk.Tk()
        sendBox.title('撰写邮件')
        sendBox.geometry('600x520')
        sendBox.resizable(width=False, height=False)
        tk.Label(sendBox, text='From').place(x=20, y=15)
        # var_from = tk.StringVar()
        var_from = tk.Entry(sendBox, bd=1, width=65)
        var_from.pack()
        var_from.place(x=60, y=15)
        tk.Label(sendBox, text='To').place(x=20, y=50)
        var_to = tk.Entry(sendBox, bd=1, width=65)
        var_to.pack()
        var_to.place(x=60, y=50)
        tk.Label(sendBox, text='Subject').place(x=12, y=85)
        var_subject = tk.Entry(sendBox, bd=1, width=65)
        var_subject.pack()
        var_subject.place(x=60, y=85)
        tk.LabelFrame(sendBox, text='正文', width=550, height=300).place(x=20, y=115)
        message = scrolledtext.ScrolledText(sendBox, width=74, height=20)
        message.pack()
        message.place(x=25, y=138)
        tk.LabelFrame(sendBox, text='附件', width=550, height=60).place(x=20, y=420)
        tk.Label(sendBox, text='路径').place(x=30, y=445)
        file_path = tk.Entry(sendBox, bd=1, width=58)
        file_path.pack()
        file_path.place(x=65, y=445)
        tk.Button(sendBox, text='选择', width=10, command=get_file_path).place(x=480, y=440)
        tk.Button(sendBox, text='发送', width=20, background='#FFCC33', command=send_mail).place(x=420, y=485)
        sendBox.mainloop()

    def set_server():

        def temp():
            pop_add = var_pop_add.get()
            smtp_add = var_smtp_add.get()
            conn(pop_add, smtp_add, var_username.get(), var_pwd.get())

        conn_window = tk.Toplevel()
        conn_window.title('邮件服务器设置')
        conn_window.geometry('350x220')
        conn_window.resizable(width=False, height=False)
        tk.Label(conn_window, text='POP3服务器').place(x=50, y=20)
        var_pop_add = tk.StringVar(value='pop.126.com')
        tk.Entry(conn_window, width=25, bd=1, textvariable=var_pop_add).place(x=50, y=50)
        tk.Label(conn_window, text='SMTP服务器').place(x=50, y=85)
        var_smtp_add = tk.StringVar(value='smtp.126.com')
        tk.Entry(conn_window, width=25, bd=1, textvariable=var_smtp_add).place(x=50, y=115)
        tk.Button(conn_window, text='确定', width=15, background='#00ff00', command=temp).place(x=80, y=160)
        conn_window.mainloop()

    def conn(pop_add, smtp_add, account, usr_pass):
        print(smtp_add)
        try:
            server = poplib.POP3_SSL(pop_add)   # 建立连接
            server.set_debuglevel(1)
            w = server.getwelcome().decode('utf8') # 获取服务器连接信息
            server_info.insert('insert', str(w) + '\n')
            server.user(account)
            server.pass_(usr_pass)
            # server.encoding = 'GB18030'
            rsp, msg_list, rsp_siz = server.list()
            print(server.getwelcome().decode('utf8'))
            server_info.insert('insert', '客户端:正在连接:' + pop_add + '\n')
            server_info.insert('insert', '账号:' + account + '\n')
            server_info.insert('insert', "服务器的响应: {0}".format(rsp) + '\n')
            server_info.insert('insert', '------------------>\n【Connected】\n\n\n')
            mail_info.insert('insert', '邮件总数：{}'.format(len(msg_list))+'\n')
            #print(type(msg))
            #return msg
        except Exception as error:
            tmb.showerror('错误', error)

    def rec_box():
        '''获取详细收件内容'''
        def mail_detail():

            def decode_str(s):
                value, charset = decode_header(s)[0]
                if charset:
                    value = value.decode(charset)
                return value

            def guess_charset(msg):
                charset = msg.get_charset()
                if charset is None:
                    content_type = msg.get('Content-Type', '').lower()
                    pos = content_type.find('charset=')
                    if pos >= 0:
                        charset = content_type[pos + 8:].strip()
                return charset
                '''解析头部'''
            def show_header(msg):
                for header in ['From', 'To', 'Subject']:
                    value = msg.get(header, '')
                    if value:
                        if header == 'Subject':
                            value = decode_str(value)
                        else:
                            (hdr, addr) = parseaddr(value)
                            name = decode_str(hdr)
                            addr = decode_str(addr)
                            value = u'%s <%s>' % (name, addr)
                    print('%s: %s' % (header, value))
                    detail.insert('insert', str(header)+'：'+str(value)+'\n')
            '''显示信件详细，进行分类判断'''
            def show_body(msg):
                if (msg.is_multipart()):
                    parts = msg.get_payload()
                    for part in parts:
                        show_body(part)
                else:
                    content_type = msg.get_content_type()
                    print('content_type=', content_type)
                    type_pre = content_type.split('/')[0]
                    if type_pre == 'text':
                        content = msg.get_payload(decode=True)
                        charset = guess_charset(msg)
                        if charset:
                            content = content.decode(charset)
                        print(content)
                        detail.insert('insert', content)
                        detail.insert('insert', '\n')
                    elif type_pre == 'image':
                        fname = msg['Content-ID'] + '.' + content_type.split('/')[1]
                        p_file = open(fname, 'wb')
                        data = msg.get_payload(decode=True)
                        p_file.write(data)
                        p_file.close()
                       # print('A picture is downloaded to', fname)
                    else:
                        fname = msg.get_filename()
                        fname = decode_str(fname)
                        att_file = open(fname, 'wb')
                        data = msg.get_payload(decode=True)
                        att_file.write(data)
                        att_file.close()
                       # print('The attachment is downloaded to ', fname)

            pop_obj = poplib.POP3_SSL(pop_ser)
            print(pop_obj.getwelcome())
            pop_obj.user(var_username.get())
            pop_obj.pass_(var_pwd.get())
            print('Messages: %s, Size: %s' % pop_obj.stat())
            (resp, mails, octets) = pop_obj.list()
            index = mail_list.get(mail_list.curselection())
            print('index=', index)
            (resp, lines, octets) = pop_obj.retr(index)
            lines_str = []
            for i in lines:
                lines_str.append(i.decode('utf-8'))
            msg_content = '\n'.join(lines_str)
            msg = Parser().parsestr(msg_content)
            show_detail_mail = tk.Toplevel()
            show_detail_mail.title('详细信息')
            show_detail_mail.geometry('500x430')
            show_detail_mail.resizable(width=False, height=False)
            detail = scrolledtext.ScrolledText(show_detail_mail, width=66, height=31)
            detail.pack()
            detail.place(x=5, y=10)
            show_header(msg)
            show_body(msg)
            show_detail_mail.mainloop()
            '''获取邮件列表'''
        def get_mail_list():
            try:
                server = poplib.POP3_SSL(pop_ser)
                server.set_debuglevel(1)
                w = server.getwelcome().decode('utf8')
                server.user(var_username.get())
                server.pass_(var_pwd.get())
                rsp, msg_list, rsp_siz = server.list() # 邮件索引
                total_mail_numbers = len(msg_list)
                print(total_mail_numbers)
                for i in range(1, total_mail_numbers+1):
                    rsp, msglines, msgsiz = server.retr(i) # 邮件具体信息
                    msg_content = b'\r\n'.join(msglines).decode('gbk')
                    msg = Parser().parsestr(text=msg_content)
                    subject = msg['Subject']
                    value, charset = decode_header(subject)[0]
                    print(msg)
                    if charset:
                        value = value.decode(charset)
                    print('邮件主题： {0}'.format(value))
                    mail_list.insert(0, '{0}'.format(value))
                    mail_list.insert(0, '主题：')
                    mail_list.insert(0, i)
                    mail_list.insert(0, '序号')
                    mail_list.insert(0, '**************************************')
            except Exception as error:
                tmb.showerror('错误', error)

        rec_window = tk.Toplevel()
        rec_window.title('收件箱')
        rec_window.geometry('550x430')
        tk.LabelFrame(rec_window, text='收件箱', width=355, height=425).place(x=195, y=4)
        rec_window.resizable(width=False, height=False)
        mail_list = tk.Listbox(rec_window, width=48, height=22)
        mail_list.pack()
        mail_list.place(x=200, y=20)
        tk.Button(rec_window, text='查看详细', width=17, background='#00ffcc',
                  command=mail_detail).place(x=30, y=15)
        tk.Button(rec_window, text='刷新列表', width=17, background='#99ccff',
                  command=get_mail_list).place(x=30, y=60)
        tk.Button(rec_window, text='删除邮件', width=17, background='#FFCC33').place(x=30, y=100)
        rec_window.mainloop()

    def end_process():
        sys.exit()

    if var_username.get() == '' or var_at.get() == '' or var_pwd.get() == '':
        tmb.showwarning('注意', '当前用户名和密码为空')
    else:
        server = poplib.POP3_SSL(pop_ser)
        root.withdraw()
        window = tk.Tk()
        window.title('简易邮件客户端')
        window.geometry('600x420')
        tk.LabelFrame(window, text='服务器消息', width=470, height=200).place(x=120, y=10)
        server_info = scrolledtext.ScrolledText(window, width=62, height=13)
        server_info.pack()
        server_info.place(x=127, y=30)
        tk.LabelFrame(window, text='收件箱信息', width=470, height=180).place(x=120, y=230)
        mail_info = scrolledtext.ScrolledText(window, width=62, height=11)
        mail_info.pack()
        mail_info.place(x=127, y=252)
        tk.Button(window, text='重置连接', width=14, foreground='#000000', background='#00ffcc',
                  command=set_server).place(x=5, y=20)
        tk.Button(window, text='发送邮件', width=14, foreground='#000000', background='#FFCC33',
                  command=send_mail_box).place(x=5, y=55)
        tk.Button(window, text='查看邮件', width=14, foreground='#000000', background='#99ccff',
                  command=rec_box).place(x=5, y=90)
        tk.Button(window, text='结束进程', width=14, foreground='#000000', background='#FF0033',
                  command=end_process).place(x=5, y=125)
        window.resizable(width=False, height=False)
        conn(pop_ser, smtp_ser, var_username.get(), var_pwd.get())
        window.mainloop()

'''主函数，登陆界面'''
if __name__ == '__main__':
    root = tk.Tk()
    root.title('LOGIN')
    root.geometry('350x210')
    root.resizable(width=False, height=False)
    tk.Label(root, text='DanMail ver 1.0', width=350, font=('Arial', 25), foreground='#ffffff', justify='center',
             background='#000000').pack()
    var_username = tk.StringVar(value='wydx_sdac')
    tk.Label(root, text='用户名').place(x=60, y=85)
    tk.Entry(root, width=10, bd=1, textvariable=var_username).place(x=115, y=85)
    tk.Label(root, text='@', font=('Arial', 12)).place(x=191, y=85)
    var_at = tk.StringVar()
    var_at.set('126.com')
    tk.Entry(root, width=8, bd=1, textvariable=var_at).place(x=213, y=85)
    tk.Label(root, text='授权码').place(x=60, y=120)
    var_pwd = tk.StringVar(value='wydx19627')
    tk.Entry(root, width=22, bd=1, textvariable=var_pwd, show='*').place(x=115, y=120)
    tk.Button(root, text='确定', width=12, foreground='#000000', background='#00ff00', command=main_window).place(x=140, y=160)
    root.mainloop()