# -*- encoding = utf-8 -*-
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
    """文字转二维码"""
    def __init__(self):
        """UI初始化"""
        self.root = tk.Tk()
        self.root.title('文字、二维码互转——yhwasys')
        self.root.geometry('850x400+100+100')
        # 添加菜单
        self.menuBar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menuBar, tearoff=0)
        self.filemenu.add_command(label="打开", command=self.open_file)
        self.filemenu.add_command(label="保存", command=self.save_file)
        self.menuBar.add_cascade(label="文件", menu=self.filemenu)
        self.root.config(menu=self.menuBar)
        # 添加控件
        self.left_frame = tk.LabelFrame(self.root, text='请输入文字')
        self.left_frame.place(relx=0.01, rely=0.01, relwid=0.46, relheight=0.98)
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.scrolled_text = ScrolledText(self.left_frame, width=16)
        self.scrolled_text.grid(row=0, column=0, sticky=NSEW)
        self.button_1 = ttk.Button(self.root, text='生成', width=10, command=self.create_qrcode)
        self.button_1.place(relx=0.47, rely=0.4)
        self.button_2 = ttk.Button(self.root, text='解析', width=10, command=self.decode_qrcode)
        self.button_2.place(relx=0.47, rely=0.6)
        self.right_frame = tk.LabelFrame(self.root, text='二维码')
        self.right_frame.place(relx=0.53, rely=0.01, relwid=0.46, relheight=0.98)
        self.label = tk.Label(self.right_frame, text='[二维码]')
        self.label.place(relx=0, rely=0, relwid=1, relheight=1)
        self.root.mainloop()
 
    def open_file(self):
        """打开图片"""
        self.qrcode_path =  askopenfilename(title = "请选择要解析的二维码",  filetypes=[('Png File', '*.png'),  ('JPG File', '*.jpg')])
        qrcode = Image.open(self.qrcode_path)
        self.qrcode_image = ImageTk.PhotoImage(qrcode)
        self.label['image'] = self.qrcode_image

    def decode_qrcode(self):
        """解码二维码"""
        qrcode_image = cv2.imread(self.qrcode_path)
        qrCodeDetector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = qrCodeDetector.detectAndDecode(qrcode_image)
        self.scrolled_text.delete('0.0','end')
        self.scrolled_text.insert(INSERT, str(data))
  
    def create_qrcode(self):
        """创建并刷新二维码"""
        qr = qrcode.QRCode( version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=5,
                            border=2,)
        text = self.scrolled_text.get('0.0','end')
        number = len(text.strip())
        print(number)
        if number==0:
            showinfo('提示', '你输入的字符个数为：{}\n请在左侧输入文字!'.format(number))
        elif number>1800:
            showerror('错误', '你输入的字符个数为：{}\n输入的文字太多，无法转为二维码!'.format(number))
        else:
            qr.add_data(self.scrolled_text.get('0.0','end'))
            qr.make(fit=True)
            self.new_qrcode = qr.make_image(fill_color="black", back_color="white")
            self.new_qrcode_img = ImageTk.PhotoImage(self.new_qrcode)
            self.label['image'] = self.new_qrcode_img

    def save_file(self):
        """保存二维码"""
        self.save_file_name =  asksaveasfilename(title='另存为', defaultextension='.png', filetypes=[('PNG File', '*.png'),  ('All File', '*.*')])
        self.new_qrcode.save(self.save_file_name)
        showinfo('提示', '{}保存成功'.format(self.save_file_name))

if __name__ == "__main__":
    myqrcode()
