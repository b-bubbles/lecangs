#coding=UTF-8
'''
Created on 2022-2-14

@author: Administrator
'''
import time

import pytest
from selenium import webdriver

from page.page import LoginPage


@pytest.fixture("module")
def login(request):
    user=request.param["user"]
    password=request.param["password"]
#     user="lixiuzhu"
#     password="1234567w"
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(chrome_options=option)
    
    driver.maximize_window()
    login=LoginPage(driver)
    login.open()
    time.sleep(1)
    account = login.login(user,password)
    flag=(account.text == user,'Login failed')
    return (flag,driver)


@pytest.fixture("module")
def myfixture(request):
#     user=request.param["user"]
#     password=request.param["password"]
#     print("myfixture,user=%s,password=%s"%(user,password))
#     return (user,password)
    return request

        
