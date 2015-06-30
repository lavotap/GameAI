#!/usr/bin/env python
#-*-coding:utf-8-*-

import re

class Number(object):
    # 验证是否为数字
    @classmethod
    def is_number(cls,number):
        is_num=re.compile('^[+|-]?[0-9]+[.]?[0-9]*')
        if is_num.match(str(number)):
            return True
        else:
            return False

    def __init__(self,number):
        if Number.is_number(number):
            self.num=number
        else:
            exit("ERROR:<__init__@Number>:Is not a number.\n")

    # 格式化输出浮点数
    def format(self):
        is_zero=re.compile('^[+|-]?[0-9]+[.]?[1-9]*')
        num_string=(is_zero.match(str(self.num))).group()
        if num_string[-1]=='.':
            num_string=num_string[0:-1]
        return num_string

    def __str__(self):
        return("%s"%self.format())
