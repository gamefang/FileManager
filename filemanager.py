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
    DATA_FILE = os.path.join(BASE_FULL_PATH,'filesdata.json')
    # 左、右侧UI的起始x、y值
    UI_LEFT_BASE_X = 20
    UI_RIGHT_BASE_X = 450
    UI_BASE_Y = 60
    # 默认样式
    STYLE_LABEL_FONT = ('simhei', 16)
    STYLE_BTN_FONT = ('simhei', 18)
    STYLE_CBTN_FONT = ('simhei', 16)
    STYLE_NORMAL_FONT = ('simhei', 12)

    def load_data(self):
        '''
        加载json字典
        @return: python字典对象
        '''
        with open(self.DATA_FILE,'r',encoding='utf8') as file:
            return json.load(file)

    def save_data(self,data):
        '''
        存储json字典
        @param data: python字典对象
        '''
        with open(self.DATA_FILE,'w',encoding='utf8') as file:
            json.dump(
                data,
                file,
                indent=2,   # 缩进
                ensure_ascii=False, # 不转译汉字
                )

    def path_to_key(self,full_path):
        '''
        根据绝对路径，获取与json字典对应的路径索引key
        @param full_path: 文件的绝对路径
        @return: 返回适用于json字典索引的路径，以|分隔
        '''
        rel_path = os.path.relpath(full_path,self.BASE_FULL_PATH)
        if '/' in rel_path:
            li = rel_path.split('/')
        elif '\\' in rel_path:
            li = rel_path.split('\\')
        else:
            return rel_path
        return '|'.join(li)

    def key_to_path(self,path_key):
        '''
        根据json字典的索引key，返回绝对路径
        @param path_key: 以|分隔的相对路径
        @return: 绝对路径
        '''
        rel_path = path_key.replace('|','/')
        return os.path.abspath(rel_path)
