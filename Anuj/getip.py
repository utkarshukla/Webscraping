from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import re
import time
import csv


url = "https://lists.blocklist.de/lists/all.txt"

check_url = 'https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a1.20.137.212&run=toolpage#'

browser = webdriver.Chrome()
browser.get(url)

get_ips= browser.find_element_by_xpath('/html/body/pre').text

ips = get_ips.split('\n')
print(ips)
browser.quit()
time.sleep(5)
browser = webdriver.Chrome()
browser.get(check_url)
time.sleep(6)
for ip in ips:
    time.sleep(5)
    browser.find_element_by_xpath('//*[@id="txtInput2"]').clear()
    browser.find_element_by_xpath('//*[@id="txtInput2"]').send_keys(ip)
    browser.find_element_by_xpath('//*[@id="btnAction3"]').click()
    time.sleep(5)
    ls = []
    ls.append(ip)
    time.sleep(2)

    results_path = ('//div[3]/table/tbody/tr')
    results = browser.find_elements_by_xpath(results_path)

    for result in range(88):
        print("checking list")
        img_src = browser.find_element_by_xpath('//div[3]/table/tbody/tr['+ str(result+1) +']/td[1]/img').get_attribute('src')
        print(img_src)
        if img_src == 'https://mxtoolbox.com/public/images/statusicons/problem.png':
            print('blacklisted')
            ls.append(browser.find_element_by_xpath('//div[3]/table/tbody/tr['+ str(result+1) +']/td[2]/span').text)
            print('appending')
    with open('final.csv','a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(ls)
    print(ls)
                        
                    