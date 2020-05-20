# -*-coding: utf-8-*-

import os
import time
import threading
from tkinter import *
from tkinter import ttk

from filemanager import FileManager,FileObject,SingletonType
from timeit_deco import timeit

class UIFileManager(FileManager,metaclass=SingletonType):
    '''
    文件管理工具UI(单例)
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
        # 单选按钮：标签页
        self.rbtn_sheet_tags = Radiobutton(self.wd,
                                           text = '树状',
                                           value = 0,
                                           variable = self.v_sheet,
                                           command = self.cb_change_sheet,
                                           bg = 'blue',
                                           font=self.STYLE_BTN_FONT,
                                           )
        self.rbtn_sheet_types = Radiobutton(self.wd,
                                            text = '信息',
                                            value = 1,
                                            variable = self.v_sheet,
                                            command = self.cb_change_sheet,
                                            bg = 'blue',
                                            font=self.STYLE_BTN_FONT,
                                            )
        self.rbtn_sheet_cfgs = Radiobutton(self.wd,
                                           text = '筛选',
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

        ##### 标签页：树状 #####


        ##### 标签页：信息 #####
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
        self.libo_tags.bind('<Double-1>',
                           self.cb_shift_tag,    # 鼠标双击标签，按标签排序文件
                           )
        self.sb_tags.config(command=self.libo_tags.yview)  # 执行竖直滚动条的滚动
        self.libo_tags.pack(side=LEFT, fill=BOTH)
        # 字符串变量：当前文件标签
        self.v_cur_file_tags = StringVar()
        # 输入框：当前文件标签
        self.en_tags = Entry(self.wd,
                             width=35,   # 输入框宽
                             textvariable=self.v_cur_file_tags,
                             )
        # 按钮：标签修改
        self.btn_tags_mod = Button(text='修改',
                                   command=self.cb_modify_tags,
                                   activebackground='blue',
                                   font=self.STYLE_BTN_FONT,
                                   )
        # 按钮：保存修改
        self.btn_save_mod = Button(text='保存',
                                   command=self.cb_save_mod,
                                   activebackground='blue',
                                   font=self.STYLE_BTN_FONT,
                                   )

        ##### 标签页：筛选 #####
        # 复选按钮：是否递归展开
        self.cbtn_recur = Checkbutton(self.wd,
                                      text = '递归展开',
                                      command = self.cb_toggle_recur,
                                      font = self.STYLE_CBTN_FONT,
                                      )
        # 输入框：标签筛选规则
        # 字符串变量：当前标签筛选规则
        self.v_cur_tags = StringVar()
        self.en_tag_filter = Entry(self.wd,
                             width=35,   # 输入框宽
                             textvariable=self.v_cur_tags,
                             )
        self.en_tag_filter.bind('<Return>',
                                self.cb_do_filter,
                                )
        # 按钮：筛选
        self.btn_filter = Button(text='筛选',
                                 command=self.cb_do_filter,
                                 activebackground='blue',
                                 font=self.STYLE_BTN_FONT,
                                 )

        ################## 右侧 ##################
        # 字符串变量：当前目录名（绝对路径）
        self.v_cur_folder = StringVar()
        self.v_cur_folder.set(self.cur_folder)

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

        # 框架：表格框架
        self.fm_tv_fps = Frame(self.wd)
        # 滚动条：表格纵向滚动条
        self.sb_tv_fps = Scrollbar(self.fm_tv_fps)
        self.sb_tv_fps.pack(side=RIGHT, fill=Y)
        # 表格：主体定义
        self.tv_fps = ttk.Treeview(self.fm_tv_fps,
                                   height = 20,
                                   yscrollcommand=self.sb_tv_fps.set,   # 竖直滚动
                                   show = 'headings',   # 显示表头
                                   columns = ('fn','type','tags','fullpath'),  # 表格字段
                                   selectmode = EXTENDED,   # 支持多选
                                   )
        self.tv_fps.bind('<ButtonRelease-1>',
                         self.cb_tv_show_cur_file,    # 鼠标单击表格任一行，显示当前文件信息
                         )
        self.tv_fps.bind('<Double-1>',
                         self.cb_change_dir,    # 鼠标双击表格任一行，打开文件
                         )
        # 表格：定义列宽和对齐
        self.tv_fps.column('fn',
                           width = 150, # 字段初始宽度
                           anchor = 'w',    # 左对齐
                           )
        self.tv_fps.column('type',
                           width = 100,
                           anchor = 'center',   # 居中
                           )
        self.tv_fps.column('tags',
                           width = 150,
                           anchor = 'center',
                           )
        self.tv_fps.column('fullpath',
                           width = 150,
                           anchor = 'w',
                           )
        # 表格：定义表头
        self.tv_fps.heading('fn',text='文件名')
        self.tv_fps.heading('type',text='类型')
        self.tv_fps.heading('tags',text='标签')
        self.tv_fps.heading('fullpath',text='完整路径')

        self.sb_tv_fps.config(command=self.tv_fps.yview)  # 执行竖直滚动条的滚动
        self.tv_fps.pack(side=LEFT, fill=BOTH)
        self.fm_tv_fps.place(relx=0.45,
                             rely=0.25,
                             relwidth = 0.5,
                             relheight = 0.6,
                             )

        # 按钮：打开所选文件
        self.btn_open = Button(text='打开',
                               command=self.cb_open_file,
                               activebackground='blue',
                               font=self.STYLE_BTN_FONT,
                               )
        self.btn_open.place(x=self.UI_RIGHT_BASE_X,
                            y=self.UI_BASE_Y + 460,
                            )

        # 初始化执行
        self.tv_update_list()   # 初始化表格
        self.v_sheet.set(1) # 初始化标签页
        self.cb_change_sheet()

    ############# 内置属性 #############
    @property
    def cur_tv_data(self):
        '''
        返回当前选择的所有表格的内容元组
        '''
        result = []
        for data in self.tv_fps.selection():
            data_list = self.tv_fps.item(data,'value')
            result.append(data_list)
        return result

    @property
    def cur_single_tv_data(self):
        '''
        返回当前选择的单项表格的内容元组
        [文件名,类型,标签,完整路径]
        '''
        datas = self.cur_tv_data
        if datas:
            return datas[0]

    @property
    def cur_selected_single_tag(self):
        '''
        返回当前选择的单项标签内容
        '''
        return self.libo_tags.get(self.libo_tags.curselection())

    ############# 回调方法 #############
    def cb_change_sheet(self):
        '''
        单选按钮rbtn_sheet*的回调函数：更新sheet页UI元素
        '''
        # 隐藏所有sheet页元素
        self.fm_tags.place_forget()
        self.en_tags.place_forget()
        self.btn_tags_mod.place_forget()
        self.btn_save_mod.place_forget()
        self.cbtn_recur.place_forget()
        self.en_tag_filter.place_forget()
        self.btn_filter.place_forget()
        # 展示本sheet页元素
        sheet_num = self.v_sheet.get()
        if sheet_num == 0:  # 树状
            pass    # TODO 树状文件结构浏览
        elif sheet_num == 1:    # 信息
            # 框架：标签框架
            self.fm_tags.place(x=self.UI_LEFT_BASE_X,
                               y=self.UI_BASE_Y + 80,
                               )
            # 输入框：当前文件标签
            self.en_tags.place(x=self.UI_LEFT_BASE_X,
                               y=self.UI_BASE_Y + 350,
                               )
            # 按钮：标签修改
            self.btn_tags_mod.place(x=self.UI_LEFT_BASE_X,
                                    y=self.UI_BASE_Y + 400,
                                    )
            # 按钮：保存修改
            self.btn_save_mod.place(x=self.UI_LEFT_BASE_X + 300,
                                    y=self.UI_BASE_Y,
                                    )
        elif sheet_num == 2:    # 筛选
            # 复选按钮：是否递归展开
            self.cbtn_recur.place(x=self.UI_LEFT_BASE_X,
                                  y=self.UI_BASE_Y + 40,
                                  )
            # 输入框：标签筛选规则
            self.en_tag_filter.place(x=self.UI_LEFT_BASE_X,
                                    y=self.UI_BASE_Y + 100,
                                    )
            # 按钮：标签筛选
            self.btn_filter.place(x=self.UI_LEFT_BASE_X,
                                  y=self.UI_BASE_Y + 400,
                                  )

    def cb_toggle_recur(self):
        '''
        复选按钮cbtn_recur的回调函数：切换是否递归展开的选项
        '''
        self.is_recur = not self.is_recur
        if self.is_recur:
            self.msg('修改为递归展开')
        else:
            self.msg('只显示当前目录文件')
        self.change_dir()   # 刷新文件目录

    def cb_open_file(self, ev=None):
        '''
        按钮btn_open的回调函数：打开所选文件(多选打开第一个)
        '''
        fp = self.cur_single_tv_data[3]
        if fp:
            self.msg(self.open_file(fp),show_time=3)

    def cb_tv_show_cur_file(self, ev=None):
        '''
        表格tv_fps单击的回调函数：显示当前文件信息(多选显示第一个)
        '''
        datas = self.cur_single_tv_data
        if datas:
            full_path = os.path.abspath(datas[3])
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


    def cb_change_dir(self, ev=None):
        '''
        表格tv_fps双击的回调函数：变更当前路径，并切换当前目录
        '''
        fp = self.cur_single_tv_data[3]
        if os.path.isdir(fp):
            self.change_dir(fp)
        else:
            self.msg(self.open_file(fp),show_time=3)

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
        files = [item[3] for item in self.cur_tv_data]
        for file in files:  # 支持批量修改
            key = self.path_to_key(os.path.abspath(file))
            if key in self.data:    # 修改已有标签
                self.data[key]['tags'] = new_tags
                self.cb_tv_show_cur_file()    # 刷新文件显示
                self.msg(f'文件标签修改为：{new_tags}')
            else:   # 新增标签存储
                self.data[key] = {}
                self.data[key]['tags'] = new_tags
                self.cb_tv_show_cur_file()    # 刷新文件显示
                self.msg(f'文件新增标签：{new_tags}')

    def cb_shift_tag(self,ev=None):
        '''
        列表框libo_tags回调函数：切换标签
        '''
        cur_tag = self.cur_selected_single_tag
        if cur_tag in self.cur_tags:
            self.cur_tags.remove(cur_tag)
        else:
            self.cur_tags.append(cur_tag)
        self.msg(f'标签筛选规则：{self.cur_tags}')
        self.change_dir()   # 刷新文件目录
        self.v_cur_tags.set(','.join(self.cur_tags))    # 更新标签筛选显示

    def cb_do_filter(self, ev=None):
        '''
        按钮btn_filter回调函数：按标签执行筛选
        '''
        userinput = self.v_cur_tags.get().strip()
        if userinput:
            self.cur_tags = userinput.split(',')
            self.msg(f'标签筛选规则：{self.cur_tags}')
        else:
            self.cur_tags = []
            self.msg('清除标签筛选规则')
        self.change_dir()   # 刷新文件目录
        self.v_cur_tags.set(','.join(self.cur_tags))    # 更新标签筛选显示

    def cb_save_mod(self):
        '''
        按钮btn_save_mod的回调函数：保存所有标签修改
        '''
        self.fdata.save_data(self.data)
        self.msg('所有修改已保存！',show_time=3)

    ############# 普通方法 #############
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

    def change_dir(self,full_path=None):
        '''
        变更当前路径并刷新
        '''
        if not full_path:
            full_path = self.cur_folder
        self.v_cur_folder.set(full_path)
        self.cur_folder = full_path
        self.filelist = self.get_file_list(self.cur_folder)
        if self.is_thread_updating():
            self.msg('操作过于频繁，请稍后再试！',show_time=3)
            return
        global thread_update
        thread_update = threading.Thread(target=self.tv_update_list)
        thread_update.start()    # 多线程提升速度（TODO 部分行为需要禁止）
        # self.tv_update_list()
        print('path change to: ',full_path)
        
    @staticmethod
    def is_thread_updating():
        '''
        当前是否在执行刷新线程
        '''
        if 'thread_update' in globals():
            return thread_update.is_alive()
        return False

    def open_file(self,full_path):
        '''
        打开指定文件
        '''
        try:
            os.startfile(full_path)
        except Exception as e:
            print(e)
            if e.errno == 22:
                return '该文件在本系统内暂无打开方式'
        else:
            return f'open: {full_path}'

    @timeit
    def tv_update_list(self):
        '''
        刷新表格tv_fps内文件
        '''
        # 清空现有表格
        for data in self.tv_fps.get_children():
            self.tv_fps.delete(data)
        # 装入文件信息
        for num,file in enumerate(self.filelist):
            fo = FileObject(file)
            self.tv_fps.insert('',num,values=(fo.name,fo.typ,fo.tags_str,fo.full_path))
        self.v_cur_folder.set(self.cur_folder)

if __name__ == "__main__":
    fm = UIFileManager()
    mainloop()
