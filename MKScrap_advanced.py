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

def browserInit():
    driver = webdriver.Chrome("C:\local\chromedriver.exe")
    driver.maximize_window()  
    return driver

def search(mbrowser, searchContent):
    mbrowser.get('https://www.michaelkors.com/search/_/N-0/Ntt-')
    
    _searchContent = searchContent
    assert "Michael Kors" in mbrowser.title
    mbrowser.find_element_by_id("search-box").send_keys(_searchContent)
    mbrowser.find_element_by_id("search-box").send_keys(Keys.RETURN)
    assert "No results found." not in mbrowser.page_source
    return _searchContent

def makeDir():
    dir_name = os.path.abspath(os.curdir) + "\\images\\"
    if(os.path.exists(dir_name)!=True):
        os.mkdir(dir_name)
    return dir_name

def findAndSaveImg(mbrowser, searchContent, dirName):
    img_url_dic = {}  #crawled img_url
    thumbnailXpath = "//div[@class='image-panel']/a"
    fullResImgXpath = "//div[@class='float-right medium-10 large-10 large-offset-2']/div[@class='gallery-images']/a[1]/figure[@class='gallery-images-item']/img"    
    # 模拟滚动窗口以浏览下载更多图片  
    pos = 0  
    count = 0 # 图片编号  
    for i in range(10):  
        pos += i*500 # 每次下滚500  
        #js = "document.body.scrollTop=%d" % pos  
        #browser.execute_script(js)    
        
        elements = mbrowser.find_elements_by_xpath(thumbnailXpath)
        #for element in elements: 
        for i in range(len(elements)):
            
            elements = mbrowser.find_elements_by_xpath(thumbnailXpath)
            mbrowser.get(elements[i].get_attribute('href'))
            
            image = mbrowser.find_elements_by_xpath(fullResImgXpath)
            img_url = image[0].get_attribute('src')  
            
            if img_url != None and not img_url in img_url_dic:
                img_url_dic[img_url] = ''                 #这句直接就把img_url作为一个对象加入了dictionary，内容为”“
                count += 1 
                
                img_file = urllib.request.urlopen(img_url)
                imgbyte=img_file.read()
                print("Downloading %d" % count , '-'*10 , 'size:' , str(imgbyte.__len__()/1024) , 'KB')   # , 可以连接所有类型
            
                file_name="%s_%s_%s.jpg"%("MKbags", searchContent, count)
                #保存图片数据  
                data = imgbyte
                f = open(dirName + file_name, 'wb')
                f.write(data)  
                f.close() 
                time.sleep(0.1)
            mbrowser.back()                               #execute_script("window.history.go(-1)")
    print("Download complete!")


#=============Main============================
if __name__ == "__main__":
    browser = browserInit()
    searchObj = search(browser, "bag")
    savedir = makeDir()
    findAndSaveImg(browser, searchObj, savedir)
    browser.quit()
    