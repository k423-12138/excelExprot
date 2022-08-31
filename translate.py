

from errno import ESTALE
from importlib.metadata import files
from operator import le
import os
from pickle import TRUE
import re
import random
import json
from tkinter import W
import xlwt
import pandas as pd
#  优化 少用循环 应该用 Python中字典 提高整体 的效率 现在存在 整体效率低下 大部分的需求已经完成


def randomEvent():
    def strEvent(num=5):
        return ''.join(random.sample(['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a'], num))
    return strEvent()+strEvent(3)+str(random.randint(1, 1000))
# 写入为 json 文件


def writeInEvent(data):
    
    with open(r"E:\学习\Python\基础代码\test.txt", 'a+', encoding='utf-8') as f:
        # print('是否有数据',f.readlines())
        # f.write(data)
        f.writelines(['\n',data])
        f.close()


def xlsEvent(data,type=False):
    # 创建新的workbook（创建excel）
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet("My new Sheet")
    if(type == False):
        data = json.loads(data)
    
    num = 0
  

    for key, val in data.items():
        # # 往表格写入内容 i代表第i行，j代表第j列，
        worksheet.write(num, 0, key)
        worksheet.write(num, 1, val)
        num = num+1
    # workbook.col(0).width = 500    
    workbook.save(r"E:\学习\Python\基础代码\img\test.xls")


def RegEvent():
    regStr01 = r"'[^\x00-\xff]+'"
    regStr02 = r"//[^\r\n]*|/\*.*?\*/"
    # 正则 // /*xx*/
    regStr03 = r"/*[^\x00-\xff]+*/"

# # 创建新的sheet表
#     worksheet = workbook.add_sheet("My new Sheet")

# # 保存
#     workbook.save("新创建的表格.xls")


def RegType(str_K):
    # 正则使用判断 "" ''
    # print('文章内容',str_K)
    regStr = r"[^\x00-\xff]+"
    # 存在 '' "" 这种情况时
    regStr_01 = r"[\'|\"][^\x00-\xff]+[\'|\"]"
    # 存在 title: "这是标题", 这种情况时
    regStr_02 = r'\:\s*[\"|\'][^\x00-\xff]+[\'|\"]'
    #  keys str_content为替换文本内容
    objStr = {"arr": [], "keys": '0', 'str_intl': '0', 'str_content': ''}
    keys = randomEvent()
    objStr['keys'] = keys
    jsStr = f"intl.get('{keys}')"
    if (len(re.compile(regStr_02).findall(str_K)) > 0):
        #  因为检测出来为  : "这是标题" 这种 我只需要替换其中的中文  替换走的是第二个 正则
        objStr['str_content'] = re.sub(regStr_01, jsStr, str_K, count=1)
        
        objStr['str_intl'] ="{"+jsStr+"}"
        return objStr        
    if(len(re.compile(regStr_01).findall(str_K)) > 0):
        objStr['str_content'] = re.sub(regStr_01, "{"+jsStr+"}", str_K, count=1)
        objStr['str_intl'] = "{"+jsStr+"}"
        return objStr       
    if (len(re.compile(regStr).findall(str_K)) > 0):
        objStr['str_content'] = re.sub(regStr, "{"+jsStr+"}", str_K, count=1)
        objStr['str_intl'] = "{"+jsStr+"}"
        return objStr
 
   





def readFile(name):
    # print('当前文件路径', os.getcwd())
    regStr = r"[^\x00-\xff]+"
    regStr02 = r"//[^\r\n]*|/\*.*?\*/"
    # 正则 // /*xx*/
    files = open(r"E:\学习\Python\基础代码\test.js", encoding="utf-8")
    arrStr = files.readlines()
   
    file = open(r"E:\学习\Python\基础代码\test.js", 'w', encoding="utf-8")
    reg = re.compile(regStr)
    jsonArr = {}
    for k in arrStr:
       
        matchObj = []
       
        if(re.search(regStr02, k) == None):
            # 这段字符串中不存在 注释时 可以进行查找
            matchObj = reg.findall(k) 
            # matchObj = RegType(k)

        if(len(matchObj) > 0):
            #    print(len(matchObj),k)
            newStr = ''
            for i in matchObj:
                content = newStr if newStr else k
                # keys = randomEvent() 
                # jsonArr[keys] = i
                # jsStr = f"intl.get('{keys}')"
                # newStr = re.sub(regStr, "{"+jsStr+"}", content, count=1)
                objStr = RegType(content)
                # print('返回信息',objStr)
                jsonArr[objStr['keys']] = i
                newStr = objStr['str_content']
            file.writelines(newStr)
            newStr = ''
        else:
            file.writelines(k)

    # print(jsonArr)
    jsonArr = json.dumps(jsonArr,ensure_ascii=False,sort_keys=True)
    #  写入 json
    writeInEvent(jsonArr)
    #  写入xls 文件
    # xlsEvent(jsonArr)  
    file.close()
    files.close()
# Json 文件转化为 xls 文件 

def xlsData():
    cn ={}
    en ={}
    data=[]
    with open(r'E:\学习\Python\基础代码\json\cn.json', 'r',encoding="utf-8") as f:
            # row_data = json.load(f)
            # xlsEvent(row_data,type=True)
            cn =  json.load(f)
            f.close()
    
    with open(r'E:\学习\Python\基础代码\json\en.json', 'r',encoding="utf-8") as f:
            # row_data = json.load(f)
            # xlsEvent(row_data,type=True)
            en =  json.load(f)
            f.close()

    for k, val in cn.items():
        obj ={"keys":'',"cn":'','en':''}
        obj['keys'] = k
        obj['cn'] = cn[k]
        if(en.get(k)):
           obj['en'] = en[k]
        else:
            obj['en'] = ' '
        data.append(obj)

    xlsEvent_cn_en(data)



def xlsEvent_cn_en(data):
  
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet("前端")
    worksheet.write(0, 0, 'keys')
    worksheet.write(0, 1, '中文')
    worksheet.write(0, 2, '英文')
    for i in range(len(data)):
         worksheet.write(i+1, 0, data[i].get('keys'))
         worksheet.write(i+1, 1, data[i].get('cn'))
         worksheet.write(i+1, 2, data[i].get('en'))
    workbook.save(r"E:\学习\Python\基础代码\img\客户端翻译.xls")
xlsData()    
# test()    
# readFile('测试函数')
