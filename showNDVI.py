from PIL import ImageTk
from tkinter import filedialog as fd
# from tkinter import *
import PIL
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from osgeo import gdal
import numpy as np
from numpy import *
import sys
import gc
import scipy.misc
from PIL import Image

from ExcelManage import *


# import os
#显示NDVI的折线图
class showresult(object):

    def __init__(self):
        #定义一些参数
        self.root = tk.Tk(screenName="select")
        self.root.title("Show NDVI")
        # 设置整个顶层GUI页面长宽可拉伸
        self.root.resizable(width=True, height=True)
        self.path = tk.StringVar()
        #开始年限
        self.staryear = tk.StringVar()  # 窗体自带的文本，新建一个值
        #结束年限
        self.endyear = tk.StringVar()
        #下拉框内容
        options = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
        self.staryear.set(options[0])
        self.endyear.set(options[9])
        # 界面布局
        tk.Label(self.root, text="选择起始年:").grid(row=0, column=0)
        # 选择年限
        start = tk.OptionMenu(self.root, self.staryear, *options, command=self.selectPath).grid(row=0,
                                                                                                column=1)  # *号有一个解包的功能
        tk.Label(self.root, text="选择终结年:").grid(row=0, column=2)

        start = tk.OptionMenu(self.root, self.endyear, *options, command=self.selectPath).grid(row=0,
                                                                                               column=3)  # *号有一个解包的功能
        tk.Button(self.root, text="绿地变化比较", command=self.showPhoto).grid(row=0, column=4)
        tk.Button(self.root, text="绿地面积变化统计", command=self.showarea).grid(row=0, column=5)
        self.root.mainloop()

    def return_code(self):
        self.root.destroy()  # 关闭窗体

    def showarea(self):
        #读入选择的开始年限和结束年限
        startyear = int(self.staryear.get())
        endyear = int(self.endyear.get())
        #显示NDVI结果
        showNDVI(startyear, endyear)

    def selectPath(self):
        print("start year is" + self.staryear.get())
        print("end year is" + self.endyear.get())

    # 重置图片（按要求缩放） 同mainprogram中一样
    def resize(self, w_box, h_box, pil_image):  # 参数是：要适应的窗口宽、高、Image.open后的图片
        w, h = pil_image.size  # 获取图像的原始大小
        f1 = 0.5 * w_box / w
        f2 = 0.5 * h_box / h
        factor = min([f1, f2])
        width = int(w * factor)
        height = int(h * factor)
        return pil_image.resize((width, height), PIL.Image.ANTIALIAS)
        # open_path为选择图片的路径

    def showPhoto(self):
        startyear = int(self.staryear.get())
        endyear = int(self.endyear.get())

        # 期望图像显示的大小
        w_box = 600
        h_box = 600
        # get the size of the image

        # 根据选择的路径显示图片
        im = []
        #读取图片
        for i in range(startyear, endyear + 1):
            col = i - startyear
            print(i)
            print(col)
            im.append(PIL.Image.open('ndvi' + i.__str__() + '.tif'))
            # 缩放图像让它保持比例，同时限制在一个矩形框范围内
            im[col] = self.resize(w_box, h_box, im[col])
            im[col] = ImageTk.PhotoImage(im[col])
            #如果图片数量大于5则画在第三行
            if col >= 5:
                tk.Label(self.root, image=im[col]).grid(row=3, column=col - 5)  # 布局控件
                tk.Label(self.root, text=i).grid(row=4, column=col - 5)
            # 前五个图片显示在界面的第一行
            else:
                tk.Label(self.root, image=im[col]).grid(row=1, column=col)  # 布局控件
                tk.Label(self.root, text=i).grid(row=2, column=col)

        self.root.mainloop()  # 显示图片


if __name__ == '__main__':
    showresult()
