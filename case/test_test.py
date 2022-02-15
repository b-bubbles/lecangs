'''
Created on 2022-2-15

@author: Administrator
'''
import pytest
# @pytest.mark.parametrize("myfixture", aa, indirect=True)  


aa=[{"user":"lixiuzhu","password":"1234567w"}]
@pytest.fixture() 
def myfixture1(myfixture):
    print("test_01,%s,run..."%type(myfixture1))
    
    
def test_01(myfixture1):
    print("test_01,run...")
     
def test_02(myfixture1):
    print("test_02,run...")
 
 
if __name__=="__main__":
    pytest.main(["-s","test_test.py"])    
    
    
    
       