#coding=UTF-8
'''
Created on 2022-2-7

@author: Administrator
'''
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from common import tools
from common.ExcelUtil import ExcelUtil


class Page(object):
    login_url='https://apptest.lecangs.com'

    def __init__(self,selenium_driver,base_url=login_url):
        self.base_url=base_url
        self.driver=selenium_driver
        self.timeout=30

    def _open(self,url):
        url=self.base_url+url
        self.driver.get(url)

    def find_element(self,*loc,parentNode=None):

        self.driver.implicitly_wait(self.timeout)
        if parentNode==None:
            return self.driver.find_element(*loc)
        else:
            return parentNode.find_element(*loc)
    
    def find_elements(self,*loc,parentNode=None):

        self.driver.implicitly_wait(self.timeout)
        if parentNode==None:
            return self.driver.find_elements(*loc)
        else:
            return parentNode.find_elements(*loc)
    
    def open(self):
        self._open(self.url)
    
    def script(self,src,*args):
        return self.driver.execute_script(src,*args)
    # not user for now
    def send_keys(self,loc,value,clear_first=True,click_first=True):
        try:
            loc=getattr(self, '%s'%loc)
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
            self.find_element(*loc).send_keys(value)
        except AttributeError:
            print('%s page does not have "%s" locator'%(self,loc))


class LoginPage(Page):
    url='/'
    #location
    username_loc=(By.ID,"username")
    password_loc=(By.ID,"password") 
    submit_loc=(By.CSS_SELECTOR,"button[type='submit']")
    #notice loc
    notice_loc=(By.CSS_SELECTOR,"a.ant-notification-notice-close")
    #logout loc
    account_loc=(By.CSS_SELECTOR,"a.user-btn.ant-dropdown-trigger")
    logout_loc=(By.CSS_SELECTOR,'li[role="menuitem"][data-menu-id="logout"]')

    #action
    def open(self):
        self._open(self.url)
        
    def login(self,username,password):
        self.find_element(*self.username_loc).send_keys(username)
        self.find_element(*self.password_loc).send_keys(password)
        self.find_element(*self.submit_loc).click()
        self.find_element(*self.notice_loc).click()
        return self.find_element(*self.account_loc)
        
    
    def switch_lang(self,lang='zh-CN'):
        '''@data-menu-id=en-US or zh-CN'''
        #location
        lang_select_loc=(By.XPATH,'//div[@class="header-action"]/div[last()]/div[2]//button')
        lang_opt_loc=(By.XPATH,'//li[@role="menuitem" and @data-menu-id="%s"]' % lang)
        lang_select_isopen_loc=(By.XPATH,'//div[@class="header-action"]/div[last()]/div[2]/a')
        #action
        # lang_select=self.find_element(*lang_select_loc)
        # self.script('arguments[0].click()',lang_select)
        # self.find_element(*lang_select_loc).send_keys(Keys.SPACE)
        self.find_element(*lang_select_loc).click()
        self.find_element(*lang_opt_loc).click()
        # return self.find_element(*lang_select_isopen_loc).get_attribute("class")

    # def switch_page(self,menu_name='财务计费',side_menu_name='计费规则',page_url='/bms/quotationTemplate'):
    #     #location
    #     menu_loc=(By.XPATH,'//div[@class="header-menu"]//div[text()="%s"]'%menu_name)
    #     side_menu_loc=(By.XPATH,'//div[contains(@class,"sider")]/ul/li[div/span="%s"]'%side_menu_name)
    #     submenu_loc=(By.XPATH,'//ul/li[div/span="%s"]/ul'%side_menu_name)
    #     submenu_link_loc=(By.XPATH,'//ul/li[@role="menuitem" and @data-menu-id="%s"]'%page_url)
    #     #action
    #     self.find_element(*menu_loc).click()
    #     style=self.find_element(*submenu_loc).get_attribute('style')
    #     if style.find('height: 0px;')>=0:
    #         self.find_element(*side_menu_loc).click()
    #         time.sleep(1)
    #     self.find_element(*submenu_link_loc).click()

    def logout(self):
        self.find_element(*self.account_loc).click()
        self.find_element(*self.logout_loc).click()
    

class TemplateListPage(Page): 
    url='/bms/quotationTemplate'
    # close page
    close_icon_loc=(By.CSS_SELECTOR,'.tags-view-wrap a[aria-current] div[class*=icon_close]')
    # query
    q_templateType_select_loc=(By.CSS_SELECTOR, '#templateTypeList>div')
    q_templateType_input_loc=(By.CSS_SELECTOR,'#templateTypeList input')
    q_priceType_select_loc=(By.CSS_SELECTOR,'#priceTypeList>div')
    q_priceType_input_loc=(By.CSS_SELECTOR,'#priceTypeList input')
    q_status_select_loc=(By.CSS_SELECTOR,'#status>div')
    q_status_input_loc=(By.CSS_SELECTOR,'#status input')
    q_templateName_input_loc=(By.CSS_SELECTOR,'input[id="templateName"]')
    q_validTime_start_loc=(By.CSS_SELECTOR,'#validTime input:nth-of-type(1)')
    q_validTime_end_loc=(By.CSS_SELECTOR,'#validTime input:nth-of-type(2)' )
    q_timePanel_start_loc=(By.CSS_SELECTOR,'.ant-calendar-range-left input')
    q_timePanel_end_loc=(By.CSS_SELECTOR,'.ant-calendar-range-right input')
    q_timePanel_submit_loc=(By.CSS_SELECTOR,'.ant-calendar-footer a:last-child')
    q_query_btn_loc=(By.CSS_SELECTOR,'.query-wrapper button:nth-child(1)')

    # add express fee template
    addExpressfee_btn_loc=(By.XPATH,'//div[@class="operate-wrapper"]//a[@href="/bms/quotationTemplate/expressFees/add"]')
    templateName_text_loc=(By.CSS_SELECTOR,'input#templateName')
    priceType_select_loc=(By.CSS_SELECTOR,'div#priceType')
    priceType_input_loc=(By.CSS_SELECTOR,'div#priceType input')
    productId_select_input_loc=(By.CSS_SELECTOR,'input#productId')
    moneyUnit_select_loc=(By.CSS_SELECTOR,'div#moneyUnit')
    moneyUnit_input_loc=(By.CSS_SELECTOR,'div#moneyUnit input')
    country_select_loc=(By.CSS_SELECTOR,'div#country')
    country_input_loc=(By.CSS_SELECTOR,'div#country input')
    # --duplicate
    validTime_start_loc=q_validTime_start_loc
    validTime_end_loc=q_validTime_end_loc
    timePanel_start_loc=q_timePanel_start_loc
    timePanel_end_loc=q_timePanel_end_loc
    timePanel_submit_loc=q_timePanel_submit_loc
    
    upload_input_loc=(By.CSS_SELECTOR,'#basicFees div[class*="upload"] input')
    basicFees_rows_loc=(By.CSS_SELECTOR,'#basicFees tbody>tr')
    # relative position
    basicFees_boxs_loc=(By.CSS_SELECTOR,'.col--edit>div')
    basicFees_inputs_loc=(By.CSS_SELECTOR,'.col--edit input')
    
    addSurcharge_btn_loc=(By.CSS_SELECTOR,'#additionalSurcharge>button')
    
    surcharge_rows_loc=(By.CSS_SELECTOR,'#additionalSurcharge tbody>tr')
    # relative position
    costType_select_loc=(By.CSS_SELECTOR,'td:nth-child(1)')
    costType_input_loc=(By.CSS_SELECTOR,'td:nth-child(1) input')
    # units_text_loc=(By.CSS_SELECTOR,'td:nth-child(2) input')
    Min_int_loc=(By.CSS_SELECTOR,'td:nth-child(3) input')
    Max_int_loc=(By.CSS_SELECTOR,'td:nth-child(4) input')
    zones_select_loc=(By.CSS_SELECTOR,'td:nth-child(5) .ant-select-selector')
    zones_opt_loc=(By.CSS_SELECTOR,'td:nth-child(5) input')
    price_int_loc=(By.CSS_SELECTOR,'td:nth-child(6) input')
    # chargingUnit_text_loc=(By.CSS_SELECTOR,'td:nth-child(7) input')
    instruction_text_loc=(By.CSS_SELECTOR,'td:nth-child(8) input')
    del_btn_loc=(By.CSS_SELECTOR,'td:nth-child(9) button')
    
    save_btn_loc=(By.CSS_SELECTOR,'.submit-wrapper>button:nth-child(2)')
    effect_btn_loc=(By.CSS_SELECTOR,'.submit-wrapper>button:nth-child(3)')

    # add storage fee
    addStoragefee_btn_loc = (
    By.XPATH, '//div[@class="operate-wrapper"]//a[@href="/bms/quotationTemplate/warehousingFees/add"]')
    # --duplicate
    # templateName_text_loc = (By.CSS_SELECTOR, 'input#templateName')
    weightUnit_select_loc = (By.CSS_SELECTOR, 'div#weightUnit')
    weightUnit_input_loc = (By.CSS_SELECTOR, 'div#weightUnit input')
    # --duplicate
    # country_select_loc = (By.CSS_SELECTOR, 'div#country')
    # country_input_loc = (By.CSS_SELECTOR, 'div#country input')
    # moneyUnit_select_loc = (By.CSS_SELECTOR, 'div#moneyUnit')
    # moneyUnit_input_loc = (By.CSS_SELECTOR, 'div#moneyUnit input')
    # validTime_start_loc = q_validTime_start_loc
    # validTime_end_loc = q_validTime_end_loc
    # timePanel_start_loc = (By.CSS_SELECTOR, '.ant-calendar-range-left input')
    # timePanel_end_loc = (By.CSS_SELECTOR, '.ant-calendar-range-right input')
    # timePanel_submit_loc = (By.CSS_SELECTOR, '.ant-calendar-footer a:last-child')
    # Unload Cabinet
    unload_rows_loc=(By.CSS_SELECTOR,'form .ant-card:nth-child(1)>.ant-card-body>div:nth-child(2) tbody>tr')
    # relative position
    unloadPrice_int_loc=(By.CSS_SELECTOR,'td:nth-child(2) input')
    # outData
    addOut_btn_loc=(By.CSS_SELECTOR,'#outData>button')
    out_rows_loc=(By.CSS_SELECTOR,'#outData tbody>tr')
    # relative position
    applyScope_select_loc=(By.CSS_SELECTOR,'td:nth-child(1) .ant-select-selector')  
    applyScope_input_loc=(By.CSS_SELECTOR,'td:nth-child(1) input')  
    minWeight_int_loc=(By.CSS_SELECTOR,'td:nth-child(2) input')
    maxWeight_int_loc=(By.CSS_SELECTOR,'td:nth-child(3) input')
    outprice_int_loc=(By.CSS_SELECTOR,'td:nth-child(4) input')
    outdel_btn_loc=(By.CSS_SELECTOR,'td:nth-child(6) button')
    # inData
    inPrice_multi_loc = (By.CSS_SELECTOR, '#inData tbody>tr>td:nth-child(2) input')
    # palletData
    palletPrice_loc = (By.CSS_SELECTOR, '#palletData tbody>tr>td:nth-child(2) input')
    # labelingData
    labelingPrice_loc = (By.CSS_SELECTOR, '#labelingData tbody>tr>td:nth-child(2) input')
    # --duplicate
    # save_btn_loc = (By.CSS_SELECTOR, '.submit-wrapper>button:nth-child(2)')
    # effect_btn_loc = (By.CSS_SELECTOR, '.submit-wrapper>button:nth-child(3)')

    def open(self):
        self._open(self.url)

    def select_opt(self,select_loc,input_loc,parentNode=None,opt_index=(1,)):
        '''
        :param select_loc: (By.CSS_SELECTOR, '')
        :param input_loc: (By.CSS_SELECTOR, '')
        :param parentNode: WebElement
        :param opt_index: str or tuple,str:"1,2,3",tuple:(1,2,3)
        
        '''
        self.find_element(*select_loc,parentNode=parentNode).click()
        input_el = self.find_element(*input_loc,parentNode=parentNode)
        # print(input_el.get_attribute("aria-expanded"))
        opt_id = input_el.get_attribute("aria-owns")
        if isinstance(opt_index, str):
            opt_index=opt_index.split(",")
        for index in opt_index:
            opt_loc = (By.CSS_SELECTOR, '#%s+div .ant-select-item-option:nth-child(%s)' % (opt_id, index))
            self.find_element(*opt_loc).click()
        
        # close select list
        opt_prt_loc = (By.XPATH, '//*[@id="%s"]/../..' % opt_id)
        opt_prt = self.find_element(*opt_prt_loc)
        self.script(
            'arguments[0].setAttribute("style","min-width: 447px; width: 447px; left: 825px; top: 123px; display: none;")',
            opt_prt)

    def type_calendar(self,**kwargs):
        '''
        kwargs:{"str":"2022-01-01,2022-02-01","time_loc":(validTime_start_loc,timePanel_start_loc,timePanel_end_loc,timePanel_submit_loc)}
        ''' 
        self.find_element(*kwargs["time_loc"][0]).click()
        
        startTime_loc=kwargs["time_loc"][1]
        endTime_loc=kwargs["time_loc"][2]       
        date_start=self.find_element(*startTime_loc)
        date_end=self.find_element(*endTime_loc)
        # js="document.querySelector('%s').removeAttribute('readonly');\
        # document.querySelector('%s').removeAttribute('readonly');" %(startTime_loc[1],endTime_loc[1])
        js="arguments[0].removeAttribute('readonly');\
            arguments[1].removeAttribute('readonly');" 
        args=(date_start,date_end)    
        self.script(js,*args)
        date_scope=kwargs["str"]
        date_list=date_scope.split(",")
        print(date_list)
        print(len(date_list))
        if isinstance(date_scope, str) and len(date_list)==2:
            date_start.send_keys(date_list[0] + ' 00:00:00')
            date_end.send_keys(date_list[1] + ' 23:59:59')
            
        self.find_element(*kwargs["time_loc"][3]).click()
    #not use
    def remove_calendarComp(self):
        calendarComp_loc=(By.CSS_SELECTOR,'.ant-calendar-picker-container')
        calendarComp=self.find_element(*calendarComp_loc)
        js="arguments[0].parentNode.removeChild(arguments[0])"
        self.script(js,calendarComp)
    def close_cur_page(self):
        self.find_element(*self.close_icon_loc).click()

    def query(self,**kwargs):
        '''
        :param kwargs: {"templateType":(1,),"priceType":(1,),"status":(1,),"templateName":"","validTime":"2022-02-01,2022-02-28"}
        :return:
        '''
        cdt_list={"templateType","priceType","status","templateName","validTime"}
        if kwargs=={}:
            self.find_element(*self.q_query_btn_loc).click()
        elif set(kwargs.keys()).issubset(cdt_list):
            flag=1
            for cdt in kwargs.keys():
                if flag==0:
                    print("wrong format of value")
                    break
                if cdt=='templateType':
                    if isinstance(kwargs[cdt],(str,tuple)):
                        self.select_opt(self.q_templateType_select_loc, self.q_templateType_input_loc, opt_index=kwargs[cdt])
                    else:
                        flag=0
                elif cdt=='priceType':
                    if isinstance(kwargs[cdt], (str,tuple)):
                        self.select_opt(self.q_priceType_select_loc, self.q_priceType_input_loc,opt_index=kwargs[cdt])
                    else:
                        flag=0
                elif cdt == 'status':
                    if isinstance(kwargs[cdt], (str,tuple)):
                        self.select_opt(self.q_status_select_loc, self.q_status_input_loc,opt_index=kwargs[cdt])
                    else:
                        flag=0
                elif cdt == 'templateName':
                    if isinstance(kwargs[cdt], str):
                        self.find_element(*self.q_templateName_input_loc).send_keys(kwargs[cdt])
                    else:
                        flag=0
                elif cdt == 'validTime':
                    if isinstance(kwargs[cdt], str):
                            d={"str":kwargs[cdt],"time_loc":(self.q_validTime_start_loc,self.q_timePanel_start_loc,self.q_timePanel_end_loc,self.q_timePanel_submit_loc)}
                            self.type_calendar(**d)
                    else:
                        flag=0
                            
            else:
                self.find_element(*self.q_query_btn_loc).click()
        else:
            print("contains key that does not exist")

    
    def add_expressfee(self,baseinfo,surcharge_item,action_type="save"):
        # go to the new courier fee page
        self.find_element(*self.addExpressfee_btn_loc).click()
        time.sleep(1)
        '''
        :param: 
        baseinfo={templateName = "220210template",priceType_index = "1" or (1,),productId_index = (1,),moneyUnit_index = (1,),country_index = (1,),validTime ="2022-02-09,2022-02-28"},
        surcharge_item=[{surcharge_costType_index = (1,),surcharge_Min = 2,surcharge_Max = 3,surcharge_zone_indexs = (1,2,3),surcharge_price = 5,surcharge_instruction = "detail"}],
        action_type="save"or "effect"
        '''
        # arguments
        # action_type:save,effect
        action_type=action_type
        templateName = baseinfo["templateName"]
        # only supports single selection
        priceType_index = baseinfo["priceType_index"]
        productId_index = baseinfo["productId_index"]
        moneyUnit_index = baseinfo["moneyUnit_index"]
        country_index = baseinfo["country_index"]
        validTime = baseinfo["validTime"]
        surcharge_count = len(surcharge_item)
        # only supports single selection
        surcharge_costType_index = tools.get_key_item(surcharge_item, "surcharge_costType_index")
        surcharge_Min = tools.get_key_item(surcharge_item, "surcharge_Min")
        surcharge_Max = tools.get_key_item(surcharge_item, "surcharge_Max")
        surcharge_zone_indexs = tools.get_key_item(surcharge_item, "surcharge_zone_indexs")
        surcharge_price = tools.get_key_item(surcharge_item, "surcharge_price")
        surcharge_instruction = tools.get_key_item(surcharge_item, "surcharge_instruction")

        # complete the form
        self.find_element(*self.templateName_text_loc).send_keys(templateName)
        self.select_opt(self.priceType_select_loc, self.priceType_input_loc,opt_index=priceType_index)
        self.select_opt(self.productId_select_input_loc, self.productId_select_input_loc,opt_index=productId_index)
        self.select_opt(self.moneyUnit_select_loc, self.moneyUnit_input_loc,opt_index=moneyUnit_index)
        self.select_opt(self.country_select_loc, self.country_input_loc,opt_index=country_index)
        '''action calendar Panel'''
        d={"str":validTime,"time_loc":(self.validTime_start_loc,self.timePanel_start_loc,self.timePanel_end_loc,self.timePanel_submit_loc)}
        self.type_calendar(**d)
        '''batch edit basicFees'''
        time.sleep(1)
        express_file=tools.get_fpath("files","express.xlsx")
        print(express_file)
        self.find_element(*self.upload_input_loc).send_keys(express_file)
        '''edit basicFees''' 
#         basicFees_rows=self.find_elements(*self.basicFees_rows_loc)
#         for basicFees_row in basicFees_rows:
#             basicFees_boxs=basicFees_row.find_elements(*self.basicFees_boxs_loc)
#             basicFees_boxs[1].click()
#             basicFees_boxs[1].click()
#             basicFees_inputs=basicFees_row.find_elements(*self.basicFees_inputs_loc) 
#             for i in range(len(basicFees_inputs)):
#                 basicFees_inputs[i].send_keys(Keys.CONTROL,'a')
#                 basicFees_inputs[i].send_keys("3")    
        
             
        addSurcharge=self.find_element(*self.addSurcharge_btn_loc)
        for i in range(surcharge_count):
            addSurcharge.click()

        rows=self.find_elements(*self.surcharge_rows_loc)
        rowNum=len(rows)
        for i in range(rowNum):
            self.select_opt(self.costType_select_loc,self.costType_input_loc,parentNode=rows[i],opt_index=surcharge_costType_index[i])
            rows[i].find_element(*self.Min_int_loc).send_keys(surcharge_Min[i])
            rows[i].find_element(*self.Max_int_loc).send_keys(surcharge_Max[i])
            self.select_opt(self.zones_select_loc,self.zones_opt_loc,parentNode=rows[i],opt_index=surcharge_zone_indexs[i])
            rows[i].find_element(*self.price_int_loc).send_keys(surcharge_price[i])
            rows[i].find_element(*self.instruction_text_loc).send_keys(surcharge_instruction[i])
        # save or submit the form
#         if action_type=="save":
#             self.find_element(*self.save_btn_loc).click()
#         else:
#             self.find_element(*self.effect_btn_loc).click()

    def add_storagefee(self,value_dict,action_type="save"):
        '''
        :param:value_dict={templateName="220210出入库模板",weightUnit_index=1,country_index=1,moneyUnit_index=1,validTime="2022-02-09,2022-02-28",\
        unloadPrices="5,6,7,8,8,8,8,8,8",minWeights="5,6",maxWeights="6,7",outPrices="5,6",inPrices="5,6",palletPrice=5,labelPrice=5}
        :param:action_type="save" or "effect"
        '''
        # go to the new storage fee page
        self.find_element(*self.addStoragefee_btn_loc).click()
        time.sleep(1)
        # arguments
        action_type=action_type
        templateName=value_dict["templateName"]
        weightUnit_index=value_dict["weightUnit_index"]
        country_index=value_dict["country_index"]
        moneyUnit_index=value_dict["moneyUnit_index"]
        validTime=value_dict["validTime"]
        unloadPrices=value_dict["unloadPrices"]
        minWeights=value_dict["minWeights"]
        maxWeights=value_dict["maxWeights"]
        outPrices=value_dict["outPrices"]
        inPrices=value_dict["inPrices"]
        palletPrice=value_dict["palletPrice"]
        labelPrice=value_dict["labelPrice"]

        # complete the form
        self.find_element(*self.templateName_text_loc).send_keys(templateName)
        self.select_opt(self.weightUnit_select_loc, self.weightUnit_input_loc,opt_index=weightUnit_index)
        self.select_opt(self.country_select_loc, self.country_input_loc,opt_index=country_index)
        self.select_opt(self.moneyUnit_select_loc, self.moneyUnit_input_loc,opt_index=moneyUnit_index)

        d = {"str":validTime, "time_loc": (self.validTime_start_loc,self.timePanel_start_loc, self.timePanel_end_loc,self.timePanel_submit_loc)}
        self.type_calendar(**d)
        # unload
        unload_rows=self.find_elements(*self.unload_rows_loc)
        unloadNum=len(unload_rows)
        unloadPrices=unloadPrices.split(",")
        for i in range(unloadNum):
            unload_rows[i].find_element(*self.unloadPrice_int_loc).send_keys(unloadPrices[i])
        # out
        out_rows=self.find_elements(*self.out_rows_loc)
        outNum=len(out_rows)
        minWeights = minWeights.split(",")
        maxWeights = maxWeights.split(",")
        outPrices = outPrices.split(",")
        for i in range(outNum):
            print(i)
            out_rows[i].find_element(*self.minWeight_int_loc).send_keys(minWeights[i])
            out_rows[i].find_element(*self.maxWeight_int_loc).send_keys(maxWeights[i])
            out_rows[i].find_element(*self.outprice_int_loc).send_keys(outPrices[i])
        # in
        in_rows=self.find_elements(*self.inPrice_multi_loc)
        inNum=len(in_rows)
        inPrices=inPrices.split(",")
        for i in range(inNum):
            in_rows[i].send_keys(inPrices[i])
        # pallet
        self.find_element(*self.palletPrice_loc).send_keys(palletPrice)
        # labeling
        self.find_element(*self.labelingPrice_loc).send_keys(labelPrice)
        # save or submit the form
#         if action_type == "save":
#             self.find_element(*self.save_btn_loc).click()
#         else:
#             self.find_element(*self.effect_btn_loc).click()

#     def item_detail(self):
        

if __name__=="__main__":
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(chrome_options=option)
    driver.maximize_window()
    login=LoginPage(driver)
    login.open()
    time.sleep(1)
    account = login.login("zhangsan", "123456")
    assert account.text == "zhangsan"
    login.switch_lang()
    tempPage =TemplateListPage(driver)
    tempPage.open()
#     query_cdt = {"templateType":(1,),"priceType":(1,),"status":(1,),"templateName":"","validTime":"2022-02-01,2022-02-28"}
#     query_cdt={"validTime":"2022-02-01,2022-02-28"}
#     tempPage.query(**query_cdt)
#     tempPage.add_expressfee()
#     tempPage.close_cur_page()
#     tempPage.add_storagefee()
#     tempPage.close_cur_page()
    fpath=tools.get_fpath("files","addStoragefee_args.xlsx")
    value_util=ExcelUtil(fpath,"value_dict")
    value_list=value_util.dict_data()
    print(value_list)
    
    value_dict=value_list[0]
    print(value_dict)
    tempPage.add_storagefee(value_dict)
    print("end..")

