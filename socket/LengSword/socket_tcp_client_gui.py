import threading
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from socket import socket, AF_INET, SOCK_STREAM

DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = '4555'


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.is_connect = False

    def create_widgets(self):
        self.textbox_recv_msg = scrolledtext.ScrolledText(
            self, width=30, height=5)
        self.textbox_recv_msg.grid(row=0, column=0, padx=5, pady=5)

        ttk.Label(self, text='IP:').grid(
            row=0, column=1, sticky='NW', padx=5, pady=5)
        self.entry_ip = ttk.Entry(self, width=10)
        self.entry_ip.grid(row=0, column=2, sticky='NW', padx=5, pady=5)
        self.entry_ip.insert(0, DEFAULT_IP)

        ttk.Label(self, text='Port:').grid(
            row=0, column=1, sticky='SW', padx=5, pady=5)
        self.entry_port = ttk.Entry(self, width=10)
        self.entry_port.grid(row=0, column=2, sticky='SW', padx=5, pady=5)
        self.entry_port.insert(0, DEFAULT_PORT)

        self.entry_chatbox = ttk.Entry(self)
        self.entry_chatbox.grid(row=1, column=0, sticky='W', padx=5, pady=5)
        self.entry_chatbox.focus()

        button_send = ttk.Button(
            self, text='Send', width=10, command=self.send)
        button_send.grid(row=1, column=0, sticky='E', rowspan=5)

        button_connect = ttk.Button(
            self, text='Connect', width=10, command=self.connect
        )
        button_connect.grid(row=1, column=1, sticky='W', rowspan=5)

        button_disconnect = ttk.Button(
            self, text='Disconnect', width=10, command=self.disconnect
        )
        button_disconnect.grid(row=1, column=2, sticky='W', rowspan=5)

        button_quit = ttk.Button(
            self, text='Quit', width=10, command=self.quit)
        button_quit.grid(row=1, column=3, sticky='W', rowspan=5)

    def send(self):
        str_send = self.entry_chatbox.get()
        if str_send:
            self.client_socket.send(str_send.encode('utf-8'))
            (my_ip, my_port) = self.client_socket.getsockname()
            my_ip_info = f'{my_ip}:{my_port}'
            self.textbox_recv_msg.insert(
                tk.END, (f'我({my_ip_info})' f'发送信息: {str_send}\n')
            )

    def connect(self):
        self.addr_info = (self.entry_ip.get(), int(self.entry_port.get()))
        # AF_INET: IPv4
        # SOCK_STREAM: TCP
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        thread = threading.Thread(target=self.on_connect)
        thread.start()

    def on_connect(self):
        self.client_socket.connect(self.addr_info)
        self.is_connect = True
        self.server_ip_info = f'{self.addr_info[0]}:{self.addr_info[1]}'
        self.textbox_recv_msg.insert(
            tk.END, (f'成功连接到' f'服务器({self.server_ip_info})\n'))
        recv_thread = threading.Thread(target=self.recv_msg)
        recv_thread.start()

    def recv_msg(self):
        server_ip_info = self.server_ip_info
        while True:
            str_recv = self.client_socket.recv(1024).decode('utf-8')
            if str_recv:
                self.textbox_recv_msg.insert(
                    tk.END, (f'服务器({server_ip_info})' f'发送信息: {str_recv}\n')
                )

    def disconnect(self):
        if self.is_connect:
            self.client_socket.send('[exit]'.encode('utf-8'))
            self.client_socket.close()
            self.is_connect = False

    def quit(self):
        self.disconnect()
        self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Easy TCP Client')
    root.resizable(0, 0)

    app = Application(root)
    app.mainloop()
