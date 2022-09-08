
import xlrd
from xlrd import xldate_as_tuple
import datetime
import json

class ExcelData():
    # 初始化方法
    def __init__(self, data_path, sheetname):
        # json cn 路径
        self.json_path_cn = r"E:\学习\Python\基础代码\json\cn.json"
        # 定义 json en  本地路径
        self.json_path_en = r"E:\学习\Python\基础代码\json\en.json"
        #定义一个属性接收文件路径
        self.data_path = data_path
        # 定义一个属性接收工作表名称
        self.sheetname = sheetname
        # 使用xlrd模块打开excel表读取数据
        self.data = xlrd.open_workbook(self.data_path)
        # 根据工作表的名称获取工作表中的内容（方式①）
        self.table = self.data.sheet_by_name(self.sheetname)
        # 根据工作表的索引获取工作表的内容（方式②）
        # self.table = self.data.sheet_by_name(0)
        # 获取第一行所有内容,如果括号中1就是第二行，这点跟列表索引类似
        self.keys = self.table.row_values(0)
        # 获取工作表的有效行数
        self.rowNum = self.table.nrows
        # 获取工作表的有效列数
        self.colNum = self.table.ncols
    # 定义一个读取excel表的方法
    def readExcel(self):
        # 定义一个空列表 以及 CN EN 字典
        datas = []
    
        for i in range(1, self.rowNum):
            # 定义一个空字典
            sheet_data = {}
            for j in range(self.colNum):
                # 获取单元格数据类型
                c_type = self.table.cell(i,j).ctype
                # 获取单元格数据
                c_cell = self.table.cell_value(i, j)
                if c_type == 2 and c_cell % 1 == 0:  # 如果是整形
                    c_cell = int(c_cell)
                elif c_type == 3:
                    # 转成datetime对象
                    date = datetime.datetime(*xldate_as_tuple(c_cell,0))
                    c_cell = date.strftime('%Y/%d/%m %H:%M:%S')
                elif c_type == 4:
                    c_cell = True if c_cell == 1 else False
                sheet_data[self.keys[j]] = c_cell
                # 循环每一个有效的单元格，将字段与值对应存储到字典中
                # 字典的key就是excel表中每列第一行的字段
                # sheet_data[self.keys[j]] = self.table.row_values(i)[j]
            # 再将字典追加到列表中
            datas.append(sheet_data)
        # 返回从excel中获取到的数据：以列表存字典的形式返回
        self.createJson(arr=datas)
        return datas
    def createJson(self,arr):
        # 定义一个 cn , en 字典 
        print(arr)
        cn={}
        en={}
        for k in arr:
            cn[k['key']] = k['中文']
            en[k['key']] = k['英文']
            # 写入数据
        cn = json.dumps(cn,ensure_ascii=False,sort_keys=False)
        en = json.dumps(en,ensure_ascii=False,sort_keys=False)        
        with open(self.json_path_cn, 'w', encoding='utf-8') as f:
           f.write(cn)
           f.close()
        with open(self.json_path_en, 'w', encoding='utf-8') as f:
           f.write(en)
           f.close()
        print('构建完成.....')           
        
if __name__ == "__main__":
    data_path = r"E:\学习\Python\基础代码\static\test.xls"
    sheetname = "test"
    get_data = ExcelData(data_path, sheetname)
    datas = get_data.readExcel()

