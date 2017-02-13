# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 11:58:20 2015

@author: larry.jerome
"""

from splinter import Browser                
#with Browser() as browser: 
#  browser.visit("http://ps-dev.kippdc.org/admin/pw.html")
#  #browser.fill('login-inputs', 'larry.jerome;Cubs1908!')
#  browser.find_by_name('Submit').click()
#  #copied_text = browser.find_by_id('results')[0].text
#  

browser = Browser()



#browser.visit('http://google.com')
#browser.fill('q', 'splinter - python acceptance testing for web applications')

browser.visit('https://powerschool.kippdc.org/admin/pw.html')
#browser.fill('fieldPassword','larry.jerome;Cubs1908!')
inputField = browser.find_by_id('fieldUsername')
inputField[0].fill('larry.jerome')
inputField2 = browser.find_by_id('fieldPassword')
inputField2[0].fill('BicycleRace1!')
button = browser.find_by_id('btnEnter')
button.click()
