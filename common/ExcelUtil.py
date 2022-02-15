'''
Created on 2022-2-10

@author: Administrator
'''
import xlrd
from common import tools


class ExcelUtil(object):

    def __init__(self, file_path,sheet_name):
        self.data=xlrd.open_workbook(file_path)
        self.sheet_name=self.data.sheet_names()
        self.table=self.data.sheet_by_name(sheet_name)
        self.rowNum=self.table.nrows
        self.colNum=self.table.ncols
        self.keys=self.table.row_values(0)
    def dict_data(self):
        l=[]
        x=1        
        for i in range(self.rowNum-1):            
            d={}
            values=self.table.row_values(x)
            for j in range(self.colNum):       
               d[self.keys[j]]=values[j]
            l.append(d)
            x+=1
        
        return l
    
if __name__=="__main__":
    fname="addStoragefee_args.xlsx"
    file_path=tools.get_fpath("files",fname)
    sheet_name="value_dict"
    data=ExcelUtil(file_path,sheet_name)
    print(data.dict_data())