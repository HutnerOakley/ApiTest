#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-02-27 17:21
# @Name    : get_files_path.py
# @Description   : 获取文件路径以及处理文件
# @Author  : Hunter


import os
from jinja2 import Environment, FileSystemLoader

config_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'config')
output_tem_path = os.path.join(config_path, 'report_output.html')


def get_all_files(file_path, data_switch=False):
    """
    获取文件路径
    :param file_path:
    :param data_switch:
    :return:
    """
    file_name = []
    # 获取所有文件的子文件名称
    for root, dirs, files in os.walk(file_path):
        for _file_path in files:
            path = os.path.join(root, _file_path)
            if data_switch:
                if 'yaml' in path or '.yaml' in path:
                    file_name.append(path)
            else:
                file_name.append(path)
    return file_name


def del_file(path):
    """
    删除目录下的文件
    :param path:
    :return:
    """
    # 遍历目录下的所有子目录和文件
    for root, dirs, files in os.walk(path, topdown=False):
        # 删除所有文件
        for file in files:
            os.remove(os.path.join(root, file))
        # 删除所有目录
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def create_file_or_dir(path, name, is_dir=True):
    """
    在指定路径下创建文件或目录
    :param path:
    :param name:
    :param is_dir:
    :return:
    """
    new_path = os.path.join(path, name)
    if is_dir:
        os.mkdir(new_path)
    else:
        # 利用open()函数打开文件，同时会创建一个空文件
        open(new_path, 'w').close()


def replace_html(data, path=config_path, name='report_template.html'):
    """
    替换html中的占位符
    :param data: 需要替换的数据,字典格式
    :param path: 你的html模板所在的目录
    :param name: 需要操作的模板
    :return:
    """
    # 创建一个加载器，用来加载模板
    env = Environment(loader=FileSystemLoader(path))

    # 加载模板
    template = env.get_template(name)

    # 使用数据渲染模板
    html_output = template.render(data)

    # 写入文件
    # with open(output_tem_path, 'w', encoding='utf-8')as f:
    #     f.write(html_output)
    return html_output


if __name__ == '__main__':
    case_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'report', 'html', 'data', 'test-cases')
    file_name = get_all_files(case_path)
    # print(file_name)
    report_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'report')
    # print(report_path)
    # del_file(report_path)
    # create_file_or_dir(report_path, "tmp")
    data={
        "result":"123",
        "address":"456",
        "spend_time":"1231"
    }
    print(replace_html(data))