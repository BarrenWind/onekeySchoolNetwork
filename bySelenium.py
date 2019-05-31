#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

try:
     f=open(".logindata.data",'r')
     info=[]
     for a in f.readlines():
         info.append(a.rstrip('\n'))
     f.close()
     if info.__len__()<1:
         info.append(str(input("输入学号：")))
         info.append(str(input("输入密码：")))
         f=open(".logindata.data",'w')
         f.write("\n".join(info))
         f.close()
except:
    info=[]
    info.append(str(input("输入学号：")))
    info.append(str(input("输入密码：")))
    f=open(".logindata.data",'w')
    f.write("\n".join(info))
    f.close()
studentId=info[0]
passwd=info[1]
driver=webdriver.Chrome()
driver.minimize_window()
driver.get("http://172.16.2.100")
elem=driver.find_element_by_xpath('//*[@id="edit_body"]/div[3]/div[3]/form/input[2]')
elem.click()
elem.send_keys(studentId)
elem=driver.find_element_by_xpath('//*[@id="edit_body"]/div[3]/div[3]/form/input[3]')
elem.click()
elem.send_keys(passwd)
select=Select(driver.find_element_by_xpath('//*[@id="edit_body"]/div[3]/select'))
select.select_by_index(1)
elem=driver.find_element_by_xpath('//*[@id="edit_body"]/div[3]/div[3]/form/input[1]').click()
print(driver.get_cookies())
driver.close()
