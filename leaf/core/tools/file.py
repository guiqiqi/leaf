"""文件工具库"""

import os
import codecs
import mimetypes
import configparser

from typing import List, IO, NoReturn, Tuple

_DEFAULT_MIME = "application/octet-stream"


class FileTools:
    """一些文件读取常用到的工具"""

    @staticmethod
    def isfile(source: str) -> bool:
        """判断某一文件是否存在

        *source: 文件的绝对/相对路径
        """
        return os.path.isfile(source)

    @staticmethod
    def isdir(source: str) -> bool:
        """判断某一目录是否存在

        *source: 文件夹的绝对/相对目录
        """
        return os.path.isdir(source)

    @staticmethod
    def dirs(location: str) -> List[str]:
        """获取某一路径下所有文件夹

        *location : 文件夹地址
        """
        location = location.strip("\\")
        dirs = os.listdir(location)
        for name in dirs[:]:
            full = location + "/" + name
            if not os.path.isdir(full):
                dirs.remove(name)
        return dirs

    @staticmethod
    def files(location: str) -> List[str]:
        """获取某一文件夹下的所有文件

        * location : 文件夹地址
        """
        location = location.strip("\\")
        files = os.listdir(location)
        for name in files[:]:
            full = location + "/" + name
            if os.path.isdir(full):
                files.remove(name)
        return files

    @staticmethod
    def read(location: str) -> IO[str]:
        """以UTF8编码读方式打开文件"""
        handler = codecs.open(location, "r", "utf-8")
        return handler

    @staticmethod
    def write(location: str) -> IO[str]:
        """以UTF8编码写方式打开文件"""
        handler = codecs.open(location, "w", "utf-8")
        return handler

    @staticmethod
    def mimetype(location: str) -> str:
        """根据文件名获取相应的mimetype"""

        # 默认为 数据流 模式
        default = _DEFAULT_MIME
        mimetype = mimetypes.guess_type(location)[0]

        # 当给不出尝试猜测的值时
        if not mimetype:
            mimetype = default
        return mimetype

    @staticmethod
    def read_config(handler: IO[str]) -> dict:
        """读取配置文件并返回字典"""
        # 生成 config_reader 类
        config_reader = configparser.ConfigParser()
        config_reader.read_file(handler)
        sections = config_reader.sections()
        config = dict()

        # 选中对应的 section 进行添加
        for section in sections:
            options = config_reader.options(section)
            config[section] = dict()
            # 选中 option 添加
            for option in options:
                value = config_reader.get(section, option)
                config[section][option] = value

        return config

    @staticmethod
    def write_config(handler: IO[str], config: dict) -> NoReturn:
        """将制定配置写入配置文件"""

        sections = config.keys()
        config_writer = configparser.ConfigParser()

        # 选中 section
        for section in sections:
            options = config[section].keys()
            config_writer.add_section(section)
            # 选中 option
            for option in options:
                value = config[section][option]
                config_writer.set(section, option, value)

        # 写入配置
        config_writer.write(handler)

    @staticmethod
    def edit_config(handler: IO[str], change: Tuple[str, str, str]) -> NoReturn:
        """按照配置修改文件"""

        # 创建 configparser 实例
        config_editor = configparser.ConfigParser()
        config_editor.read(handler)

        section = change[0]  # 要更改的section
        option = change[1]  # 要更改的option
        value = change[2]  # 要更改的value

        # 如果没有有对应的 section 则创建一个
        if not config_editor.has_section(section):
            config_editor.add_section(section)
        config_editor.set(section, option, value)

        # 写入配置
        config_editor.write(handler)
