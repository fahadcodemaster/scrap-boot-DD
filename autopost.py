import datetime
import pickle
import time

import undetected_chromedriver as uc
from time import sleep
#import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from random import randint
from selenium import webdriver
from dotenv import load_dotenv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


base_dir = os.path.dirname(os.path.realpath(__file__))


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
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1200x600')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-setuid-sandbox')

    user_directory_path = base_dir+'/profile'
    chrome_options.add_argument(f'--user-data-dir={user_directory_path}')


    headers = {
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
    driver = uc.Chrome(executable_path=os.path.join(base_dir,'chromedriver'),options = chrome_options, headers=headers)
    return driver

def get_list_to_post():
    directory = base_dir + "/listings"
    folders = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            folders.append(directory + "/"+  item + "/")
    result_list =[]
    for folder in folders:
        with open(folder + "info", 'rb') as file:
            r = pickle.load(file)
            result_list.append(r)
         
    return result_list



driver = None
wait_driver = None
driver_action = None


def wait_for_element(by , selector) -> WebElement:
    sleep(1)
    try:
        return wait_driver.until(EC.presence_of_element_located((by,selector)))
    except Exception as e:
        return False 
        
def accept_cookie():
    try:
        wait_for_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()
    except Exception as e:
        pass

def login_action(username , password):




    wait_for_element(By.ID , 'Username').clear()
    wait_for_element(By.ID ,'Username').click()

    wait_for_element(By.ID , 'Username').send_keys(username)
    wait_for_element(By.ID ,'Password').click()
    wait_for_element(By.ID ,'Password').clear()
    wait_for_element(By.ID , 'Password').send_keys(password)
    wait_for_element(By.XPATH , '//*[@id="login_form"]/div/div[1]/fieldset/p[3]/button').click()
    wait_for_element(By.CLASS_NAME , 'user-profile-name')# wait to login

def fill_address(data):

    try:
        # click on state
        wait_for_element(By.XPATH,
                         '//*[@id="manuallyInsertedListingForm"]/div[1]/fieldset/div/div[1]/div[2]/div/button/span[2]/span').click()
        state_input = wait_for_element(By.XPATH,
                                      '//*[@id="manuallyInsertedListingForm"]/div[1]/fieldset/div/div[1]/div[2]/div/div/div/input')
        state_input.send_keys(data["State"])
        state_input.send_keys(Keys.ENTER)
        time.sleep(1)
    except:
        pass

    #click on city
    wait_for_element(By.XPATH , '//button[@data-id="citySelector"]').click()
    city_input = wait_for_element(By.XPATH , '//*[@id="manuallyInsertedListingForm"]/div[1]/fieldset/div/div[1]/div[3]/div/div/div/input')
    city_input.send_keys(data["City"])
    city_input.send_keys(Keys.ENTER)
    time.sleep(1)

    #click on Neighborhood
    wait_for_element(By.XPATH , '//*[@id="manuallyInsertedListingForm"]/div[1]/fieldset/div/div[1]/div[4]/div/button/span[2]/span').click()
    neighborhood_input = wait_for_element(By.XPATH , '//*[@id="manuallyInsertedListingForm"]/div[1]/fieldset/div/div[1]/div[4]/div/div/div/input')
    neighborhood_input.send_keys(data["Neighborhood"])
    neighborhood_input.send_keys(Keys.ENTER)
    time.sleep(1)

    # try:
    #     wait_for_element(By.XPATH , '//*[@id="manuallyInsertedListingForm"]/div[1]/fieldset/div/div[1]/div[3]/div/div/ul').click() #select first City after search show
    #     time.sleep(13)
    # except Exception as e:
    #     city_input.clear()
    #     city_input.send_keys("ajax") # this is demo if not find any things
    #     wait_for_element(By.XPATH , '//*[@id="manuallyInsertedListingForm"]/div[1]/fieldset/div/div[1]/div[3]/div/div/ul').click()#select first City after search show


    wait_for_element(By.ID,'Address').click()
    # Modify the address to have capital letters and no unit number
    address = data['Address'].title()
    address = address.split("#")[0]  # Remove the unit number if any
    wait_for_element(By.ID, 'Address').send_keys(address)


    driver.execute_script("arguments[0].scrollIntoView();",wait_for_element(By.ID,'ZipCode'))
    wait_for_element(By.ID,'ZipCode').click()
    wait_for_element(By.ID,'ZipCode').send_keys(data['Zip_code'])



    driver.execute_script("arguments[0].scrollIntoView();", wait_for_element(By.XPATH , '//input[@value="sale"]'))
    if(data['For'].upper() == 'SALE'):
        wait_for_element(By.XPATH , '//input[@value="sale"]').click()
    else:
        wait_for_element(By.XPATH , '//input[@value="sale_pending"]').click()


def fill_price(data):
    driver.execute_script("arguments[0].scrollIntoView();", wait_for_element(By.ID,'Price'))
    wait_for_element(By.ID,'Price').send_keys(data['List'])

def add_photo(data):

    # wait_for_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()

    image = data["images"][0]
    driver.execute_script("arguments[0].scrollIntoView();", wait_for_element(By.ID, 'AddPhotoBtn'))
    wait_for_element(By.ID, 'AddPhotoBtn').click()
    wait_for_element(By.XPATH, '//*[@id="fileupload"]/div[2]/div/span/input').send_keys(image)
    wait_for_element(By.XPATH, '//*[@id="fileupload"]/div[2]/div/button').click()
    upload_wait_driver = WebDriverWait(driver, 120)  # Wait for a maximum of 10 seconds
    upload_wait_driver.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="fileupload_popup_c"]')))

    driver.execute_script("arguments[0].scrollIntoView();", wait_for_element(By.ID, 'AddPhotoBtn'))
    wait_for_element(By.ID, 'AddPhotoBtn').click()
    for image in data["images"][1:]:
        wait_for_element(By.XPATH, '//*[@id="fileupload"]/div[2]/div/span/input').send_keys(image)
        sleep(0.1)

    wait_for_element(By.XPATH, '//*[@id="fileupload"]/div[2]/div/button').click()
    upload_wait_driver = WebDriverWait(driver, 120)  # Wait for a maximum of 10 seconds
    # upload_wait_driver.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="fileupload_popup_c"]')))
    upload_wait_driver.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="fileupload"]/div[2]/div/button/span')))




        
    #wait_for_element(By.XPATH , '//*[@id="fileupload"]/div[2]/div/button').click()
    #wait_for_element(By.XPATH,'//*[@id="fileupload_popup"]/div/div[1]/a').click()


def fill_description(data):


#admin@jackhunter.com

    #description
    driver.execute_script("arguments[0].scrollIntoView();", wait_for_element(By.ID, 'AddPhotoBtn'))
    iframe = wait_for_element(By.ID,'Description_ifr')
    driver.switch_to.frame(iframe)
    sleep(1)
    driver.execute_script("arguments[0].scrollIntoView();", wait_for_element(By.ID ,'tinymce'))
    wait_for_element(By.ID ,'tinymce').click()
    wait_for_element(By.ID ,'tinymce').send_keys(data['Client Remks'] + '\n' + 'Extras : ' + data['Extras'] + '\n' + 'Courtesy of:' + data['office'].upper())
    driver.switch_to.default_content()
    sleep(1)


def building_Type_style(data):
    #building Type style
    selector = wait_for_element(By.ID , 'BuildingDetails_Type')
    driver.execute_script("arguments[0].scrollIntoView();", selector )
    type_selector = Select(selector)
    type_selector.select_by_index(1)

    type_selector = Select(wait_for_element(By.XPATH , '//*[@id="residentialSubTypes"]'))


    for option in type_selector.options:
        # Convert the option value to lowercase or uppercase for comparison
        if option.get_attribute("value").lower() == data['type_style']:
            # Select the option by value
            type_selector.select_by_value(option.get_attribute("value"))
            return
    type_selector.select_by_index(1)


def building_Type(data):
    #building type
    type_selector = Select(wait_for_element(By.ID , 'BuildingDetails_BuildingUnitType'))


    for option in type_selector.options:
        # Convert the option value to lowercase or uppercase for comparison
        if option.get_attribute("value").lower() == data['type_style']:
            # Select the option by value
            type_selector.select_by_value(option.get_attribute("value"))
            return
    type_selector.select_by_index(1)



def fill_bedrooms(data):
    driver.execute_script("arguments[0].scrollIntoView();", wait_for_element(By.ID , 'BuildingDetails_Bedrooms'))
    wait_for_element(By.ID , 'BuildingDetails_Bedrooms').send_keys(eval(data['Bedrooms']))

def fill_bathrooms(data):
    wait_for_element(By.ID , 'BuildingDetails_Bathrooms').click()
    wait_for_element(By.ID , 'BuildingDetails_Bathrooms').send_keys(data['Washrooms'])




def fill_garage(data):
    elem = None

    while not elem:
        elem = wait_for_element(By.NAME, 'BuildingDetails.GarageStalls')
    elem.send_keys(int(float(data['Gar/Gar Spcs'].split("/")[-1])))



def check_list(data):

        check_list = driver.find_elements(By.CLASS_NAME ,"features-checkbox")
        check={}
        for c in check_list:
            driver.execute_script("arguments[0].scrollIntoView();", c)
            check[c.text] = c
            if data['Extras item'] and c.text.lower().strip() in data['Extras item']:
                c.click()



def write_log(log_message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{current_time}] #AutoPost# {str(log_message)}"
        
    log_file = "ErrorLog.log"
    with open(base_dir+"/"+ log_file, 'a') as file:
        file.write(formatted_message + '\n\n\n\n')
    



def run_post(username, password, results):
    global driver
    global wait_driver
    global actions

    driver = init_UC()    
    wait_driver = WebDriverWait(driver, 10)  # Wait for a maximum of 10 seconds
    driver.get('https://www.point2homes.com/Account/AddAListing')
    actions = ActionChains(driver)






    print("Login strt successfully")
    login_action(username , password)
    print("login success")




    i=0
    for data in results:
        try:
            print(data)
            time.sleep(10)

   
            if data["__posted"] == True:
                print("conitnu")
                continue

            driver.get('https://www.point2homes.com/Account/AddAListing')
            time.sleep(10)
            print("listing")

            fill_address(data)
            print("fill_address")
            fill_price(data)
            print("fill_price")
            add_photo(data)
            print("add_photo")
            fill_description(data)
            print("fill_description")
            building_Type_style(data)
            print("building_Type_style")
            building_Type(data)
            print("building_Type")
            fill_bedrooms(data)
            print("fill_bedrooms")
            fill_bathrooms(data)
            print("fill_bathrooms")

            fill_garage(data)
            print("fill_garage")
            check_list(data)
            print("check_list")

            #save
            wait_for_element(By.XPATH,'//*[@id="manuallyInsertedListingForm"]/div[7]/button').click()
            
            #active
            active_wait_driver = WebDriverWait(driver, 300)  # Wait for a maximum of 300 seconds
            active_wait_driver.until(EC.presence_of_element_located((By.CLASS_NAME, 'item-cnt')))
            driver.find_elements(By.CLASS_NAME,'item-cnt')[0].find_element(By.CLASS_NAME,'btn-primary').click()
            wait_for_element(By.XPATH,'//*[@id="btnYes"]').click()

            extra_money_wait_driver = WebDriverWait(driver, 300)  # Wait for a maximum of 300 seconds


            no_money = extra_money_wait_driver.until(EC.presence_of_element_located((By.XPATH, '//*[@id="SelectedPromotion3"]')))
            driver.execute_script("arguments[0].scrollIntoView();", no_money)
            no_money.click()
            extra_money_wait_driver.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content_right_top"]/div[2]/div[4]/input'))).click()

            data["__posted"] = True
            with open(data["__dir"] + "/info", 'wb') as file:
                pickle.dump(data,file)

            print('success : ' + data['Address'])
            i+=1
        except Exception as e:
            write_log("Fail in main while : " + str(e) )
            print('fail')


    success_count = i
    fail_count = len(results) - success_count

    print("success_count===>>", success_count)
    print("fail_count==>", fail_count)
    return success_count, fail_count







# username = "admin@jackhunter.com"
# password = "Trial_123"
# s_count , f_count = run_post(username , password , get_list_to_post())



