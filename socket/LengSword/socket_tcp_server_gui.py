import threading
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP

DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = '4555'


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.is_listen = False
        self.can_recv = False

    def create_widgets(self):
        self.textbox_recv_msg = scrolledtext.ScrolledText(
            self, width=30, height=5)
        self.textbox_recv_msg.grid(row=0, column=0, padx=5, pady=5)

        ttk.Label(self, text='IP:').grid(
            row=0, column=1, sticky='N', padx=5, pady=5)
        self.entry_ip = ttk.Entry(self)
        self.entry_ip.grid(row=0, column=2, sticky='N', padx=5, pady=5)
        self.entry_ip.insert(0, DEFAULT_IP)

        ttk.Label(self, text='Port:').grid(
            row=0, column=1, sticky='S', padx=5, pady=5)
        self.entry_port = ttk.Entry(self)
        self.entry_port.grid(row=0, column=2, sticky='S', padx=5, pady=5)
        self.entry_port.insert(0, DEFAULT_PORT)

        self.entry_chatbox = ttk.Entry(self)
        self.entry_chatbox.grid(row=1, column=0, sticky='W', padx=5, pady=5)
        self.entry_chatbox.focus()

        button_send = ttk.Button(self, text='Send', command=self.send)
        button_send.grid(row=1, column=0, sticky='E', rowspan=5)

        button_listen = ttk.Button(self, text='Listen', command=self.listen)
        button_listen.grid(row=1, column=1, sticky='W', rowspan=5)

        button_quit = ttk.Button(self, text='Quit', command=self.quit)
        button_quit.grid(row=1, column=2, sticky='W', rowspan=5)

    def send(self):
        str_send = self.entry_chatbox.get()
        if str_send:
            self.server_socket.sendall(str_send.encode('utf-8'))
            (my_ip, my_port) = self.server_socket.getsockname()
            my_ip_info = f'{my_ip}:{my_port}'
            self.textbox_recv_msg.insert(
                tk.END, (f'我({my_ip_info})' f'发送信息: {str_send}\n')
            )

    def listen(self):
        ip_port = (self.entry_ip.get(), int(self.entry_port.get()))
        # AF_INET: IPv4
        # SOCK_STREAM: TCP
        # IPPROTO_TCP: TCP - Server
        self.socket_listener = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
        self.socket_listener.bind(ip_port)
        self.socket_listener.listen(5)
        self.is_listen = True

        self.textbox_recv_msg.insert(tk.END, '等待客户端连接中...\n')
        recv_thread = threading.Thread(target=self.recv_msg)
        recv_thread.start()

    def recv_msg(self):
        while True:
            (
                self.server_socket,
                (client_ip, client_port),
            ) = self.socket_listener.accept()
            self.can_recv = True
            client_ip_info = f'{client_ip}:{client_port}'
            self.textbox_recv_msg.insert(tk.END, f'客户端IP信息:{client_ip_info}\n')
            str_recv = self.server_socket.recv(1024).decode('utf-8')
            if str_recv == '[exit]':
                self.textbox_recv_msg.insert(
                    tk.END, (f'客户端({client_ip_info})' f'已与服务器断开连接\n')
                )
            else:
                self.textbox_recv_msg.insert(
                    tk.END, (f'客户端({client_ip_info})' f'发送信息: {str_recv}\n')
                )

    def quit(self):
        if self.is_listen:
            self.socket_listener.close()
        if self.can_recv:
            self.server_socket.close()

        self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Easy TCP Server')
    root.resizable(0, 0)

    app = Application(root)
    app.mainloop()
