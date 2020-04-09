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

    def __init__(self):
        '''
        初始化UI
        '''
        # 继承文件管理逻辑对象
        super(UIFileManager,self).__init__()

        ################## UI初始化 ##################
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
                                           command = self.cb_change_sheet,
                                           bg = 'blue',
                                           font=self.STYLE_BTN_FONT,
                                           )
        self.rbtn_sheet_types = Radiobutton(self.wd,
                                            text = '类型',
                                            value = 1,
                                            variable = self.v_sheet,
                                            command = self.cb_change_sheet,
                                            bg = 'blue',
                                            font=self.STYLE_BTN_FONT,
                                            )
        self.rbtn_sheet_cfgs = Radiobutton(self.wd,
                                           text = '设置',
                                           value = 2,
                                           variable = self.v_sheet,
                                           command = self.cb_change_sheet,
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
        # 按钮：保存修改
        self.btn_save_mod = Button(text='保存',
                                   command=self.cb_save_mod,
                                   activebackground='blue',
                                   font=self.STYLE_BTN_FONT,
                                   )
        self.btn_save_mod.place(x=self.UI_LEFT_BASE_X + 300,
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

        # 字符串变量：当前文件标签
        self.v_cur_file_tags = StringVar()
        # 输入框：当前文件标签
        self.en_tags = Entry(self.wd,
                             width=35,   # 输入框宽
                             textvariable=self.v_cur_file_tags,
                             )
        self.en_tags.place(x=self.UI_LEFT_BASE_X,
                           y=self.UI_BASE_Y + 350,
                           )
        # 按钮：标签修改
        self.btn_tags_mod = Button(text='修改',
                                   command=self.cb_modify_tags,
                                   activebackground='blue',
                                   font=self.STYLE_BTN_FONT,
                                   )
        self.btn_tags_mod.place(x=self.UI_LEFT_BASE_X,
                                y=self.UI_BASE_Y + 400,
                                )

        ##### 标签页：类型 #####

        ##### 标签页：设置 #####
        # 整数变量：是否递归展开（0-不展开，1-展开）
        self.v_is_recur = IntVar(0)
        # 复选按钮：是否递归展开
        self.cbtn_recur = Checkbutton(self.wd,
                                      text = '递归展开',
                                      variable = self.v_is_recur,
                                      command = self.cb_toggle_recur,
                                      font = self.STYLE_CBTN_FONT,
                                      )

        ################## 右侧 ##################
        # 字符串变量：当前目录名（相对路径）
        self.v_cur_folder = StringVar()
        self.v_cur_folder.set(self.cur_folder)
        # # 标签：当前文件目录路径
        # self.lb_cur_fp = Label(self.wd,
        #                        fg='purple',
        #                        font=('arial', 12, 'bold'),
        #                        )
        # self.lb_cur_fp.place(x=self.UI_RIGHT_BASE_X,
        #                      y=self.UI_BASE_Y,
        #                      )

        # 按钮：向上一层
        self.btn_prev = Button(text='<',
                               command=self.cb_go_prev,
                               activebackground='blue',
                               )
        # self.btn_prev.bind('<BackSpace>', # 死活绑不上
        #                     self.go_prev,
        #                     )
        self.btn_prev.place(x=self.UI_RIGHT_BASE_X,
                            y=self.UI_BASE_Y + 30,
                            )
        # 输入框：手动输入路径及提示框
        self.en_fp = Entry(self.wd,
                           width=66,   # 输入框宽
                           textvariable=self.v_cur_folder,    # 链接当前目录名
                           )
        self.en_fp.bind('<Return>',
                        self.cb_input_dir,
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
                                font=self.STYLE_NORMAL_FONT,    # 可多选
                                selectmode = EXTENDED,
                                )
        self.libo_fps.bind('<ButtonRelease-1>',
                           self.cb_show_cur_file,    # 鼠标单击列表框任一行内容，显示当前文件信息
                           )
        self.libo_fps.bind('<Double-1>',
                           self.cb_change_dir,    # 鼠标双击列表框任一行内容，回调change_dir
                           )
        self.sb_fps.config(command=self.libo_fps.yview)  # 执行竖直滚动条的滚动
        self.libo_fps.pack(side=LEFT, fill=BOTH)
        self.fm_fps.place(x=self.UI_RIGHT_BASE_X,
                          y=self.UI_BASE_Y + 80,
                          )
        self.update_list()  # 文件列表初始化刷新

        # 按钮：打开所选文件
        self.btn_open = Button(text='打开',
                               command=self.cb_open_file,
                               activebackground='blue',
                               font=self.STYLE_BTN_FONT,
                               )
        self.btn_open.place(x=self.UI_RIGHT_BASE_X,
                            y=self.UI_BASE_Y + 460,
                            )

    @property
    def cur_select_files(self):
        '''
        当前选定的文件路径列表
        '''
        selections = self.libo_fps.curselection()
        return [self.libo_fps.get(item) for item in selections]

    @property
    def cur_select_single_file(self):
        '''
        返回单独的选定文件(第一个)或空(相对路径)
        '''
        if self.cur_select_files:
            return self.cur_select_files[0]

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

    def cb_change_sheet(self):
        '''
        单选按钮rbtn_sheet*的回调函数：更新sheet页UI元素
        '''
        # 隐藏所有sheet页元素
        self.fm_tags.place_forget()
        self.cbtn_recur.place_forget()
        self.btn_tags_mod.place_forget()
        self.en_tags.place_forget()
        # 展示本sheet页元素
        sheet_num = self.v_sheet.get()
        if sheet_num == 0:  # 标签页
            self.fm_tags.place(x=self.UI_LEFT_BASE_X,
                               y=self.UI_BASE_Y + 80,
                               )
            self.en_tags.place(x=self.UI_LEFT_BASE_X,
                               y=self.UI_BASE_Y + 350,
                               )
            self.btn_tags_mod.place(x=self.UI_LEFT_BASE_X,
                                    y=self.UI_BASE_Y + 400,
                                    )
        elif sheet_num == 1:    # 类型页
            pass
        elif sheet_num == 2:    # 设置页
            self.cbtn_recur.place(x=self.UI_LEFT_BASE_X,
                                  y=self.UI_BASE_Y + 40,
                                  )

    def cb_toggle_recur(self):
        '''
        复选按钮cbtn_recur的回调函数：切换是否递归展开的选项
        '''
        if self.v_is_recur.get():   # 需要递归展开
            self.msg('修改为递归展开')
        else:
            self.msg('普通树状浏览')

    def cb_open_file(self, ev=None):
        '''
        按钮btn_open的回调函数：打开所选文件(多选打开第一个)
        '''
        fn = self.cur_select_single_file
        if fn:
            os.startfile(fn)
            print('open: ',os.path.abspath(fn))

    def cb_show_cur_file(self, ev=None):
        '''
        列表框libo_fps单击的回调函数：显示当前文件信息(多选显示第一个)
        '''
        fn = self.cur_select_single_file
        if fn:
            full_path = os.path.abspath(fn)
            self.libo_tags.delete(0, END)   # 清空标签框
            infos = self.get_infos(full_path)
            if infos:
                tags = infos.get('tags')
                for tag in tags:
                    self.libo_tags.insert(END, tag) # 标签框
                self.v_cur_file_tags.set(','.join(tags))    # 标签修改区
            else:
                self.v_cur_file_tags.set('')    # 清空标签修改区
            self.msg(full_path)

    def change_dir(self,full_path):
        '''
        变更当前路径并刷新
        '''
        self.v_cur_folder.set(full_path)
        self.cur_folder = full_path
        self.filelist = self.get_file_list(self.cur_folder)
        self.update_list()
        print('path change to: ',full_path)

    def cb_change_dir(self, ev=None):
        '''
        列表框libo_fps双击的回调函数：变更当前路径，并切换当前目录
        '''
        fn = os.path.abspath(self.cur_select_single_file)
        if os.path.isdir(fn):
            self.change_dir(fn)
        else:
            os.startfile(fn)
            print('open: ',fn)

    def cb_go_prev(self, ev=None):
        '''
        按钮btn_prev的回调函数：目录向上一层
        '''
        tar_folder = os.path.abspath(os.pardir)
        if os.path.isdir(tar_folder):
            self.change_dir(tar_folder)

    def cb_input_dir(self,ev=None):
        '''
        输入框en_fp回车的回调函数：变更路径
        '''
        full_path = self.v_cur_folder.get()
        if os.path.isdir(full_path):
            self.change_dir(full_path)
        else:   # TODO 路径错误需还原
            pass

    def cb_modify_tags(self):
        '''
        按钮btn_tags_mod的回调函数：修改标签
        '''
        new_tags = self.v_cur_file_tags.get().split(',')
        new_tags = [item for item in new_tags if item]  # 去除空项
        files = self.cur_select_files
        for file in files:  # 支持批量修改
            key = self.path_to_key(os.path.abspath(file))
            if key in self.data:    # 修改已有标签
                self.data[key]['tags'] = new_tags
                self.show_cur_file()    # 刷新文件显示
                self.msg(f'文件标签修改为：{new_tags}')
            else:   # 新增标签存储
                self.data[key] = {}
                self.data[key]['tags'] = new_tags
                self.show_cur_file()    # 刷新文件显示
                self.msg(f'文件新增标签：{new_tags}')

    def cb_save_mod(self):
        '''
        按钮btn_save_mod的回调函数：保存所有标签修改
        '''
        self.save_data(self.data)
        self.msg('所有修改已保存！',show_time=3)

    def update_list(self,ev=None):
        '''
        刷新列表框内文件
        '''
        self.libo_fps.delete(0, END)    # 清空列表框
        for file in self.filelist:
            self.libo_fps.insert(END, os.path.split(file)[1])
        self.v_cur_folder.set(self.cur_folder)

    def update_list_old(self, ev=None, exts=['pdf']):
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
    fm = UIFileManager()
    mainloop()
