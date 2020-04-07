from selenium import webdriver
from bs4 import BeautifulSoup
import time
import data
import date_selector
import court_selector
import case_selector
import captcha_solution
import data_extraction
#This module take care of accessing the browser and initiating its instance

def open_browser(url):
    try:
        try:
            browser = webdriver.Chrome()
        except:
            print("Error opening Browser!!!!!!!!!\nPlease check executable path")
        
        browser.get(url)
    except:
        print("Can't open url")
        browser.get(url)
    return browser


if __name__ == '__main__':

    flag = True
    
    #For retrying in case of wrong captcha extraction 
    while(flag):

        # Opening Web Browser and Visiting url
        browser = open_browser(data.url)
        
        #Entering field data into the fields
        date_selector.date(browser, data.dateopenedfrom, data.dateopenedto)
        court_selector.courttype(browser, data.court_selections)
        case_selector.casetype(browser, data.case_selections)
        captcha_solution.captcha_solver(browser)
        
        #Clicking Search button to submit 
        time.sleep(5)
        browser.find_element_by_xpath("""//*[@id="searchButton"]""").click()

        #To check if captcha was success or not
        flag = (browser.current_url.find(data.url) != -1)
        if flag:
            browser.close()

    data_extraction.iterator(browser)