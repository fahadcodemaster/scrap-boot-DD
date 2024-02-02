from flask import Flask, render_template, request
import datetime
import pickle
import time

import undetected_chromedriver as uc
from time import sleep


# import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from random import randint
from selenium import webdriver

import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

base_dir = os.path.dirname(os.path.realpath(__file__))

print(base_dir)
style_conf = {
    'Condominium': os.getenv('Condominium'),
    'Co_op': os.getenv('Co_op'),
    'Duplex': os.getenv('Duplex'),
    'Farm_and_Ranch': os.getenv('Farm_and_Ranch'),
    'House': os.getenv('House'),
    'Lots_and_Land': os.getenv('Lots_and_Land'),
    'Mobile_Manufactured_Modular_House': os.getenv('Mobile_Manufactured_Modular_House'),
    'Multi_Family': os.getenv('Multi_Family'),
    'Recreational_Cabin_Timeshare_etc': os.getenv('Recreational_Cabin_Timeshare_etc'),
    'Single_Family': os.getenv('Single_Family'),
    'Townhouse': os.getenv('Townhouse'),
    'Triplex': os.getenv('Triplex'),
    'Apartment': os.getenv('Apartment'),
}


def init_UC():
    chrome_options = uc.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1200x600')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-setuid-sandbox')

    user_directory_path = base_dir + '/profile'
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
    driver = uc.Chrome(executable_path=os.path.join(base_dir, 'chromedriver.exe'), options=chrome_options, headers=headers)
    return driver





driver = None
wait_driver = None
driver_action = None


def wait_for_element(by, selector) -> WebElement:
    sleep(1)
    try:
        return wait_driver.until(EC.presence_of_element_located((by, selector)))
    except Exception as e:
        return False





def login_action(username, password):
    wait_for_element(By.ID, 'Username').clear()
    wait_for_element(By.ID, 'Username').click()

    wait_for_element(By.ID, 'Username').send_keys(username)
    wait_for_element(By.ID, 'Password').click()
    wait_for_element(By.ID, 'Password').clear()
    wait_for_element(By.ID, 'Password').send_keys(password)
    wait_for_element(By.XPATH, '//*[@id="login_form"]/div/div[1]/fieldset/p[3]/button').click()
    wait_for_element(By.CLASS_NAME, 'user-profile-name')  # wait to login


def DelfromArhice():
    archive_tab = wait_for_element(By.XPATH, '//*[@id="Archived"]/a')
    archive_tab.click()
    time.sleep(4)
    delete = wait_for_element(By.XPATH, '//a[contains(text(), "Delete")]')


    delete.click()
    time.sleep(1)

    del_yes = wait_for_element(By.XPATH, '//*[@id="btnYes"]')
    del_yes.click()


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('active_draft.html')

@app.route('/run_post', methods=['POST'])
def run_post():
    username = "admin@jackhunter.com"
    password = "Trial_123"
    global driver
    global wait_driver
    global actions

    driver = init_UC()
    wait_driver = WebDriverWait(driver, 10)  # Wait for a maximum of 10 seconds
    driver.get('https://www.point2homes.com/Account/AddAListing')
    actions = ActionChains(driver)

    # print("Login strt successfully")
    login_action(username, password)
    print("login success")
    time.sleep(4)

    i = 1

    while True:
        print(f"iteration no {i}")
        driver.get("https://www.point2homes.com/Account/MyListings?Tab=Draft&page=1")
        time.sleep(10)
        try:
            active = driver.find_element(By.XPATH, '//*[@class="btn-primary"]')
            active.click()
            print("click")
            time.sleep(2)

            active_now = driver.find_element(By.XPATH, '//*[@id="btnYes"]')
            # print(active_now)
            active_now.click()
            time.sleep(20)
            i += 1
        except:
            break


    driver.quit()


    return '''
        <script>
            alert("Active all draft listing.");
            window.location.href = "/"; // Redirect back to the form
        </script>
        '''

if __name__ == '__main__':
    app.run()
