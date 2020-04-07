from io import BytesIO
from selenium import webdriver
from bs4 import BeautifulSoup
import pytesseract as tess
from PIL import Image
import time
import os

#Xpath to captcha image
path_to_captcha = '//*[@id="mainTableContent"]/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div[3]/form/img'
path_to_enter_captcha = """//*[@id="mainTableContent"]/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div[3]/form/input[2]"""


#Module for the solution of captcha image
def captcha_solver(browser):

    # Getting location and size of captcha image
    element = browser.find_element_by_xpath(path_to_captcha) 
    location = element.location
    size = element.size

    #Getting screenshot of the page
    png = browser.get_screenshot_as_png()

    # uses PIL library to open image in memory
    im = Image.open(BytesIO(png)) 

    # defines crop points
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    #Extracting captcha from screenshot and saving image
    im = im.crop((left, top, right, bottom)) 
    im.save('captcha.png') 

    #using pytessearact for getting numbers from the image
    im = Image.open('captcha.png')
    captcha = tess.image_to_string(im)
    solution = 0
    i=0
    #Concluding sum from characters
    for x in captcha:
        if x.isdigit():
            if i<2:
                solution = solution*10 +int(x)
                i=i+1    
            else:
                solution += int(x)
    os.remove('captcha.png')
    browser.find_element_by_xpath(path_to_enter_captcha).send_keys(solution)
