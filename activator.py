import undetected_chromedriver as uc
from time import sleep
import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from random import randint
from selenium import webdriver
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv('config.env')
style_conf = {
    'Condominium' : os.getenv('Condominium'),
    'Co_op' : os.getenv('Co_op'),
    'Duplex' : os.getenv('Duplex'),
    'Farm_and_Ranch' : os.getenv('Farm_and_Ranch'),
    'House' : os.getenv('House'),
    'Lots_and_Land' : os.getenv('Lots_and_Land'),
    'Mobile_Manufactured_Modular_House' : os.getenv('Mobile_Manufactured_Modular_House'),
    'Multi_Family' : os.getenv('Multi_Family'),
    'Recreational_Cabin_Timeshare_etc' : os.getenv('Recreational_Cabin_Timeshare_etc'),
    'Single_Family' : os.getenv('Single_Family'),
    'Townhouse' : os.getenv('Townhouse'),
    'Triplex' : os.getenv('Triplex'),
    'Apartment' : os.getenv('Apartment'),
}


def init_UC():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-setuid-sandbox')
    headers = {
    'authority': 'accounts.google.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"108.0.5359.125"',
    'sec-ch-ua-full-version-list': '"Not?A_Brand";v="8.0.0.0", "Chromium";v="108.0.5359.125", "Google Chrome";v="108.0.5359.125"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"8.0.0"',
    'sec-ch-ua-wow64': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'x-chrome-id-consistency-request': 'version=1,client_id=77185425430.apps.googleusercontent.com,device_id=91c169ab-71ab-4040-933c-d2bca9ab8f98,signin_mode=all_accounts,signout_mode=show_confirmation',
    'x-client-data': 'CLL5ygE=',
}
    driver = uc.Chrome(service=Service(chromedriver_autoinstaller.install()),options = chrome_options)
    return driver


username = 'admin@jackhunter.com' # this is  ypour email ! right yes ok 
password = 'Trial_123'


# data  = {
#     'image' : '/user1-128x128.jpg',
#     'address' : '27 Newton Dr',
#     'city' : 'Toronto',
#     'zip_code' : 'M2M 2M6',
#     'price' : '$3,000,000',
#     'sales_type' : 'Sale',
#     'style_string' : 'DetachedLink:N2-StoreyIrreg:Front On:SAcre:40 x 122 Feet',
#     'storey' : '2',
#     'exterior' : 'Brick',
#     'heat' : 'Forced Air / Gas',
#     'ac' : 'Central Air',
#     'sqft' : '',
#     'g_stalls' : '2',
#     'amenties' : '',
#     'remarks' : '***No Door Knock Or Visit Land Permited***Prohibited Transpassing Without Consent***',
#     'extra' : '',
#     'bedrooms' : '2',
#     'bathrooms' : '2'
#     }


def activator(username, password):

    driver = init_UC()
    #login
    driver.get('https://www.point2homes.com/CA')

    actions = ActionChains(driver)

    sleep(randint(1,2))

    try:
        driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()
        sleep(randint(2,3))
    except:
        pass
    driver.find_element(By.XPATH , '//*[@id="login"]').click()

    sleep(randint(1,2))

    while(True):
        try:
            driver.find_element(By.ID ,'Username').click()
            sleep(randint(1,2))
            break
        except:
            sleep(randint(3,5))
    driver.find_element(By.ID , 'Username').send_keys(username)
    sleep(randint(1,2))
    driver.find_element(By.ID ,'Password').click()
    sleep(randint(1,2))
    driver.find_element(By.ID , 'Password').send_keys(password)
    sleep(randint(1,2))

    driver.find_element(By.XPATH , '//*[@id="login_form"]/div/fieldset/div[1]/p/button').click()
    sleep(randint(20,30))

    driver.get('https://www.point2homes.com/Account/MyListings?Tab=Draft')
    
    while(True):
        try:
            draftContainer = driver.find_element(By.ID,'draftListingsContainer')
            if(len(draftContainer.find_elements(By.CLASS_NAME,'item-cnt')) == 0):
                break
            draftContainer.find_elements(By.CLASS_NAME,'item-cnt')[0].find_element(By.CLASS_NAME,'btn-danger').click()
            
            sleep(1.5)
            driver.find_element(By.ID,'btnYes').click()
            sleep(randint(3,5))
        except:
            sleep(2)
            continue
    driver.get('https://www.point2homes.com/Account/MyListings?tab=Archived')
    sleep(3)
    
    while(True):
        try:
            archivedContainer = driver.find_element(By.ID,'archivedListingsContainer')
            if(len(archivedContainer.find_elements(By.CLASS_NAME,'item-cnt')) == 0):
                break
            archivedContainer.find_elements(By.CLASS_NAME,'item-cnt')[0].find_element(By.CLASS_NAME,'btn-danger').click()
            
            sleep(1.5)
            driver.find_element(By.ID,'btnYes').click()
            sleep(randint(3,5))
        except:
            sleep(2)
            continue
          
    


activator('Admin@jackhunter.com' , 'Trial_123')

    


# run_post(data)
