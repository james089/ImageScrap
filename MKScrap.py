# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 12:23:08 2017

@author: bojun.lin
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time  
import urllib.request

img_url_dic = {}  
xpath = "/html/body[@class='mk-web']/div[@id='app']/div[@class='app']/div[@class='mk-search-page']/div[@class='search-visible-panel']/section[@id='pageBodyWrapper']/div[@class='panel content-wrapper']/div[@class='result-panel']/div[@class='restricted-content row']/main[@class='medium-12 small-12 large-9 columns result-container panel']/div[@class='medium-12 row panel tile-listing']/ul[@class='product-wrapper product-wrapper-four-tile']//div[@class='product-tile-container']/div[@class='image-panel']/a/div[@class='product-image-container']/div[@class='LazyLoad is-visible']/img[@class='product-image']"

browser = webdriver.Chrome("C:\local\chromedriver.exe")
browser.maximize_window()  
browser.get('https://www.michaelkors.com/search/_/N-0/Ntt-')

assert "Michael Kors" in browser.title
elem = browser.find_element_by_id("search-box")
searchObject = "bag"
elem.send_keys(searchObject)
elem.send_keys(Keys.RETURN)
assert "No results found." not in browser.page_source

# Make dir
root_dir='C:\\temp\\'
dir_name=root_dir

if(os.path.exists(root_dir)!=True):
    os.mkdir(root_dir)
if(os.path.exists(dir_name)!=True):
    os.mkdir(dir_name)
  

# 模拟滚动窗口以浏览下载更多图片  
pos = 0  
count = 0 # 图片编号  
for i in range(10):  
    pos += i*500 # 每次下滚500  
    js = "document.body.scrollTop=%d" % pos  
    browser.execute_script(js)  
    time.sleep(5)     
  
    images=browser.find_elements_by_xpath(xpath)
    for element in images: 
        count+=1
        img_url = element.get_attribute('src')  
        if img_url != None and not img_url in img_url_dic:
                img_url_dic[img_url] = ''  
                #ext = img_url.split('.')[-1]  
                file_name="%s_%s_%s.jpg"%(browser.title, searchObject, count)
                #保存图片数据  
                data = urllib.request.urlopen(img_url).read()
                f = open(root_dir + file_name, 'wb')
                f.write(data)  
                f.close() 
                time.sleep(0.1)
browser.close()