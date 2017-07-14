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
xpath = "/html/body[@class='mk-web']/div[@id='app']/div[@class='app']/div[@class='mk-search-page']/div[@class='search-visible-panel']/section[@id='pageBodyWrapper']/div[@class='panel content-wrapper']/div[@class='result-panel']/div[@class='restricted-content row']/main[@class='medium-12 small-12 large-9 columns result-container panel']/div[@class='medium-12 row panel tile-listing']/ul[@class='product-wrapper product-wrapper-four-tile']//div[@class='product-tile-container']/div[@class='image-panel']/a"
subXpath = "/html/body[@class='mk-web']/div[@id='app']/div[@class='app']/div[@class='mk-pdp-page']/section[@class='row pdp-main aria-restricted page-body-wrapper page-padding']/div[@class='panel content-wrapper']/section[@class='row pdp-main-content restricted-content']/div[@class='product-img-carousel column small-12 medium-12 large-6']/div[@class='pdp-gallery']/div[@class='pdp-gallery-list']/div[@class='gallery clearfix row']/div[@class='float-right medium-10 large-10 large-offset-2']/div[@class='gallery-images']/a[1]/figure[@class='gallery-images-item']/img"
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
    #js = "document.body.scrollTop=%d" % pos  
    #browser.execute_script(js)    
    
    elements = browser.find_elements_by_xpath(xpath)
    #for element in elements: 
    for i in range(len(elements)):
        
        elements = browser.find_elements_by_xpath(xpath)
        browser.get(elements[i].get_attribute('href'))
        
        image = browser.find_elements_by_xpath(subXpath)
        img_url = image[0].get_attribute('src')  
        print("Downloading from..." + img_url)
        
        
        if img_url != None and not img_url in img_url_dic:
            img_url_dic[img_url] = ''                 #这句直接就把img_url作为一个对象加入了dictionary，内容为”“
            count+=1 
            file_name="%s_%s_%s.jpg"%("MKbags", searchObject, count)
            #保存图片数据  
            data = urllib.request.urlopen(img_url).read()
            f = open(root_dir + file_name, 'wb')
            f.write(data)  
            f.close() 
            time.sleep(0.1)
        browser.back()                               #execute_script("window.history.go(-1)")
browser.close()