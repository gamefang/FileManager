# -*-coding: utf-8-*-

import os
import json

class FileManager(object):
    '''
    文件管理工具逻辑
    '''
    # 常量定义
    # 工具所在基础路径
    BASE_FULL_PATH = os.path.abspath(os.curdir)
    # 信息文件相对路径
    DATA_FILE = 'filesdata.json'
    # 左、右侧UI的起始x、y值
    UI_LEFT_BASE_X = 20
    UI_RIGHT_BASE_X = 450
    UI_BASE_Y = 60
    # 默认样式
    STYLE_BTN_FONT = ('simhei', 18)
    STYLE_CBTN_FONT = ('simhei', 16)

    def load_data(self):
        '''
        加载json字典
        @return: python字典对象
        '''
        with open(self.DATA_FILE,'r',encoding='utf-8') as file:
            return json.load(file)

    def save_data(self,data):
        '''
        存储json字典
        @param data: python字典对象
        '''
        with open(self.DATA_FILE,'w',encoding='utf-8') as file:
            json.dump(data,file)

    def get_rel_path(self,full_path):
        '''
        根据绝对路径，获取相对路径
        @param full_path: 文件的绝对路径
        '''
        return os.path.relpath(full_path,self.BASE_FULL_PATH)
