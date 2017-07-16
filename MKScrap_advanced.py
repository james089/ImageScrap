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
    print ("Browser is loading... please wait...")
    driverPath = os.path.join(os.path.abspath(os.curdir),"chromedriver")          #mac
    #driverPath = os.path.join(os.path.abspath(os.curdir),"chromedriver.exe")      #windows
    driver = webdriver.Chrome(driverPath)
    driver.maximize_window()  
    return driver

def search(mbrowser, searchContent):
    mbrowser.get('https://www.michaelkors.com/search/_/N-0/Ntt-')
    
    _searchContent = searchContent
    assert "Michael Kors" in mbrowser.title
    print ("Searching",searchContent, "...")
    mbrowser.find_element_by_id("search-box").send_keys(_searchContent)
    mbrowser.find_element_by_id("search-box").send_keys(Keys.RETURN)
    assert "No results found." not in mbrowser.page_source
    return _searchContent

def makeDir(searchObj):
    dir_name = os.path.join(os.path.abspath(os.curdir),'images', searchObj)
    if(os.path.exists(dir_name)!=True):
        os.makedirs(dir_name)
        print (dir_name, " is created!")
    return dir_name

def findAndSaveImg(mbrowser, searchContent, dirName):
    element_url_dic = {}  #crawled img_url
    thumbnailXpath = "//div[@class='image-panel']/a"
    fullResImgHolderXpath = "//div[@class='float-right medium-10 large-10 large-offset-2']/div[@class='gallery-images']/a[1]/figure[@class='gallery-images-item']/img"    
    # Simulate scrolling  
    pos = 0  
    count = 0 # image count  
    for i in range(10):  
        pos += i*500 # scroll down 500  
        js = "document.body.scrollTop=%d" % pos  
        mbrowser.execute_script(js)    
        
        elements = mbrowser.find_elements_by_xpath(thumbnailXpath)
        #for element in elements: 
        for i in range(len(elements)):
            
            elements = mbrowser.find_elements_by_xpath(thumbnailXpath)
            element_url = elements[i].get_attribute('href')
            
            if (element_url != None and not element_url in element_url_dic):
                element_url_dic[element_url] = ''                 # this add img_url to img_url_dic, set its content to ""
                mbrowser.get(element_url)                         # enter thumbnail, into new page
                
                img_holder = mbrowser.find_elements_by_xpath(fullResImgHolderXpath)
                j = 0
                for imgdf in img_holder:
                    j+=1
                    
                if img_holder != None and j >= 1:
                    img_url = img_holder[0].get_attribute('src')
                    #Saving img and other info
                    count += 1 
                    #read item info
                    itemInfo = {
                        'name': mbrowser.find_elements_by_xpath("//h1")[0].text.replace(' ', '_'),
                        'styleName': mbrowser.find_elements_by_xpath("//li[@class='style-name']")[0].text.replace('Style# ', '')
                    }
                    #read image data
                    img_data = urllib.request.urlopen(img_url).read()
                    print("Downloading %d" % count , '-'*10 , 'size:' , str(img_data.__len__()/1024) , 'KB')   # , could bind string and int
                    file_name="%s_%s_%s.jpg"%(count, itemInfo['name'], itemInfo['styleName'])
                    #Save Image 
                    f = open(os.path.join(dirName, file_name), 'wb')
                    f.write(img_data)  
                    f.close() 
                    time.sleep(0.1)
                else:
                     print('No image found')  
                mbrowser.back()                               
    print("Download complete!")


#=============Main============================
if __name__ == "__main__":
    browser = browserInit()
    obj_name = input('Input item name: ')
    searchObj = search(browser, obj_name)
    savedir = makeDir(obj_name)
    findAndSaveImg(browser, searchObj, savedir)
    browser.quit()
    