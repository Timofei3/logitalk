from customtkinter import *
from socket import *
import threading
class MyWin(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('400x300')
        self.title('')
        self.scale = 1

        self.frame = CTkFrame(self, width=0, fg_color='light blue')
        self.frame.pack_propagate(False)
        self.frame.place(x=0, y=0)
        self.btn_menu = CTkButton(self, text='▶️', command=self.click,
                                  width=30)
        self.btn_menu.place(x=0, y=0)

        self.is_show_menu = False
        self.frame_width = 0

        self.entry = CTkEntry(self, placeholder_text='Введіть повідомлення:')
        self.btn_send = CTkButton(self, text='>', width=28, command=self.send_message, fg_color="paleturquoise")
        self.messages = CTkTextbox(self, state = "disable", fg_color="paleturquoise")

        self.update_ui()
        self.username="timofei"
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('127.0.0.1', 8080))
            hello = f"{self.username} приєднався(лась) до чату!"
            self.sock.send(hello.encode())
            threading.Thread(targert=self.recv_message, daemon=True).start()
        except:
            pass
    def recv_message(self):
        while True:
            try:
                message = self.sock.recv(1024).decode()
                self.add_message(message, "left")
            except:
                pass
    def send_message(self):
        message = self.entry.get()
        self.entry.delete(0, END)
        if message:
            data = f"{self.username}: {message}"
            self.add_message(data, "right")
            try:
                self.sock.sendall(data.encode())
            except:
                pass

    def add_message(self, msg, align):
        self.messages.configure(state='normal')
        self.messages._textbox.tag_configure(align, justify=align)
        self.messages.insert(END, f"{msg}\n", align)
        self.messages.configure(state='disable')

    def update_ui(self):
        win_w = self.winfo_width() / self.scale
        win_h = self.winfo_height() / self.scale

        self.btn_send.place(x=win_w-28, y=win_h-28)
        self.entry.configure(width=win_w-28-self.frame.winfo_width()/self.scale)
        self.entry.place(x=self.frame.winfo_width()/self.scale, y=win_h-28)
        self.messages.place(x=self.frame_width)
        self.messages.configure(width=win_w - self.frame_width, height=win_h - 30)
        self.after(50, self.update_ui)

    def click(self):
        if self.is_show_menu:
            self.btn_menu.configure(text='◀️')
            self.is_show_menu = False
            self.hide_menu()
        else:
            self.btn_menu.configure(text='▶️')
            self.is_show_menu = True
            self.show_menu()

    def show_menu(self):
        if self.frame_width < 200:
            self.frame_width += 5
            self.frame.configure(width=self.frame_width,
                                 height=self.winfo_height())
        if self.is_show_menu:
            self.after(10, self.show_menu)

    def hide_menu(self):
        if self.frame_width > 0:
            self.frame_width -= 5
            self.frame.configure(width=self.frame_width,
                                 height=self.winfo_height())
        if not self.is_show_menu:
            self.after(10, self.hide_menu)


win = MyWin()
win.mainloop()