# -*-coding: utf-8-*-

import os
import time
import threading
from tkinter import *

from filemanager import FileManager

class UIFileManager(FileManager):
    '''
    文件管理工具UI
    '''

    def __init__(self, initdir=None, filter_dic={}):
        '''
        初始化UI
        '''
        # 创建文件管理逻辑对象
        self.file_manager = FileManager()
        self.data = self.file_manager.load_data()   # 加载json对象
        # 文件过滤信息的字典
        self.filter_dic = filter_dic
        # 窗体创建
        self.wd = Tk()
        self.wd.title('文件管理工具')
        self.wd.geometry('1024x600+0+20')

        # 提示信息框
        # 字符串变量：提示信息
        self.v_tips = StringVar()
        self.v_tips.set('欢迎使用文件管理器，可使用标签管理文件')
        # 标签：提示信息
        self.lb_tips = Label(self.wd,
                           textvariable=self.v_tips,
                           bg='grey',
                           fg='white',
                           font=('simhei',14),
                           )
        self.lb_tips.place(x=20,y=10,width=984,height=40)

        ################## 左侧 ##################
        # 整数变量：当前标签页
        self.v_sheet = IntVar(0)
        # 单选按钮：标签页：标签、类型、其它
        self.rbtn_sheet_tags = Radiobutton(self.wd,
                                           text = '标签',
                                           value = 0,
                                           variable = self.v_sheet,
                                           command = self.change_sheet,
                                           bg = 'blue',
                                           font=self.STYLE_BTN_FONT,
                                           )
        self.rbtn_sheet_types = Radiobutton(self.wd,
                                            text = '类型',
                                            value = 1,
                                            variable = self.v_sheet,
                                            command = self.change_sheet,
                                            bg = 'blue',
                                            font=self.STYLE_BTN_FONT,
                                            )
        self.rbtn_sheet_cfgs = Radiobutton(self.wd,
                                           text = '设置',
                                           value = 2,
                                           variable = self.v_sheet,
                                           command = self.change_sheet,
                                           bg = 'blue',
                                           font=self.STYLE_BTN_FONT,
                                           )
        self.rbtn_sheet_tags.place(x=self.UI_LEFT_BASE_X,
                                   y=self.UI_BASE_Y,
                                   )
        self.rbtn_sheet_types.place(x=self.UI_LEFT_BASE_X + 100,
                                    y=self.UI_BASE_Y,
                                    )
        self.rbtn_sheet_cfgs.place(x=self.UI_LEFT_BASE_X + 200,
                                   y=self.UI_BASE_Y,
                                   )

        ##### 标签页：标签 #####
        # 框架：标签框架
        self.fm_tags = Frame(self.wd)
        # 滚动条：在这里是对标签提供滚动功能
        self.sb_tags = Scrollbar(self.fm_tags)
        self.sb_tags.pack(side=RIGHT, fill=Y)
        # 列表框：显示所有标签
        self.libo_tags = Listbox(self.fm_tags,
                                 yscrollcommand=self.sb_tags.set, # 接收竖直滚动条滚动
                                 font=self.STYLE_BTN_FONT,
                                 selectmode = EXTENDED,
                                 )
        # self.libo_tags.bind('<Double-1>',
        #                    self.show_by_tag,    # 鼠标双击标签，按标签排序文件
        #                    )
        self.sb_tags.config(command=self.libo_tags.yview)  # 执行竖直滚动条的滚动
        self.libo_tags.pack(side=LEFT, fill=BOTH)
        self.fm_tags.place(x=self.UI_LEFT_BASE_X,
                           y=self.UI_BASE_Y + 80,
                           )

        ##### 标签页：类型 #####

        ##### 标签页：设置 #####
        # 整数变量：是否递归展开（0-不展开，1-展开）
        self.v_is_recur = IntVar(0)
        # 复选按钮：是否递归展开
        self.cbtn_recur = Checkbutton(self.wd,
                                      text = '递归展开',
                                      variable = self.v_is_recur,
                                      command = self.toggle_recur,
                                      font = self.STYLE_CBTN_FONT,
                                      )

        ################## 右侧 ##################
        # 字符串变量：当前目录名（相对路径）
        self.v_cur_folder = StringVar(self.wd)
        # 标签：当前文件目录路径
        self.lb_cur_fp = Label(self.wd,
                               fg='purple',
                               font=('arial', 12, 'bold'),
                               )
        self.lb_cur_fp.place(x=self.UI_RIGHT_BASE_X,
                             y=self.UI_BASE_Y,
                             )

        # 按钮：向上一层
        self.btn_prev = Button(text='<',
                               command=self.go_prev,
                               activebackground='blue',
                               )
        self.btn_prev.place(x=self.UI_RIGHT_BASE_X,
                            y=self.UI_BASE_Y + 30,
                            )
        # 输入框：手动输入路径及提示框
        self.en_fp = Entry(self.wd,
                           width=66,   # 输入框宽
                           textvariable=self.v_cur_folder,    # 链接当前目录名
                           )
        self.en_fp.bind('<Return>',
                        self.update_list,   # 回车后执行update_list
                        )
        self.en_fp.place(x=self.UI_RIGHT_BASE_X + 30,
                         y=self.UI_BASE_Y + 33,
                         )

        # 框架：路径框架
        self.fm_fps = Frame(self.wd)
        # 滚动条：在这里是对列表框提供滚动功能
        self.sb_fps = Scrollbar(self.fm_fps)
        self.sb_fps.pack(side=RIGHT, fill=Y)
        # 列表框：显示路径下所有文件
        self.libo_fps = Listbox(self.fm_fps,
                                height = 20,  # 列表框高
                                width = 65,  # 列表框宽
                                yscrollcommand=self.sb_fps.set, # 接收竖直滚动条滚动
                                font=self.STYLE_NORMAL_FONT,    # 可多选 TODO 多选忽略交互
                                selectmode = EXTENDED,
                                )
        self.libo_fps.bind('<ButtonRelease-1>',
                           self.show_cur_file,    # 鼠标单击列表框任一行内容，显示当前文件信息
                           )
        self.libo_fps.bind('<Double-1>',
                           self.change_dir,    # 鼠标双击列表框任一行内容，回调change_dir
                           )
        self.sb_fps.config(command=self.libo_fps.yview)  # 执行竖直滚动条的滚动
        self.libo_fps.pack(side=LEFT, fill=BOTH)
        self.fm_fps.place(x=self.UI_RIGHT_BASE_X,
                          y=self.UI_BASE_Y + 80,
                          )

        # 按钮：打开所选文件
        self.btn_open = Button(text='打开',
                               command=self.open_file,
                               activebackground='blue',
                               font=self.STYLE_BTN_FONT,
                               )
        self.btn_open.place(x=self.UI_RIGHT_BASE_X,
                            y=self.UI_BASE_Y + 460,
                            )

        # 设定初始路径
        if initdir:
            self.v_cur_folder.set(os.curdir)
            self.update_list()

    @property
    def cur_selection(self):
        '''
        当前选定的文件路径
        '''
        selection = self.libo_fps.curselection()
        if selection:
            return self.libo_fps.get(selection)
        else:
            return os.curdir

    def msg(self,content,show_time=0):
        '''
        播放消息（错误提示等）
        @param content: 提示信息字符串（会强制转化str）
        @param show_time: 显示时间，如非0则显示一段时间后还原上一条
        '''
        old_msg = self.v_tips.get()
        self.v_tips.set(str(content))
        self.wd.update()
        if show_time:   # 还原上一条信息
            threading.Thread(target=self.delay_msg,kwargs={'content':old_msg,'show_time':show_time}).start()

    def delay_msg(self,content,show_time):
        '''
        分线程延迟信息刷新，同msg
        '''
        time.sleep(show_time)
        self.v_tips.set(str(content))
        self.wd.update()

    def change_sheet(self):
        '''
        单选按钮rbtn_sheet*的回调函数：更新sheet页UI元素
        '''
        # 隐藏所有sheet页元素
        self.fm_tags.place_forget()
        self.cbtn_recur.place_forget()
        # 展示本sheet页元素
        sheet_num = self.v_sheet.get()
        if sheet_num == 0:  # 标签页
            self.fm_tags.place(x=self.UI_LEFT_BASE_X,
                               y=self.UI_BASE_Y + 80,
                               )
        elif sheet_num == 1:    # 类型页
            pass
        elif sheet_num == 2:    # 设置页
            self.cbtn_recur.place(x=self.UI_LEFT_BASE_X,
                                  y=self.UI_BASE_Y + 40,
                                  )

    def toggle_recur(self):
        '''
        复选按钮cbtn_recur的回调函数：切换是否递归展开的选项
        '''
        if self.v_is_recur.get():   # 需要递归展开
            self.msg('修改为递归展开')
        else:
            self.msg('普通树状浏览')

    def open_file(self, ev=None):
        '''
        按钮btn_open的回调函数：打开所选文件
        '''
        os.startfile(self.cur_selection)
        print('open: ',os.path.abspath(self.cur_selection))

    def show_cur_file(self, ev=None):
        '''
        列表框libo_fps单击的回调函数：显示当前文件信息
        '''
        full_path = os.path.abspath(self.cur_selection)
        path_key = self.path_to_key(full_path)
        self.libo_tags.delete(0, END)   # 清空标签信息
        infos = self.data.get(path_key)
        if infos:
            tags = infos.get('tags')
            for tag in tags:
                self.libo_tags.insert(END, tag)
        self.msg(full_path)

    def change_dir(self, ev=None):
        '''
        列表框libo_fps双击的回调函数：变更当前路径，并切换当前目录
        '''
        self.v_cur_folder.set(self.cur_selection)
        self.update_list()
        print('path change to: ',os.path.abspath(os.curdir))

    def go_prev(self, ev=None):
        '''
        按钮btn_prev的回调函数：目录向上一层
        '''
        self.v_cur_folder.set(os.pardir)
        self.update_list()

    def update_list(self, ev=None, exts=['pdf']):
        '''
        刷新列表框内文件
        @param exts: 后缀 TODO
        '''
        error = ''
        tdir = self.v_cur_folder.get() or os.curdir
        print('tdir:',tdir)

        if not os.path.exists(tdir):    # 路径不存在
            self.msg(tdir + ': 路径不存在',show_time=3)
            if not (hasattr(self, 'last') and self.last):
                self.last = os.curdir
            self.v_cur_folder.set(self.last)  # 重新设置输入框为当前目录
            self.wd.update()
        elif not os.path.isdir(tdir):    # 路径存在且为文件，双击打开文件
            self.open_file()
        else:   # 路径存在且为文件夹，双击进入文件夹
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
            self.v_cur_folder.set(os.curdir)


if __name__ == "__main__":
    fm = UIFileManager(os.curdir,filter_dic={})
    mainloop()
