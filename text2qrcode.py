# -*- encoding = utf-8 -*-
# author:parriss
import cv2
import qrcode
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showinfo, showerror
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk


class myqrcode():
    """Transform long text to QR code"""
    def __init__(self):
        """UI init"""
        self.root = tk.Tk()
        self.root.title('Transform long text to QR code——yhwasys')
        self.root.geometry('850x400+100+100')
        # add menubar
        self.menuBar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menuBar, tearoff=0)
        self.filemenu.add_command(label="open imge", command=self.open_file)
        self.filemenu.add_command(label="save qrcode", command=self.save_file)
        self.menuBar.add_cascade(label="file", menu=self.filemenu)
        self.root.config(menu=self.menuBar)
        # add widgets
        self.left_frame = tk.LabelFrame(self.root, text='input text')
        self.left_frame.place(relx=0.01, rely=0.01, relwid=0.46, relheight=0.98)
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.scrolled_text = ScrolledText(self.left_frame, width=16)
        self.scrolled_text.grid(row=0, column=0, sticky=NSEW)
        self.button_1 = ttk.Button(self.root, text='generate', width=10, command=self.create_qrcode)
        self.button_1.place(relx=0.47, rely=0.4)
        self.button_2 = ttk.Button(self.root, text='decode', width=10, command=self.decode_qrcode)
        self.button_2.place(relx=0.47, rely=0.6)
        self.right_frame = tk.LabelFrame(self.root, text='QRcode')
        self.right_frame.place(relx=0.53, rely=0.01, relwid=0.46, relheight=0.98)
        self.label = tk.Label(self.right_frame, text='[QRcode]')
        self.label.place(relx=0, rely=0, relwid=1, relheight=1)
        self.root.mainloop()
 
    def open_file(self):
        """open imgae"""
        self.qrcode_path =  askopenfilename(title = "select QRcode",  filetypes=[('Png File', '*.png'),  ('JPG File', '*.jpg')])
        qrcode_img = Image.open(self.qrcode_path)
        self.qrcode_image = ImageTk.PhotoImage(qrcode_img)
        self.label['image'] = self.qrcode_image

    def decode_qrcode(self):
        """decode QRcode"""
        qrcode_image = cv2.imread(self.qrcode_path)
        qrCodeDetector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = qrCodeDetector.detectAndDecode(qrcode_image)
        self.scrolled_text.delete('0.0','end')
        self.scrolled_text.insert(INSERT, str(data))
  
    def create_qrcode(self):
        """generate and refreshQRcode"""
        qr = qrcode.QRCode( version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=5,
                            border=2,)
        text = self.scrolled_text.get('0.0','end')
        number = len(text.strip())
        print(number)
        if number==0:
            showinfo('info', 'The number of characters that you enter is：{}\nplease enter your text!'.format(number))
        elif number>1800:
            showerror('error', 'The number of characters that you enter is：{}\nout of range，can not decode!'.format(number))
        else:
            qr.add_data(self.scrolled_text.get('0.0','end'))
            qr.make(fit=True)
            self.new_qrcode = qr.make_image(fill_color="black", back_color="white")
            self.new_qrcode_img = ImageTk.PhotoImage(self.new_qrcode)
            self.label['image'] = self.new_qrcode_img

    def save_file(self):
        """save the QR code as a picture"""
        self.save_file_name =  asksaveasfilename(title='save as', defaultextension='.png', filetypes=[('PNG File', '*.png'),  ('All File', '*.*')])
        self.new_qrcode.save(self.save_file_name)
        showinfo('info ', '{}save QR code success!'.format(self.save_file_name))

if __name__ == "__main__":
    myqrcode()
