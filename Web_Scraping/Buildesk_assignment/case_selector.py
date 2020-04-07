from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Xpath to elements 
id = "caseTypesButton"
path_of_case_type_dropdown = """//*[@id="caseTypesButton"]"""
path_to_select_all_case = """/html/body/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div[1]/div[2]/div[4]/div[2]/div/div/ul/li[1]/a/label/input"""
path_to_case_types = """/html/body/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div[1]/div[2]/div[4]/div[2]/div/div/ul/li/a/label"""



def casetype(browser, case_selections):
    

    #Add wait to avoid exception due to element not loaded
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, id))
    )

    #Clicking on the field to access dropdown
    browser.find_element_by_xpath(path_of_case_type_dropdown).click()

    #Unselecting all
    browser.find_element_by_xpath(path_to_select_all_case).click()

    #Selecting specified case types
    case_types = browser.find_elements_by_xpath(path_to_case_types)

    #iteration over specified types
    for selector in case_selections:
        i = 1
        #iteration to match webelements
        for case in case_types:
            if case.text.find(selector) != -1:
                #Creating path for that specified element
                dynamic_path = '/html/body/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div[1]/div[2]/div[4]/div[2]/div/div/ul/li['+str(i)+']/a/label/input'
                #Selecting specified elements
                browser.find_element_by_xpath(dynamic_path).click()
            i=i+1
            
    #Clicking on the field to access dropdown
    browser.find_element_by_xpath(path_of_case_type_dropdown).click()