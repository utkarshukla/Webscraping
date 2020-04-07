from csv import DictWriter
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
from io import BytesIO
import re
import pytesseract as tess
import os

def iterator(browser):

    # to iterate in case of multiple pages
    next_page = True
    
    while(next_page):
    
        # This is going to extract
        data_extract(browser)

        #Click next page         
        browser.find_element_by_xpath('//*[@id="gridSearchResults_next"]').click()
        


def data_extract(browser):
    
    #To not iterate a link again and again
    case_num = ''

    #This is a to get all row in result page
    for i in range(len(browser.find_elements_by_xpath('//*[@id="gridSearchResults"]/tbody/tr'))):
        time.sleep(5)
        
        #Checking if case is open
        if browser.find_element_by_xpath('//*[@id="gridSearchResults"]/tbody/tr['+str(i+1)+']/td[4]').text == 'OPEN' and browser.find_element_by_xpath('//*[@id="gridSearchResults"]/tbody/tr['+str(i+1)+']/td[3]/a').text.strip() != case_num.strip():
            
            #Opening link
            browser.find_element_by_xpath('//*[@id="gridSearchResults"]/tbody/tr['+str(i+1)+']/td[3]/a').click()
            time.sleep(10)

            #This is to get defendent name and plantiff
            path_to_parties = '//*[@id="gridParties"]/tbody/tr'
            parties_list = browser.find_elements_by_xpath(path_to_parties)
            
            #Dictionary to store all data
            dict_info = {
                "CaseDate":"",
                "CaseId":"",
                "CaseType":"",
                "DefendantName":"",
                "BankName":"",
                "ClaimValue":"NA",
            }

            # Iterating to get find relevant parties
            for i in range(len(parties_list)): 

                #Checking if its defedent and not on the data
                if (browser.find_element_by_xpath('//*[@id="gridParties"]/tbody/tr['+ str(i+1)+']/td[1]').text.strip() == 'DEFENDANT') and (dict_info['DefendantName']==''):
                    dict_info["DefendantName"] = browser.find_element_by_xpath('//*[@id="gridParties"]/tbody/tr['+ str(i+1)+']/td[2]//a').text
                    
                #Checking if its BankName    
                if browser.find_element_by_xpath('//*[@id="gridParties"]/tbody/tr['+ str(i+1)+']/td[1]').text.strip() == 'PLAINTIFF':
                    dict_info["BankName"] = browser.find_element_by_xpath('//*[@id="gridParties"]/tbody/tr['+ str(i+1)+']/td[2]//div').text

            #Getting Date, Id, CaseType
            dict_info['CaseDate'] = browser.find_element_by_xpath('//*[@id="summaryAccordionCollapse"]/table/tbody/tr/td/dl/dd[@class=\'clerkfiledate\']').text
            case_num = dict_info['CaseId'] = browser.find_element_by_xpath('//*[@id="summaryAccordionCollapse"]/table/tbody/tr/td/dl/dd[@class=\'casenumber\']').text
            dict_info['CaseType'] = browser.find_element_by_xpath('//*[@id="summaryAccordionCollapse"]/table/tbody/tr/td/dl/dd[@class=\'casetype\']').text
            
            #To take back handle after opening pdf
            result_page = browser.current_window_handle
                    
            #To get all Dockets
            path_to_dockets = '//*[@id="gridDockets"]/tbody/tr'
            Dockets = browser.find_elements_by_xpath(path_to_dockets)
            for Docket in range (len(Dockets)):
                
                #Checking if docket is having value of cost
                if browser.find_element_by_xpath('//*[@id="gridDockets"]/tbody/tr['+str(Docket+1)+']/td[3]').text.find('VALUE OF REAL PROPERTY OR MORTGAGE FORECLOSURE CLAIM:') != -1:
                    
                    #Opening pdf
                    browser.find_element_by_xpath('//*[@id="gridDockets"]/tbody/tr['+str(Docket+1)+']/td[1]//a').click()
                    
                    #Wait Time to get pdf loaded
                    time.sleep(15)

                    #initiating cost page handle
                    cost = result_page    

                    #Getting handle of the pdf
                    for handle in browser.window_handles: 
                        if handle != result_page: 
                            cost = handle
                    
                    #Switching handle to pdf
                    browser.switch_to.window(cost)

                    #Getting screenshot and saving
                    png = browser.get_screenshot_as_png()
                    im = Image.open(BytesIO(png))
                    im.save('cost.png')

                    #closing pdf page to avoid getting wrong result
                    browser.close()

                    #Extracting data from image
                    im = Image.open('cost.png')
                    captcha = tess.image_to_string(im)
                    ls = captcha.split('\n')
                    for x in ls:
                        if x.find('TOTAL ESTIMATED VALUE OF CLAIM') != -1:
                            print(x)
                            dict_info['ClaimValue'] = re.findall(r'[$][\d|,|.]+',x)
                            print(dict_info['ClaimValue'])

                    #Getting back handle to result_page
                    browser.switch_to.window(result_page)
                    
                    #Deleting file to avoid false result
                    os.remove('cost.png')
                    break
            
            
            #saving data on the file final.csv
           
            with open('final.csv','a',newline='') as f:
                csv_writer = DictWriter(f, fieldnames=['CaseDate','CaseId','CaseType','DefendantName','BankName','ClaimValue'])
                csv_writer.writerow(dict_info)
            browser.back()
