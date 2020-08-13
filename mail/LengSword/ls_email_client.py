import os
import tkinter as tk
import poplib
import smtplib
import json

from threading import Timer
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from email.header import Header, decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import parseaddr, formataddr
from email.parser import Parser

CLIENT_TITLE = 'SMTP/POP3电子邮件客户端'
# 邮箱地址
EMAIL = ''
# 第三方客户端授权码
PASSWORD = ''
# SMTP服务器地址
SMTP_SERVER = 'smtp.126.com'
# POP3服务器地址
POP3_SERVER = 'pop.126.com'


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.is_pop3_init = False
        self.master.protocol('WM_DELETE_WINDOW', self.quit)
        self.email = tk.StringVar(value=EMAIL)
        self.password = tk.StringVar(value=PASSWORD)
        self.smtp_server_address = tk.StringVar(value=SMTP_SERVER)
        self.pop3_server_address = tk.StringVar(value=POP3_SERVER)
        self.fetched_mails = []
        self.selected_mail_subject = tk.StringVar()
        self.selected_mail_sender = tk.StringVar()
        self.selected_mail_receiver = tk.StringVar()
        self.send_mail_subject = tk.StringVar()
        self.send_mail_sender_email = tk.StringVar(value=EMAIL)
        self.send_mail_sender_name = tk.StringVar(value='我')
        self.send_mail_receiver_email = tk.StringVar()
        self.send_mail_receiver_name = tk.StringVar()
        self.send_mail_attachment = tk.StringVar()
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        tab_controller = ttk.Notebook(self)

        recv_tab = ttk.Frame(tab_controller)
        tab_controller.add(recv_tab, text='收信')

        send_tab = ttk.Frame(tab_controller)
        tab_controller.add(send_tab, text='发信')

        setting_tab = ttk.Frame(tab_controller)
        tab_controller.add(setting_tab, text='设置')

        tab_controller.pack(expand=1, fill=tk.BOTH)
        '''
        收信
        '''
        mails_box_frame = ttk.Labelframe(recv_tab, text='收件箱', padding=5)
        mails_box_frame.pack(side=tk.LEFT, expand=tk.NO, fill=tk.Y)

        columns_values = ['id', 'sender', 'subject']
        self.mails_box = ttk.Treeview(
            mails_box_frame,
            columns=columns_values,
            show='headings',
            selectmode='browse'
        )

        self.mails_box.column(columns_values[0], width=50, anchor='center')
        self.mails_box.column(columns_values[1], width=200, anchor='center')
        self.mails_box.column(columns_values[2], width=200, anchor='center')

        self.mails_box.heading(columns_values[0], text='编号')
        self.mails_box.heading(columns_values[1], text='发件人')
        self.mails_box.heading(columns_values[2], text='主题')

        vbar = ttk.Scrollbar(
            mails_box_frame, orient=tk.VERTICAL, command=self.mails_box.yview
        )
        vbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.mails_box.configure(yscrollcommand=vbar.set)
        self.mails_box.bind('<ButtonRelease-1>', self.on_mail_click)

        self.mails_box.pack(expand=tk.YES, fill=tk.Y)

        frame_mail_details = ttk.Labelframe(recv_tab, text='邮件详情', padding=5)
        frame_mail_details.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

        ttk.Label(frame_mail_details, text='主题:').grid(
            row=0, column=0, sticky='NW', padx=5, pady=5
        )
        entry_subject = ttk.Entry(
            frame_mail_details, width=40,
            textvariable=self.selected_mail_subject
        )
        entry_subject.grid(row=0, column=1, sticky='NW', padx=5, pady=5)

        button_delete_mail = ttk.Button(
            frame_mail_details, text='删除该邮件', width=10, command=self.delete
        )
        button_delete_mail.grid(row=0, column=1, sticky='NE', padx=5, pady=5)

        ttk.Label(frame_mail_details, text='发件人:').grid(
            row=1, column=0, sticky='NW', padx=5, pady=5
        )
        entry_sender = ttk.Entry(
            frame_mail_details, width=40,
            textvariable=self.selected_mail_sender
        )
        entry_sender.grid(row=1, column=1, sticky='SW', padx=5, pady=5)

        ttk.Label(frame_mail_details, text='收件人:').grid(
            row=2, column=0, sticky='NW', padx=5, pady=5
        )
        entry_receiver = ttk.Entry(
            frame_mail_details, width=40,
            textvariable=self.selected_mail_receiver
        )
        entry_receiver.grid(row=2, column=1, sticky='NW', padx=5, pady=5)

        ttk.Label(frame_mail_details, text='邮件正文:').grid(
            row=3, column=0, sticky='NW', padx=5, pady=5
        )
        self.textbox_mail_body = scrolledtext.ScrolledText(
            frame_mail_details, width=50, height=10
        )
        self.textbox_mail_body.grid(
            row=3, column=1, sticky='SW', padx=5, pady=5)

        ttk.Label(frame_mail_details, text='附件:').grid(
            row=4, column=0, sticky='NW', padx=5, pady=5
        )

        self.recv_attachments_listbox = tk.Listbox(
            frame_mail_details, width=40)
        self.recv_attachments_listbox.grid(
            row=4, column=1, sticky='SW', padx=5, pady=5
        )

        button_download_attachment = ttk.Button(
            frame_mail_details, text='下载', width=10,
            command=self.download_recv_attachments_item
        )
        button_download_attachment.grid(
            row=4, column=1, sticky='NE', padx=5, pady=5)

        frame_recv_logging = ttk.Labelframe(recv_tab, text='操作日志', padding=5)
        frame_recv_logging.pack(side=tk.LEFT, fill=tk.BOTH)

        self.textbox_recv_msg = scrolledtext.ScrolledText(
            frame_recv_logging, width=50, height=10
        )
        self.textbox_recv_msg.pack(side=tk.LEFT)

        # button_pop3_login = ttk.Button(
        #     recv_logging_frame, text='登录', width=10, command=self.pop3_login
        # )
        # button_pop3_login.pack()

        button_fetch = ttk.Button(
            frame_recv_logging, text='取信', width=10, command=self.fetch
        )
        button_fetch.pack()
        '''
        发信
        '''
        frame_send_mail = ttk.Labelframe(send_tab, text='编辑邮件', padding=5)
        frame_send_mail.pack(side=tk.LEFT, expand=tk.NO, fill=tk.Y)

        ttk.Label(frame_send_mail, text='主题:').grid(
            row=0, column=0, sticky='NW', padx=5, pady=5
        )
        entry_send_subject = ttk.Entry(
            frame_send_mail, width=30, textvariable=self.send_mail_subject
        )
        entry_send_subject.grid(row=0, column=1, sticky='NW', padx=5, pady=5)

        ttk.Label(frame_send_mail, text='发件人姓名:').grid(
            row=1, column=0, sticky='NW', padx=5, pady=5
        )
        entry_send_sender_name = ttk.Entry(
            frame_send_mail, width=30, textvariable=self.send_mail_sender_name
        )
        entry_send_sender_name.grid(
            row=1, column=1, sticky='SW', padx=5, pady=5)

        ttk.Label(frame_send_mail, text='发件人邮箱:').grid(
            row=2, column=0, sticky='NE', padx=5, pady=5
        )
        entry_send_sender_email = ttk.Entry(
            frame_send_mail, width=30, textvariable=self.send_mail_sender_email
        )
        entry_send_sender_email.grid(
            row=2, column=1, sticky='SW', padx=5, pady=5)

        ttk.Label(frame_send_mail, text='收件人姓名:').grid(
            row=3, column=0, sticky='NW', padx=5, pady=5
        )
        entry_send_receiver_name = ttk.Entry(
            frame_send_mail, width=30,
            textvariable=self.send_mail_receiver_name
        )
        entry_send_receiver_name.grid(
            row=3, column=1, sticky='NW', padx=5, pady=5)

        ttk.Label(frame_send_mail, text='收件人邮箱:').grid(
            row=4, column=0, sticky='NE', padx=5, pady=5
        )
        entry_send_receiver_email = ttk.Entry(
            frame_send_mail, width=30,
            textvariable=self.send_mail_receiver_email
        )
        entry_send_receiver_email.grid(
            row=4, column=1, sticky='NW', padx=5, pady=5)

        ttk.Label(frame_send_mail, text='邮件正文:').grid(
            row=5, column=0, sticky='NW', padx=5, pady=5
        )
        self.textbox_send_mail_body = scrolledtext.ScrolledText(
            frame_send_mail, width=50, height=10
        )
        self.textbox_send_mail_body.grid(
            row=5, column=1, sticky='SW', padx=5, pady=5)

        ttk.Label(frame_send_mail, text='附件:').grid(
            row=6, column=0, sticky='NW', padx=5, pady=5
        )
        entry_send_mail_attachment = ttk.Entry(
            frame_send_mail, width=40,
            textvariable=self.send_mail_attachment
        )
        entry_send_mail_attachment.grid(
            row=6, column=1, sticky='SW', padx=5, pady=5)

        button_select_attachment = ttk.Button(
            frame_send_mail, text='浏览...', width=10,
            command=self.select_send_mail_attachment
        )
        button_select_attachment.grid(
            row=6, column=1, sticky='SE', padx=5, pady=5)

        self.send_attachments_listbox = tk.Listbox(frame_send_mail, width=40)
        self.send_attachments_listbox.grid(
            row=7, column=1, sticky='SW', padx=5, pady=5
        )

        button_add_attachment = ttk.Button(
            frame_send_mail, text='添加', width=10,
            command=self.add_send_attachments_item
        )
        button_add_attachment.grid(
            row=7, column=1, sticky='NE', padx=5, pady=5)

        button_delete_attachment = ttk.Button(
            frame_send_mail, text='删除', width=10,
            command=self.delete_attachments_listbox_item
        )
        button_delete_attachment.grid(
            row=7, column=1, sticky='NE', padx=5, pady=40)

        frame_send_logging = ttk.Labelframe(send_tab, text='操作日志', padding=5)
        frame_send_logging.pack(side=tk.RIGHT, expand=tk.YES, anchor=tk.N)

        self.textbox_send_msg = scrolledtext.ScrolledText(
            frame_send_logging, width=50, height=10
        )
        self.textbox_send_msg.pack(side=tk.LEFT)

        # button_smtp_login = ttk.Button(
        #     frame_send_logging, text='登录', width=10, command=self.smtp_login
        # )
        # button_smtp_login.pack()

        button_send = ttk.Button(
            frame_send_logging, text='发信', width=10, command=self.send
        )
        button_send.pack()
        '''
        设置
        '''
        ttk.Label(setting_tab, text='SMTP服务器:').grid(
            row=0, column=0, sticky='NW', padx=5, pady=5
        )
        entry_smtp_address = ttk.Entry(
            setting_tab, width=20, textvariable=self.smtp_server_address
        )
        entry_smtp_address.grid(row=0, column=1, sticky='NW', padx=5, pady=5)

        ttk.Label(setting_tab, text='POP3服务器:').grid(
            row=1, column=0, sticky='NW', padx=5, pady=5
        )
        entry_pop3_address = ttk.Entry(
            setting_tab, width=20, textvariable=self.pop3_server_address
        )
        entry_pop3_address.grid(row=1, column=1, sticky='SW', padx=5, pady=5)

        ttk.Label(setting_tab, text='电子邮箱:').grid(
            row=2, column=0, sticky='W', padx=5, pady=5
        )
        entry_email = ttk.Entry(setting_tab, width=20, textvariable=self.email)
        entry_email.grid(row=2, column=1, sticky='W', padx=5, pady=5)

        ttk.Label(setting_tab, text='授权密码:').grid(
            row=3, column=0, sticky='SW', padx=5, pady=5
        )
        entry_password = ttk.Entry(
            setting_tab, width=20, textvariable=self.password, show='*'
        )
        entry_password.grid(row=3, column=1, sticky='SW', padx=5, pady=5)

        self.autoload()
        self.autosave_timer = Timer(5.0, self.autosave)
        self.autosave_timer.start()

    def on_mail_click(self, event):
        if not self.mails_box.selection():
            return
        selected_mail = self.mails_box.selection()[0]
        self.selected_item_id = int(
            self.mails_box.item(selected_mail, 'values')[0]
        )
        selected_mail = self.fetched_mails[self.selected_item_id - 1]
        # Header
        self.selected_mail_subject.set(selected_mail['Subject'])
        self.selected_mail_sender.set(selected_mail['From'])
        self.selected_mail_receiver.set(selected_mail['To'])
        # Body
        selected_mail_body = selected_mail['Body']
        self.textbox_mail_body.delete('1.0', tk.END)
        self.textbox_mail_body.insert(tk.END, selected_mail_body)
        # Attachments
        self.selected_mail_attachments = selected_mail['Attachments']
        self.recv_attachments_listbox.delete(0, tk.END)
        if self.selected_mail_attachments:
            for attachment_filename, _ in self.selected_mail_attachments:
                self.recv_attachments_listbox.insert(
                    tk.END, attachment_filename
                )

    def clear_mails_box(self):
        for item in self.mails_box.get_children():
            self.mails_box.delete(item)

    def select_send_mail_attachment(self):
        attachment_filename = filedialog.askopenfilename()
        if attachment_filename:
            self.send_mail_attachment.set(attachment_filename)

    def add_send_attachments_item(self):
        attachment_filename = self.send_mail_attachment.get()
        if not os.path.exists(attachment_filename):
            messagebox.showerror('错误', '不存在该文件')
            return

        self.send_mail_attachment.set('')
        self.send_attachments_listbox.insert(tk.END, attachment_filename)

    def delete_attachments_listbox_item(self):
        curselection_index = self.send_attachments_listbox.curselection()
        self.send_attachments_listbox.delete(curselection_index)

    def download_recv_attachments_item(self):
        if not self.recv_attachments_listbox.curselection():
            return

        curselection_index = self.recv_attachments_listbox.curselection()[0]
        filename, content = self.selected_mail_attachments[curselection_index]
        _, fileext = os.path.splitext(filename)
        attachment_filename = filedialog.asksaveasfilename(
            initialfile=filename,
            filetypes=[('Files', fileext),
                       ('All Files', '.*')]
        )
        with open(attachment_filename, 'wb') as f:
            f.write(content)

    def _format_email_header(self, header):
        name, addr = parseaddr(header)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def pop3_login(self):
        # Connect
        self.pop3_server = poplib.POP3_SSL(self.pop3_server_address.get())
        self.pop3_server.set_debuglevel(1)
        self.textbox_recv_msg.insert(
            tk.END, '{}\n'.format(
                self.pop3_server.getwelcome().decode('utf-8')
            )
        )
        # Login
        self.pop3_server.user(self.email.get())
        self.pop3_server.pass_(self.password.get())

        self.textbox_recv_msg.delete('1.0', tk.END)
        self.textbox_recv_msg.insert(
            tk.END,
            'Total mail(s): {0[0]} [{0[1]} byte(s)]\n'.format(
                self.pop3_server.stat()),
        )

        response, self.mails, octets = self.pop3_server.list()

    def smtp_login(self):
        # Connect
        self.smtp_server = smtplib.SMTP_SSL(self.smtp_server_address.get())
        self.smtp_server.set_debuglevel(1)
        self.smtp_server.ehlo(self.smtp_server_address.get())
        # Login
        status_code, _ = self.smtp_server.login(
            self.email.get(), self.password.get()
        )

        self.textbox_send_msg.delete('1.0', tk.END)
        self.textbox_send_msg.insert(tk.END, '{}-登录成功\n'.format(status_code))

    def send(self):
        self.smtp_login()

        msg = MIMEMultipart()
        msg['Subject'] = self.send_mail_subject.get()
        msg['From'] = self._format_email_header(
            '{} <{}>'.format(
                self.send_mail_sender_name.get(),
                self.send_mail_sender_email.get()
            )
        )
        msg['To'] = self._format_email_header(
            '{} <{}>'.format(
                self.send_mail_receiver_name.get(),
                self.send_mail_receiver_email.get()
            )
        )
        # 正文
        send_mail_content = self.textbox_send_mail_body.get('0.0', tk.END)
        msg_text = MIMEText(send_mail_content, 'plain', 'utf-8')
        msg.attach(msg_text)

        # 附件
        attachments = self.send_attachments_listbox.get(0, tk.END)
        if attachments:
            for attachment in attachments:
                attachment_data = None
                with open(attachment, 'rb') as f:
                    attachment_data = f.read()

                msg_attachment = MIMEApplication(attachment_data)
                msg_attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(attachment)
                )
                msg.attach(msg_attachment)

        try:
            self.smtp_server.sendmail(
                self.email.get(),
                self.send_mail_receiver_email.get(),
                msg.as_string()
            )
        except Exception as e:
            raise e
        else:
            self.textbox_send_msg.insert(tk.END, '发送成功\n')

    def _guess_charset(self, msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                next_pos = pos + 8
                charset = content_type[next_pos:].strip()
        return charset

    def _decode_header(self, encoded_str):
        decoded_str, charset = decode_header(encoded_str)[0]
        if charset:
            decoded_str = decoded_str.decode(charset)
        return decoded_str

    def fetch(self):
        self.fetched_mails = []
        self.clear_mails_box()

        self.pop3_login()
        mails_count = len(self.mails)
        for i in range(1, mails_count + 1):
            response, lines, octets = self.pop3_server.retr(i)

            raw_msg = b'\r\n'.join(lines).decode('utf-8')
            parsed_msg = Parser().parsestr(raw_msg)
            # Decode Header
            final_headers = {}
            for header in ['From', 'To', 'Subject']:
                header_content = parsed_msg.get(header, '')
                if header_content:
                    if header == 'Subject':
                        header_content = self._decode_header(header_content)
                    else:
                        name, addr = parseaddr(header_content)
                        name = self._decode_header(name)
                        header_content = '{} <{}>'.format(name, addr)

                final_headers[header] = header_content

            self.textbox_recv_msg.insert(tk.END, '=================\n')
            self.textbox_recv_msg.insert(
                tk.END, '主题: {}\n'.format(final_headers['Subject'])
            )
            self.textbox_recv_msg.insert(
                tk.END, '发件人: {}\n'.format(final_headers['From'])
            )
            self.textbox_recv_msg.insert(
                tk.END, '收件人: {}\n'.format(final_headers['To'])
            )

            body = []
            attachments = []

            if parsed_msg.is_multipart():
                for payload in parsed_msg.get_payload():
                    content = payload.get_payload(decode=True)
                    if payload.get_content_disposition() == 'attachment':
                        attachments.append((payload.get_filename(), content))
                    else:
                        body.append(content)

                final_body = list(
                    map(lambda bytes: bytes.decode('utf-8'), body)
                )[0]
            else:
                content_type = parsed_msg.get_content_type()
                if content_type == 'text/plain' or content_type == 'text/html':
                    final_body = parsed_msg.get_payload(decode=True)
                    charset = self._guess_charset(parsed_msg)
                    if charset:
                        final_body = final_body.decode(charset)

            self.textbox_recv_msg.insert(
                tk.END, '邮件正文:\n{}\n'.format(final_body)
            )
            print('主题: ', final_headers['Subject'])
            print('发件人: ', final_headers['From'])
            print('收件人: ', final_headers['To'])
            print('邮件正文: ', final_body)

            self.mails_box.insert(
                '',
                'end',
                values=[i, final_headers['From'], final_headers['Subject']]
            )

            self.fetched_mails.append(
                {
                    'Subject': final_headers['Subject'],
                    'From': final_headers['From'],
                    'To': final_headers['To'],
                    'Body': final_body,
                    'Attachments': attachments,
                },
            )

    def delete(self):
        self.pop3_server.dele(self.selected_item_id)
        self.pop3_login()
        self.fetch()

    def autosave(self):
        send_content_json = {
            'subject': self.send_mail_subject.get(),
            'sender_mail': self.send_mail_sender_email.get(),
            'sender_name': self.send_mail_sender_name.get(),
            'receiver_mail': self.send_mail_receiver_email.get(),
            'receiver_name': self.send_mail_receiver_name.get(),
            # Remove the redundant line break
            'body': self.textbox_send_mail_body.get('0.0', tk.END)[:-1],
        }
        with open('autosaving.json', 'wb') as config:
            data = json.dumps(send_content_json, ensure_ascii=False)
            config.write(data.encode('utf-8'))

        print('Auto saving success!')
        self.autosave_timer = Timer(10.0, self.autosave)
        self.autosave_timer.start()

    def autoload(self):
        if os.path.exists('autosaving.json'):
            with open('autosaving.json', 'rb') as config:
                data = json.loads(config.read(), encoding='utf-8')
            self.send_mail_subject.set(data['subject'])
            self.send_mail_sender_email.set(data['sender_mail'])
            self.send_mail_sender_name.set(data['sender_name'])
            self.send_mail_receiver_email.set(data['receiver_mail'])
            self.send_mail_receiver_name.set(data['receiver_name'])
            self.textbox_send_mail_body.delete('1.0', tk.END)
            self.textbox_send_mail_body.insert(tk.END, data['body'])

    def quit(self):
        # if hasattr(self, 'pop3_server'):
        #     self.pop3_server.quit()
        # if hasattr(self, 'smtp_server'):
        #     self.smtp_server.quit()
        self.autosave_timer.cancel()
        self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.title(CLIENT_TITLE)
    root.resizable(0, 0)

    app = Application(root)
    app.mainloop()
