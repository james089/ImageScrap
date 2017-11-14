# ImageScrap
Scrapping images from website, using selenium to navigate website

Simple Setup GUIDE:
1. Anaconda for Python 3.6 (graphical) https://www.continuum.io/downloads#macos
2. Open Terminal in MacOS, type "source activate root" to activate the default python 3.6 environment
3. In terminal, type "pip install selenium"
4. Open Anaconda, launch Spyder, load ImageScrap_advanced.py, and run it (or just use terminal and find the location of it, use "python ImageScrap_advanced.py" to run it)


Tips:
1. The reason to use Selenium is that MK website shows new images while you scroll down the page, without scrolling you can't find all images. Selenium could simulate scrolling.
2. Selenium is using a chromedriver to open chrome browser, which is already included in root folder of this project. If you make your own project, remember to include this driver.
