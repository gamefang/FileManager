# -*-coding: utf-8-*-

import os
from time import sleep
from tkinter import *

class UIFileManager(object):
    '''
    文件管理工具UI
    '''

    def __init__(self, initdir=None, filter_dic={}):
        '''
        初始化UI
        '''
        # 文件过滤信息的字典
        self.filter_dic = filter_dic
        # 窗体创建
        self.wd = Tk()
        self.wd.title('文件管理工具')
        self.wd.geometry('1024x600+0+20')

        # 字符串变量：当前目录名
        self.cur_folder = StringVar(self.wd)
        # 标签：当前文件目录路径
        self.lb_cur_fp = Label(self.wd,
                               fg='purple',
                               font=('arial', 12, 'bold'),
                               )
        self.lb_cur_fp.place(x=450,y=5)

        # 输入框：手动输入路径及提示框
        self.en_fp = Entry(self.wd,
                           width=66,   # 输入框宽
                           textvariable=self.cur_folder,    # 链接当前目录名
                           )
        self.en_fp.bind('<Return>',
                        self.update_list,   # 回车后执行update_list
                        )
        self.en_fp.place(x=480,y=50)

        # 按钮：向上一层
        self.btn_prev = Button(text='<',
                               command=self.go_prev,
                               activebackground='blue',
                               )
        self.btn_prev.place(x=450,y=45)
        
        # 框架：路径框架
        self.fm_fps = Frame(self.wd)
        # 滚动条：在这里是对列表框提供滚动功能
        self.sb_fps = Scrollbar(self.fm_fps)
        self.sb_fps.pack(side=RIGHT, fill=Y)
        # 列表框：显示路径下所有文件
        self.libo_fps = Listbox(self.fm_fps,
                                height=20,  # 列表框高
                                width=70,  # 列表框宽
                                yscrollcommand=self.sb_fps.set, # 接收竖直滚动条滚动
                                )
        self.libo_fps.bind('<Double-1>',
                           self.change_dir,    # 鼠标双击列表框任一行内容，回调change_dir
                           )
        self.sb_fps.config(command=self.libo_fps.yview)  # 执行竖直滚动条的滚动
        self.libo_fps.pack(side=LEFT, fill=BOTH)
        self.fm_fps.place(x=450,y=100)

        # 按钮：打开所选文件
        self.btn_open = Button(text='打开',
                               command=self.open_file,
                               activebackground='blue',
                               font=('simhei', 18),
                               )
        self.btn_open.place(x=450,y=480)

        # 设定初始路径
        if initdir:
            self.cur_folder.set(os.curdir)
            self.update_list()

    @property
    def cur_selection(self):
        '''
        当前选定的文件路径
        '''
        return self.libo_fps.get(self.libo_fps.curselection()) or os.curdir

    def msg(self,content):
        '''
        播放消息（错误提示等）
        '''
        self.cur_folder.set(content)
        self.wd.update()


    def open_file(self, ev=None):
        '''
        按钮btn_open的回调函数：打开所选文件
        '''
        os.startfile(self.cur_selection)
        print('open: ',os.path.abspath(self.cur_selection))

    def change_dir(self, ev=None):
        '''
        列表框libo_fps双击的回调函数：变更当前路径，并切换当前目录
        '''
        self.cur_folder.set(self.cur_selection)
        self.update_list()
        print('path change to: ',os.path.abspath(os.curdir))

    def go_prev(self, ev=None):
        '''
        按钮btn_prev的回调函数：目录向上一层
        '''
        self.cur_folder.set(os.pardir)
        self.update_list()

    def update_list(self, ev=None, exts=['pdf']):
        '''
        刷新列表框内文件
        @param exts: 后缀 TODO
        '''
        error = ''
        tdir = self.cur_folder.get() or os.curdir
        print('tdir:',tdir)

        if not os.path.exists(tdir):    # 路径不存在
            self.msg(tdir + ': 路径不存在')
            sleep(2)
            if not (hasattr(self, 'last') and self.last):
                self.last = os.curdir
            self.cur_folder.set(self.last)  # 重新设置输入框为当前目录
            self.wd.update()
        elif not os.path.isdir(tdir):    # 路径存在且为文件，双击打开文件
            self.open_file()
        else:   # 路径存在且为文件夹，双击进入文件夹
            self.msg('更新文件列表……')
            # 确定文件
            files = os.listdir(tdir)
            files.sort()
            os.chdir(tdir)  # 将当前工作目录设置为tdir
            self.lb_cur_fp.config(text=os.getcwd())  # 配置，将第二个标签内容定为当前工作目录
            self.libo_fps.delete(0, END)  # 删除旧目录下列表框的内容
            self.libo_fps.insert(END, os.curdir)  # 在新目录列表框的最后加入当前目录
            self.libo_fps.insert(END, os.pardir)  # 在新目录列表框的最后加入当前目录的上一级目录
            for file in files:
                self.libo_fps.insert(END, file)
            self.cur_folder.set(os.curdir)


if __name__ == "__main__":
    fm = UIFileManager(os.curdir,filter_dic={})
    mainloop()
