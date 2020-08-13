import threading
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from socket import socket, AF_INET, SOCK_DGRAM, IPPROTO_UDP

DEFAULT_MY_IP = '127.0.0.1'
DEFAULT_MY_PORT = '4555'

DEFAULT_TARGET_IP = '127.0.0.1'
DEFAULT_TARGET_PORT = '4666'


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.textbox_recv_msg = scrolledtext.ScrolledText(
            self, width=30, height=5)
        self.textbox_recv_msg.grid(row=0, column=0, padx=5, pady=5)

        ttk.Label(self, text='Local IP:').grid(
            row=0, column=1, sticky='NW', padx=5, pady=5)
        self.entry_my_ip = ttk.Entry(self, width=10)
        self.entry_my_ip.grid(row=0, column=2, sticky='NW', padx=5, pady=5)
        self.entry_my_ip.insert(0, DEFAULT_MY_IP)

        ttk.Label(self, text='Local Port:').grid(
            row=0, column=1, sticky='SW', padx=5, pady=5)
        self.entry_my_port = ttk.Entry(self, width=10)
        self.entry_my_port.grid(row=0, column=2, sticky='SW', padx=5, pady=5)
        self.entry_my_port.insert(0, DEFAULT_MY_PORT)

        ttk.Label(self, text='Target IP:').grid(
            row=0, column=3, sticky='NW', padx=5, pady=5)
        self.entry_to_ip = ttk.Entry(self, width=10)
        self.entry_to_ip.grid(row=0, column=4, sticky='NW', padx=5, pady=5)
        self.entry_to_ip.insert(0, DEFAULT_TARGET_IP)

        ttk.Label(self, text='Target Port:').grid(
            row=0, column=3, sticky='SW', padx=5, pady=5)
        self.entry_to_port = ttk.Entry(self, width=10)
        self.entry_to_port.grid(row=0, column=4, sticky='SW', padx=5, pady=5)
        self.entry_to_port.insert(0, DEFAULT_TARGET_PORT)

        self.entry_chatbox = ttk.Entry(self)
        self.entry_chatbox.grid(row=1, column=0, sticky='W', padx=5, pady=5)
        self.entry_chatbox.focus()

        button_bind = ttk.Button(
            self, text='Bind', width=10, command=self.bind)
        button_bind.grid(row=1, column=0, sticky='E', rowspan=5)

        button_send = ttk.Button(
            self, text='Send', width=10, command=self.send)
        button_send.grid(row=1, column=1, sticky='W', rowspan=5)

        button_quit = ttk.Button(
            self, text='Quit', width=10, command=self.quit)
        button_quit.grid(row=1, column=2, sticky='W', rowspan=5)

    def bind(self):
        my_addr_info = (self.entry_my_ip.get(), int(self.entry_my_port.get()))
        # AF_INET: IPv4
        # SOCK_DGRAM: UDP
        # IPPROTO_UDP: UDP - Server
        self.client_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.client_socket.bind(my_addr_info)

        self.textbox_recv_msg.insert(
            tk.END, f'已绑定{my_addr_info}, 等待接收聊天信息...\n')

        recv_thread = threading.Thread(target=self.recv)
        recv_thread.start()

    def send(self):
        str_send = self.entry_chatbox.get()
        target_ip_info = (
            self.entry_to_ip.get(),
            int(self.entry_to_port.get()))
        if str_send:
            self.client_socket.sendto(str_send.encode('utf-8'), target_ip_info)
            (my_ip, my_port) = self.client_socket.getsockname()
            my_ip_info_txt = f'{my_ip}:{my_port}'
            target_ip_info_txt = f'{target_ip_info[0]}:{target_ip_info[1]}'
            self.textbox_recv_msg.insert(tk.END, (f'我({my_ip_info_txt})向'
                                                  f'({target_ip_info_txt})'
                                                  f'发送信息: {str_send}\n'))

    def recv(self):
        while True:
            (str_recv, (target_ip, target_port)
             ) = self.client_socket.recvfrom(1024)
            str_recv = str_recv.decode('utf-8')
            target_ip_info = f'{target_ip}:{target_port}'
            if str_recv:
                self.textbox_recv_msg.insert(tk.END, (f'从({target_ip_info})'
                                                      f'接收到信息: {str_recv}\n'))

    def quit(self):
        self.client_socket.close()
        self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Easy UDP B')
    root.resizable(0, 0)

    app = Application(root)
    app.mainloop()
