# @Time : 2022/7/23 12:02 
# @Author : cyq
# @File : myExcel.py 
# @Software: PyCharm
# @Desc: 处理excel
import re
from typing import AnyStr, List, Dict

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from App import create_app
from Models.CaseModel.cases import Cases


class MyExcel:

    def __init__(self, file_path: AnyStr, sheetName: AnyStr = None):
        self.file_path = file_path
        self.wb = load_workbook(self.file_path)
        self.sheetName = sheetName

    def save(self, **kwargs):
        """
        遍历sheet 读取info
        :return:
        """
        if self.sheetName:
            return self.sheetReader(self.wb[self.sheetName], **kwargs)
        else:
            return [self.sheetReader(sheet, **kwargs) for sheet in self.sheets]

    def sheetReader(self, sheet: Worksheet, **kwargs):
        """
        [{title:xx,desc:xx,prd:xx,case_level:xx,status:xx,steps:"steps": [{step:1,do:xx,exp:xx}..]
        :param sheet:
        :return:
        """
        MAX_ROW = sheet.max_row
        MIN_ROW = sheet.min_row
        MIN_COL = sheet.min_column
        MAX_COL = sheet.max_column
        with create_app().app_context():
            for j in range(MIN_ROW + 1, MAX_ROW + 1):  # 第二行开始
                d = {'part': None, 'title': None, 'desc': None, 'prd': None, 'case_level': None, 'status': None,
                     'steps': [], "exp": None, "platform": None}
                body = [sheet.cell(j, i).value for i in range(MIN_COL, MAX_COL + 1)]
                case = dict(zip(d, body))
                case['steps'] = self.__steps(case.get("steps"), case.get("exp"))
                case['productID'] = kwargs.get("productID")
                case['versionID'] = kwargs.get("versionID")
                case['creator'] = kwargs.get('creator')
                case.pop("exp")
                Cases(**case).save()

    def __steps(self, steps: AnyStr, exp: AnyStr) -> List[Dict]:
        """
        :param steps: {1.xxx,2.xxx,3.xxx}
        :param exp: {1.xxx,2.xxx,3.xxx}
        :return:[{step:1,do:xxx,exp:xxx},{}]
        """
        _steps = []
        _st = steps.split("\n")
        _ex = exp.split("\n")
        for i in range(len(_st)):
            d = ["step", "do", "exp"]
            s = re.findall(r'(\d).(.*)', _st[i])[0]  # ("1","xx")
            r = re.findall(r'(\d).(.*)', _ex[i])[0]
            z = dict(zip(d, [int(s[0].strip()), s[1].strip()] + [r[1].strip()]))
            _steps.append(z)

        return _steps

    @property
    def sheets(self) -> List[Worksheet]:
        """
        获取所有sheet
        :return: List[<Worksheet>,<Worksheet>]
        """
        return self.wb.worksheets


if __name__ == '__main__':
    filepath = "../resource/case.xlsx"
    my = MyExcel(filepath)
    for i in my.save():
        print(i)
