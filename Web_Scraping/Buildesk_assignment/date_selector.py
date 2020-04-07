from selenium import webdriver
from bs4 import BeautifulSoup
import time

#Xpath to elements 
path_to_open_from = """//*[@id="openedFrom"]"""
path_to_back_open_from = """//*[@id="ui-datepicker-div"]/div/a[1]"""
path_to_open_to = """//*[@id="openedTo"]"""
path_to_back_open_to = """//*[@id="ui-datepicker-div"]/div/a[1]"""



# Method to set date in the table
def date(browser, dateopened, dateopenedto):

    flag = True
    while(flag):
        try:
            #Extracting day, month and year from the date to be used as arguments
            date = dateopened.split('/')[0].lstrip('0')
            month = dateopened.split('/')[1].lstrip('0')
            year = dateopened.split('/')[2]
            flag = False
        except:
            dateopened = input("Please provide date in (dd/mm/yyyy) format only")
        
      

    #Clicking on the field to access date picker
    try:
        browser.find_element_by_xpath(path_to_open_from).click()
    except:
        print("Page isn't loaded properly!!!!!!!!!!!!\n Try again!!!!!!!!")

    #Getting current month and year to determine number of the click(i.e. difference of the month)
    # on back button of datepicker to access date 
    import datetime
    cur_month = datetime.datetime.now().month
    cur_year = datetime.datetime.now().year

    #Calculating the difference of the month
    calendar_click = (int(cur_month) - int(month)) + ((int(cur_year) - int(year))*12)

    #Getting desired month calendar
    for x in range (calendar_click):
        browser.find_element_by_xpath(path_to_back_open_from).click()
    
    #Selecting the date 
    path_of_date_open_from = '//*[@id="ui-datepicker-div"]/table/tbody/tr/td[@data-month=\''+str((int(month)-1))+'\'][@data-year=\''+ year+'\']/*[text()=\''+date+'\']'
    browser.find_element_by_xpath(path_of_date_open_from).click()

    time.sleep(1)
    
    #Same process is Repeated to for openedto date

    #Extracting day, month and year from the date to be used as arguments
    date = dateopenedto.split('/')[0].lstrip('0')
    month = dateopenedto.split('/')[1].lstrip('0')
    year = dateopenedto.split('/')[2]

    #Clicking on the field to access date picker
    browser.find_element_by_xpath(path_to_open_to).click()

    #Calculating the difference of the month
    calendar_click = (int(cur_month) - int(month)) + ((int(cur_year) - int(year))*12)

    #Getting desired month calendar
    for x in range (calendar_click):
        browser.find_element_by_xpath(path_to_back_open_to).click()
    
    #Selecting the date
    path_of_date_open_to = '//*[@id="ui-datepicker-div"]/table/tbody/tr/td[@data-month=\''+str((int(month)-1))+'\'][@data-year=\''+ year+'\']/*[text()=\''+date+'\']'
    browser.find_element_by_xpath(path_of_date_open_to).click()
