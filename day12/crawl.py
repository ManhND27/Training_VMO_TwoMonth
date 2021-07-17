import time
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import pandas as pd

#1. Khai bao bien brower
brower = webdriver.Chrome(executable_path="D:\Coder\src\PROJECT AI\ketquasoxo\chromedriver.exe")
data = []
years = []
month = []
cve = [[[]]]
idx = 0

url = 'https://nvd.nist.gov/vuln/full-listing'
brower.get(url)
#time.sleep(1)
main = brower.find_element_by_id("body-section")
for i in range(2,36):
    year = main.find_elements_by_xpath("/html/body/div[2]/div[2]/span[{}]/strong".format(i))
    for y in year:
        years.append(y.text)
    li_i = main.find_elements_by_xpath("/html/body/div[2]/div[2]/span[{}]/ul/li".format(i))
    month_i = []
    for li in li_i:
        li_text = li.find_element_by_tag_name("a")
        month_i.append(li_text.text)
    month.append(month_i)
    link = []
    for li in li_i:
        idx += 1
        li_text = li.find_element_by_tag_name("a")
        link.append(li_text.get_attribute('href'))
        print(li_text.get_attribute('href'))
        li_text.click()
        """
        brower.get(li_text.get_attribute('href'))
        spans = brower.find_elements_by_xpath("/html/body/div[2]/div[2]/div/span")
        for span in spans:
            cve[i][idx].append(span.text)
        brower.back()
print(type(years))
print(years)
print(type(month))
print(month)
print(type(cve))
print(cve)
brower.close()
"""
# li_i = li_i_1[i].find_elements_by_tag_name("li")
"""

"""
