#coding=utf-8
'''
Created on 2022-1-25

@author: Administrator
'''
import time

import pytest
from selenium import webdriver

from common import tools
from common.ExcelUtil import ExcelUtil
from page.page import LoginPage, TemplateListPage

arg=[{"user":"lixiuzhu","password":"1234567w"}]
@pytest.mark.parametrize("login", arg, indirect=True)
class TestClass(): 
       
    
    

    
    def test_add_storagefee(self,login):
        result=login[0]
        driver=login[1]
        if not result:
            pytest.xfail("login failed,remark xfail")
            
        loginPage=LoginPage(driver)
        loginPage.switch_lang()
        tempPage =TemplateListPage(driver)
        tempPage.open() 
        #test
        fpath=tools.get_fpath("files","addStoragefee_args.xlsx")
        value_list=ExcelUtil(fpath,"value_dict").dict_data()
#         print(value_list) 
        value_dict=value_list[0]
        tempPage.add_storagefee(value_dict)
        # tempPage.close_cur_page()
    
    
#     def test_add_expressfee(self,login):
#         result=login[0]
#         driver=login[1]
#         if not result:
#             pytest.xfail("login failed,remark xfail")
#         loginPage=LoginPage(driver)
#         loginPage.switch_lang()
#         
#         tempPage =TemplateListPage(driver)
#         tempPage.open()
#         #test
#         fpath=tools.get_fpath("files","addExpressfee_args.xlsx")
#         baseinfo_util=ExcelUtil(fpath,"baseinfo")
#         baseinfo_list=baseinfo_util.dict_data()
#         print(baseinfo_list)
#          
#         surcharge_util=ExcelUtil(fpath,"surcharge")
#         surcharge_list=surcharge_util.dict_data()
#         print(surcharge_list)
#          
#         surcharge_dict=tools.get_idkey_dict(surcharge_list)
#         print(surcharge_dict)
#          
#         baseinfo_1=baseinfo_list[0]
#         surcharge_1=surcharge_dict["0"]
#          
#         tempPage.add_expressfee(baseinfo_1,surcharge_1)
#         # tempPage.close_cur_page()
# 
# 
    def test_query(self,login):
        time.sleep(5)
        result=login[0]
        driver=login[1]
        if not result:
            pytest.xfail("login failed,remark xfail")
        loginPage=LoginPage(driver)
        time.sleep(5)
        loginPage.switch_lang()
         
        tempPage =TemplateListPage(driver)
        tempPage.open()
        #test
        query_cdt = {"templateType":(1,),"priceType":(1,),"status":(1,),"templateName":"","validTime":"2022-02-01,2022-02-28"}
        tempPage.query(**query_cdt)
        
        
if __name__=="__main__":
    pytest.main(["-s","test_templatelist.py"])














