from selenium import webdriver
from bs4 import BeautifulSoup
import time

#Xpath to elements 
path_of_court_type_dropdown = """//*[@id="courTypesButton"]"""
path_to_select_all_court = """//*[@id="courTypesMultiSelect"]/ul/li[1]/a/label/input"""

def courttype(browser, court_selections):
    
    #Clicking on the field to access dropdown
    browser.find_element_by_xpath(path_of_court_type_dropdown).click()
    
    #Unselecting 'Select all', it is done 3 times to avoid case types not loading problem 
    browser.find_element_by_xpath(path_to_select_all_court).click()
    time.sleep(2)
    browser.find_element_by_xpath(path_to_select_all_court).click()
    time.sleep(2)
    browser.find_element_by_xpath(path_to_select_all_court).click()
    time.sleep(2)

    #Selecting specified court types
    for selections in court_selections:
        path_to_select_specifics = '/html/body/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div[1]/div[2]/div[3]/div[2]/div/div/ul/li/a/*[text()=\'' +selections+'\']/input'
        browser.find_element_by_xpath(path_to_select_specifics).click()
        time.sleep(1)

    #Unselecting dropdown
    browser.find_element_by_xpath(path_of_court_type_dropdown).click()
