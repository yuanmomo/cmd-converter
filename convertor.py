#!/usr/bin/env python
# encoding: utf-8


"This is a module of "

"""
@version    :   1.0
@author     :   MoMo
@license    :   Apache Licence 
@contact    :   yuanhongbin9090@gmail.com
@site       :   http://yuanmomo.net
@software   :   PyCharm
@file       :   convertor.py
@time       :   04/01/2018 12:31
"""

import sys
import os
import subprocess
import string
import javaFileTemplate as jft
import re

debug = True


class Main():
    def __init__(self):
        pass


cTypeJavaTypeMap = {
    "char": "String",
    "CHAR": "String",
    "BYTE": "byte",
    "WORD": "short",
    "SWORD": "short",
    "DWORD": "int",
    "SDWORD": "int",
    "QWORD": "long",
    "SQWORD": "long",
    "int": "int",
    "short": "short",
    "long": "long",
    "byte": "byte",
}

# config
project_name = "info"
cmd_default="CMD_NULL"
para_default="PARA_NULL"
dto_name = "%s%sServerDTO" % (project_name[0].upper(), project_name[1:]);
target_directory = "/Users/MoMo/SVN/siheyi/dwj-svr-base/src/main/java/com/shy/server/netty/common/dto/%s" % (
project_name)

cmdFileContentRE = r"const";
fileNameRE = r"struct[ \t]+[a-zA-z]+";
cmdRE = r"CMD_[A-Z_]+";
paramRE = r"PARA_[A-Z_]+";
fieldRE = r"[A-Za-z_]+[ \t]+[a-zA-Z0-9_\[\]]+[ \t]*;";


def get_clipboard_data():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    retcode = p.wait()
    data = p.stdout.read()
    return data


def set_clipboard_data(data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    p.wait()


def camel_to_underline(camel_format):
    '''
        驼峰命名格式转下划线命名格式
    '''
    underline_format = ''
    if isinstance(camel_format, str):
        for _s_ in camel_format:
            underline_format += _s_ if _s_.islower() else '_' + _s_.lower()
    return underline_format


def underline_to_camel(underline_format):
    '''
        下划线命名格式驼峰命名格式
    '''
    camel_format = ''
    if isinstance(underline_format, str):
        for _s_ in underline_format.split('_'):
            camel_format += _s_.capitalize()
    return camel_format


def converte(text):
    # filename
    fileName = re.split(r"[ \t]+", re.findall(fileNameRE, text)[0])[1];
    fileName = re.sub(r"[a-z]+_?", "", fileName, 1).strip();
    # fileName = underline_to_camel(fileName);

    # 写入到文件
    targetFile = '%s/%sCMD.java' % (target_directory, fileName);
    if os.path.exists(targetFile):
        # 文件存在则不写入
        print "文件已经存在了。。。。。"
        return;

    # cmd
    cmd = re.findall(cmdRE, text);
    if len(cmd) == 0:
        cmd = cmd_default
    else:
        cmd = cmd[0]

    # param
    param = re.findall(paramRE, text);
    if len(param) == 0:
        param = para_default
    else:
        param = param[0]


    fieldArray = re.findall(fieldRE, text);
    bodyArray = [];
    index = 0
    for field in fieldArray:

        field = field.replace(";", "").strip();

        array = re.split(r"[ \t]+", field)

        cType = string.upper(array[0])
        name = array[len(array) - 1]
        fieldName = name;

        javaType = array[0]
        if cType in cTypeJavaTypeMap:
            # 获取文件名
            javaType = cTypeJavaTypeMap.get(cType)

            if "CHAR" == cType:  # 字符串
                fieldName = name.split("[")[0]
                length = name.split("[")[1].replace("]", "")

                if re.match(r"\d+", length):  # 全是数字
                    cType = "_%s_LENGTH" % length

                else:
                    cType = length;


        if fieldName.find("[0]") >= 0 :
            fieldName = fieldName.replace("[0]","")
            javaType = javaType +"[]";
            cType = "OBJECT"

        bodyArray.append(jft.bodyTemplate % (fieldName, cType, index, javaType, fieldName))
        index += 1

    output = open(targetFile, 'w')
    output.write(jft.header % (project_name, dto_name, fileName, dto_name, fileName, cmd, param))
    for body in bodyArray:
        output.write(body)
    output.write(jft.foot)
    output.close()


def batchConverte():
    # 从剪贴板粘贴数据
    textFile = get_clipboard_data();

    # 循环处理
    constArray = re.split(cmdFileContentRE, textFile);

    for content in constArray:
        if string.find(content, "struct") >= 0:
            filtered_content = "";

            for line in content.split("\n") :
                if not line.strip().startswith("//") :
                    filtered_content += line;
            try :
                converte(filtered_content);
            except BaseException:
                print("生成出错[%s]" % filtered_content)



if __name__ == '__main__':
    batchConverte();
    pass
