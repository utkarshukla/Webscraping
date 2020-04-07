from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract as tess
from PIL import Image
import time
import re
url = "https://court.martinclerk.com/Home.aspx/Search"


flag = True
while(flag):

    browser = webdriver.Chrome()
    browser.get(url)

    
    time.sleep(1)
    dateopened = '16/03/2020'    
    date = dateopened.split('/')[0].lstrip('0')
    month = dateopened.split('/')[1].lstrip('0')
    year = dateopened.split('/')[2]
    browser.find_element_by_xpath("""//*[@id="openedFrom"]""").click()
    import datetime

    cur_month = datetime.datetime.now().month
    cur_year = datetime.datetime.now().year

    calendar_click = (int(cur_month) - int(month)) + ((int(cur_year) - int(year))*12)
    for x in range (calendar_click):
        browser.find_element_by_xpath("""//*[@id="ui-datepicker-div"]/div/a[1]""").click()

    browser.find_element_by_xpath('//*[@id="ui-datepicker-div"]/table/tbody/tr/td[@data-month=\''+str((int(month)-1))+'\'][@data-year=\''+ year+'\']/*[text()=\''+date+'\']').click()

    time.sleep(1)
    dateopenedto = '22/03/2020'
    date = dateopenedto.split('/')[0].lstrip('0')
    month = dateopenedto.split('/')[1].lstrip('0')
    year = dateopenedto.split('/')[2]
    browser.find_element_by_xpath("""//*[@id="openedTo"]""").click()

    calendar_click = (int(cur_month) - int(month)) + ((int(cur_year) - int(year))*12)
    for x in range (calendar_click):
        browser.find_element_by_xpath("""//*[@id="ui-datepicker-div"]/div/a[1]""").click()

    browser.find_element_by_xpath('//*[@id="ui-datepicker-div"]/table/tbody/tr/td[@data-month=\''+str((int(month)-1))+'\'][@data-year=\''+ year+'\']/*[text()=\''+date+'\']').click()


    browser.find_element_by_xpath("""//*[@id="courTypesButton"]""").click()
    # browser.find_element_by_xpath("""//*[@id="courTypesMultiSelect"]/ul/li[1]/a/label/input""").click()
    # selections_court =[' Appeal From County Court',' County Civil']

    # for selections in selections_court:
    #     path = '/html/body/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div[1]/div[2]/div[3]/div[2]/div/div/ul/li/a/*[text()=\'' +selections+'\']/input'
    #     browser.find_element_by_xpath(path).click()
    #     time.sleep(1)

    browser.find_element_by_xpath("""//*[@id="courTypesButton"]""").click()

    time.sleep(1)
    browser.find_element_by_xpath("""//*[@id="caseTypesButton"]""").click()

    

    browser.find_element_by_xpath("""/html/body/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div[1]/div[2]/div[4]/div[2]/div/div/ul/li[1]/a/label/input""").click()

    case_types = browser.find_elements_by_xpath("""/html/body/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div[1]/div[2]/div[4]/div[2]/div/div/ul/li/a/label""")
    i = 1
    ls =[]
    
    selctor='REAL PROPERTY'
    for case in case_types:
        if case.text.find(selctor) == 0:
            browser.find_element_by_xpath('/html/body/div[3]/table/tbody/tr/td[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div[1]/div[2]/div[4]/div[2]/div/div/ul/li['+str(i)+']/a/label/input').click()
        i=i+1

    browser.find_element_by_xpath("""//*[@id="caseTypesButton"]""").click()
    


    from io import BytesIO
    element = browser.find_element_by_xpath('//*[@id="mainTableContent"]/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div[3]/form/img') # find part of the page you want image of
    location = element.location
    size = element.size
    png = browser.get_screenshot_as_png()
    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']


    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save('screenshot.png') 

    im = Image.open('screenshot.png')
    captcha = tess.image_to_string(im)
    solution = 0
    i=0
    for x in captcha:
        if x.isdigit():
            if i<2:
                solution = solution*10 +int(x)
                i=i+1    
            else:
                solution += int(x)


    browser.find_element_by_xpath("""//*[@id="mainTableContent"]/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div[3]/form/input[2]""").send_keys(solution)
    time.sleep(6)
    browser.find_element_by_xpath("""//*[@id="searchButton"]""").click()
    flag = (browser.current_url.find(url) != -1)
    if flag:
        browser.close()


time.sleep(5)

from csv import DictWriter
try:

    element = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, "gridSearchResults"))
    )
except:
    pass

case_num = ''
for i in range(len(browser.find_elements_by_xpath('//*[@id="gridSearchResults"]/tbody/tr'))):
    print(case_num)
    if browser.find_element_by_xpath('//*[@id="gridSearchResults"]/tbody/tr['+str(i+1)+']/td[4]').text == 'OPEN' and browser.find_element_by_xpath('//*[@id="gridSearchResults"]/tbody/tr['+str(i+1)+']/td[3]/a').text.strip() != case_num.strip():
        browser.find_element_by_xpath('//*[@id="gridSearchResults"]/tbody/tr['+str(i+1)+']/td[3]/a').click()
        time.sleep(10)
        path_to_parties = '//*[@id="gridParties"]/tbody/tr'
        parties_list = browser.find_elements_by_xpath(path_to_parties)
        defendant_value = False
        dict_info = {
            "CaseDate":"",
            "CaseId":"",
            "CaseType":"",
            "DefendantName":"",
            "BankName":"",
            "ClaimValue":"NA",
        }
        for i in range(len(parties_list)): 
            if (browser.find_element_by_xpath('//*[@id="gridParties"]/tbody/tr['+ str(i+1)+']/td[1]').text.strip() == 'DEFENDANT') and (dict_info['DefendantName']==''):
                dict_info["DefendantName"] = browser.find_element_by_xpath('//*[@id="gridParties"]/tbody/tr['+ str(i+1)+']/td[2]//a').text
                
            if browser.find_element_by_xpath('//*[@id="gridParties"]/tbody/tr['+ str(i+1)+']/td[1]').text.strip() == 'PLAINTIFF':
                dict_info["BankName"] = browser.find_element_by_xpath('//*[@id="gridParties"]/tbody/tr['+ str(i+1)+']/td[2]//div').text

        dict_info['CaseDate'] = browser.find_element_by_xpath('//*[@id="summaryAccordionCollapse"]/table/tbody/tr/td/dl/dd[@class=\'clerkfiledate\']').text
        case_num = dict_info['CaseId'] = browser.find_element_by_xpath('//*[@id="summaryAccordionCollapse"]/table/tbody/tr/td/dl/dd[@class=\'casenumber\']').text
        dict_info['CaseType'] = browser.find_element_by_xpath('//*[@id="summaryAccordionCollapse"]/table/tbody/tr/td/dl/dd[@class=\'casetype\']').text
        
        print('entering')

        main_page = browser.current_window_handle
                
        path_to_dockets = '//*[@id="gridDockets"]/tbody/tr'
        Dockets = browser.find_elements_by_xpath(path_to_dockets)
        for Docket in range (len(Dockets)):
            print('searching')
            if browser.find_element_by_xpath('//*[@id="gridDockets"]/tbody/tr['+str(Docket+1)+']/td[3]').text.find('VALUE OF REAL PROPERTY OR MORTGAGE FORECLOSURE CLAIM:') != -1:
                print('clicking')
                browser.find_element_by_xpath('//*[@id="gridDockets"]/tbody/tr['+str(Docket+1)+']/td[1]//a').click()
                print('click')
                break
        time.sleep(10)
        print('main_page')
        cost = main_page    
        for handle in browser.window_handles: 
            if handle != main_page: 
                cost = handle
        print('switching')
        browser.switch_to.window(cost)

        png = browser.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        im.save('cost.png')

        im = Image.open('cost.png')
        captcha = tess.image_to_string(im)
        ls = captcha.split('\n')
        for x in ls:
            if x.find('TOTAL ESTIMATED VALUE OF CLAIM') != -1:
                dict_info['ClaimValue'] = re.findall(r'[$][\d|,|.]+',x)
        

        browser.switch_to.window(main_page)


        with open('final.csv','a',newline='') as f:
            csv_writer = DictWriter(f, fieldnames=['CaseDate','CaseId','CaseType','DefendantName','BankName','ClaimValue'])
            csv_writer.writerow(dict_info)
        browser.back()
        time.sleep(10)
        browser.find_element_by_xpath('//*[@id="gridSearchResults_next"]').click()
    