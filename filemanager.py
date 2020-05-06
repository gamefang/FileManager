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

    def __init__(self):
        '''
        初始化
        '''
        self.data = self.load_data()   # 加载json对象
        self.cur_folder = self.BASE_FULL_PATH   # 当前所在树状目录
        self.is_recur = False   # 文件是否递归展开
        self.filelist = self.get_file_list(self.cur_folder) # 当前筛选的文件列表（完整路径）

    def is_empty(self,data):
        '''
        检查json数据是否为空
        @param data: json第二层字典嵌套数据
        @return: bool
        '''
        for k,v in data.items():
            if any(v):  # 有任何数据即返回false
                return False
        return True # 全空返回True

    def load_data(self):
        '''
        加载json字典，并进行优化，去除空项
        @return: python字典对象
        '''
        with open(self.DATA_FILE,'r',encoding='utf8') as file:
            raw_data = json.load(file)
        data = {}
        for k,v in raw_data.items():
            if self.is_empty(v):    # 优化去除空项
                continue
            data[k] = v
        return data

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

    def get_infos(self,full_path):
        '''
        根据绝对路径获取文件的json存储额外信息
        @param full_path: 文件的绝对路径
        @return: json存储中的信息字典
        '''
        key = self.path_to_key(full_path)
        return self.data.get(key)

    def get_file_list(self,base_folder):
        '''
        获取文件路径列表
        @param base_folder: 起始的文件夹路径
        @return: 文件绝对路径的列表
        '''
        if os.path.isdir(base_folder):  # 路径错误检测
            os.chdir(base_folder)
        else:
            return f'Not a folder or not exist: {base_folder}'
        if self.is_recur:    # 递归获取
            li = []
            for root,dirs,files in os.walk(base_folder):
                for file in files:
                    fp = os.path.join(root,file)
                    li.append(fp)
            return li
        else:
            return [os.path.abspath(rel_path) for rel_path in os.listdir()]

    def filtered_file_list(self,file_list,no_folder=False,white_exts=[],black_exts=[]):
        '''
        获取过滤过的文件路径列表
        @param file_list: 文件绝对路径的列表
        @param no_folder: 移除文件夹（同时移除不存在路径）
        @param white_exts: 后缀类型的白名单（必须保留）
        @param black_exts: 后缀类型的黑名单（必不保留），黑名单优先
        @return: 按要求过滤后的文件绝对路径的列表
        '''
        li = []
        for file in file_list:
            if no_folder and os.path.isdir(file):   # 移除文件夹（同时移除不存在路径）
                continue
            ext = os.path.splitext(file)[1][1:]
            if ext in black_exts:   # 移除黑名单
                continue
            if ext not in white_exts:   #  非白名单跳过
                continue
            li.append(file)
        return li

class FileObject(object):
    '''
    文件对象
    '''
    # 加载文件管理工具对象
    FM = FileManager()
    # 文件类型通用字典
    TYPE_DICT = {
        'doc':'Word文档',
        'docx':'Word文档',
        'xls':'Excel文档',
        'xlsx':'Excel文档',
        'ppt':'PPT文档',
        'pptx':'PPT文档',
        'pdf':'PDF文档',
        'zip':'压缩包',
        'rar':'压缩包',
        'csv':'数据文件',
        'json':'数据文件',
        'dwg':'CAD图纸',
        'rvt':'BIM图纸',
    }

    def __init__(self,full_path):
        '''
        已完整路径初始化
        '''
        self.full_path = full_path
        self.isdir = os.path.isdir(full_path)

    @property
    def typ(self):
        '''
        文件类型（字符串）
        '''
        if self.isdir:
            return '文件夹'
        else:
            ext = os.path.splitext(self.full_path)[1][1:]
            return self.TYPE_DICT.get(ext,f'{ext}文件')

    @property
    def name(self):
        '''
        文件/文件夹名（字符串）
        '''
        return os.path.split(self.full_path)[1]

    @property
    def key(self):
        rel_path = os.path.relpath(self.full_path,self.FM.BASE_FULL_PATH)
        if '/' in rel_path:
            li = rel_path.split('/')
        elif '\\' in rel_path:
            li = rel_path.split('\\')
        else:
            return rel_path
        return '|'.join(li)

    # 以下涉及文件管理工具的json存储
    @property
    def saved_data(self):
        '''
        文件在管理工具中的存储数据
        '''
        return self.FM.data.get(self.key) or {}
    @property
    def tags(self):
        '''
        文件在管理工具中的标签(list)
        '''
        return self.saved_data.get('tags') or []
    @property
    def tags_str(self):
        '''
        仅用于展示的标签
        '''
        return ','.join(self.tags)
    @property
    def group(self):
        '''
        文件在管理工具中的分组数据(bool)
        '''
        return self.saved_data.get('group')

if __name__ == "__main__":
    fm = FileManager()
    raw_list = fm.get_file_list(r'E:\projects\FileManager')
    filtered_list = fm.filtered_file_list(raw_list,white_exts=['txt','doc'])
    print(filtered_list)

    fo=FileObject(r'E:\projects\FileManager\试验\测试.txt')
