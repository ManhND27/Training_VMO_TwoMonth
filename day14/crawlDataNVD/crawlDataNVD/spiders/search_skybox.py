# import time
# import json
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from time import sleep
# from selenium.webdriver.common.keys import Keys
# #import pandas as pd
# import scrapy
# options = Options()
#
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# brower = webdriver.Chrome(executable_path="D:\Coder\src\PROJECT AI\ketquasoxo\chromedriver.exe")
# #time.sleep(10)
# url = 'https://www.vulnerabilitycenter.com/#home'
# brower.get(url)
# input_search_query = brower.find_element_by_class_name("svc-SearchBox")
# f = open('year_month_cve.json')
# data = json.load(f)
# url_tails = []
# for i in data:
#     url_tails.append(i["id"])
# count = 0
# for i in url_tails:
#     input_search_query.clear()
#     input_search_query.send_keys(i)
#
#     btn_search = brower.find_element_by_class_name("svc-Button")
#     btn_search.click()
#     count += 1
# print(count)
#
#
