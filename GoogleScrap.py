# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 10:57:41 2017

@author: bojun.lin
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import os
import time  
import urllib.request

def browserInit():
    print ("Browser is loading... please wait...")
    driverPath = "";
    if sys.platform == "darwin":
        driverPath = os.path.join(os.path.abspath(os.curdir),"chromedriver")          #mac
    elif sys.platform == "win32" or sys.platform == "win64":
        driverPath = os.path.join(os.path.abspath(os.curdir),"chromedriver.exe")      #windows
    driver = webdriver.Chrome(driverPath)
    driver.maximize_window()  
    return driver

def search(mbrowser, searchContent):
    mbrowser.get('https://www.google.com/imghp')
    
    _searchContent = searchContent
    assert "Google Images" in mbrowser.title
    print ("Searching",searchContent, "...")
    mbrowser.find_element_by_id("lst-ib").send_keys(_searchContent)
    mbrowser.find_element_by_id("lst-ib").send_keys(Keys.RETURN)
    assert "No results found." not in mbrowser.page_source
    return _searchContent

def makeDir(searchObj):
    dir_name = os.path.join(os.path.abspath(os.curdir),'images', searchObj)
    if(os.path.exists(dir_name)!=True):
        os.makedirs(dir_name)
        print (dir_name, " is created!")
    return dir_name

def findAndSaveImg(mbrowser, searchContent, dirName):
    image_url_dic = {}  #crawled img_url
    thumbnailXpath = "//img[@class='rg_ic rg_i']"
    # Simulate scrolling  
    pos = 0  
    count = 0 # image count  
    for i in range(10):  
        #pos += i*500 # scroll down 500  
        #js = "document.body.scrollTop=%d" % pos
        js = "window.scrollTo(0, document.body.scrollHeight)"
        mbrowser.execute_script(js)   
        time.sleep(3) 
        
        imageHolders = mbrowser.find_elements_by_xpath(thumbnailXpath)
        
        for imgHolder in imageHolders:  
            img_url = imgHolder.get_attribute('src')
            if (img_url != None and not img_url in image_url_dic):
                count += 1 
                image_url_dic[img_url] = ''                 # this add img_url to img_url_dic, set its content to ""

                #read image data
                img_data = urllib.request.urlopen(img_url).read()
                print("Downloading %d" % count , '-'*10 , 'size:' , str(img_data.__len__()/1024) , 'KB')   # , could bind string and int
                file_name="pic%s.jpg"%(count)
                #Save Image 
                f = open(os.path.join(dirName, file_name), 'wb')
                f.write(img_data)  
                f.close() 
                time.sleep(0.1)
            #else:
                 #print('No image found')                           
    print("Download complete!")


#=============Main============================
if __name__ == "__main__":
    browser = browserInit()
    obj_name = input('Input item name: ')
    searchObj = search(browser, obj_name)
    savedir = makeDir(obj_name)
    findAndSaveImg(browser, searchObj, savedir)
    browser.quit()
    