import time
import json
import pyautogui
from rdp import get_update
import pyperclip
import PySimpleGUI as pg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

with open('cred.json') as f:
    credentials = json.load(f)

# Use the same user profile as the native Chrome browser
options = webdriver.ChromeOptions()
options.add_argument(r"--start-maximized")
options.add_argument(r"C:\Users\gsingh369\AppData\Local\Google\Chrome\User Data")

# Initialize WebDriver and HPsm plugin
driver = webdriver.Chrome(options=options)
driver.get(credentials["sm9url"])
wait = WebDriverWait(driver, 120)
action_chains = ActionChains(driver)

# Use WebDriverWait to wait for the element to be present before trying to interact with it
email_field_xpath = '/html/body/div[2]/main/div[2]/div/div/div[2]/form/div[1]/div[3]/div/div[2]/span/input'
email_field = wait.until(EC.presence_of_element_located((By.XPATH, email_field_xpath)))
email_field.send_keys(credentials["mailid"])
email_field.send_keys(Keys.RETURN)

# Use WebDriverWait to wait for the element to be present before trying to interact with it
ssopass_field_xpath = '/html/body/div[2]/main/div[2]/div/div/div[2]/form/div[1]/div[4]/div/div[2]/span/input'
ssopass_field = wait.until(EC.presence_of_element_located((By.XPATH, ssopass_field_xpath)))
ssopass_field.send_keys(credentials["ssopass"])
ssopass_field.send_keys(Keys.RETURN)

# Wait for the button to be present on the next page
button_xpath = '/html/body/div[2]/main/div[2]/div/div/div[2]/form/div[2]/div/div[3]/div[2]/div[2]/a'
wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
button = driver.find_element(By.XPATH, button_xpath)
button.click()

time.sleep(2)
pyautogui.press("tab")
time.sleep(1)
pyautogui.press("enter")
time.sleep(1)

import os
os.system("winsechandler.exe")
time.sleep(20)

# wait for the page title to change
wait.until(EC.title_contains("Service Manager AMS"))
pg.popup_timed("You are in SM9", auto_close_duration=5, keep_on_top=True)

# press incident mgmt button
button_xpath = '/html/body/div[2]/div/div[2]/div[1]/div/div/div[4]/div[1]/span'
wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
button = driver.find_element(By.XPATH, button_xpath)
button.click()

# press incident queue button
button_xpath = '/html/body/div[2]/div/div[2]/div[1]/div/div/div[4]/div[2]/div/ul/div/li[1]/div/a'
wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
button = driver.find_element(By.XPATH, button_xpath)
button.click()

time.sleep(10)

pg.popup("Please select a ticket", button_type='OK', keep_on_top=True)
time.sleep(30)
response = pg.popup_yes_no("Done selecting a ticket", keep_on_top=True)

# Handle the user's response appropriately
if response == "Yes":
    pass
elif response == "No":
    time.sleep(20)
else:
    print("Popup was closed without clicking")

def copy_item(key_num, ac=action_chains, driver=driver,):
    
    for _ in range(key_num):
        ac.send_keys(Keys.TAB)
        time.sleep(0.1)

    ac.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    ac.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()

    time.sleep(1)
    copied_text = pyperclip.paste()
    return copied_text

ci_name = copy_item(18)
issue_title = copy_item(14)
issue_desc = {}
for i in issue_title.split(", "):
    if "=" in i:
        key, value = i.split("=", 1)
        issue_desc[key] = value
    else:
        continue

print(ci_name)
print(issue_title)
print(issue_desc)

def if_3par(issue_title):
    if issue_title.startswith("HP_3PAR"):
        return True
    elif 'Fabric Performance' in issue_title or 'Port Health' in issue_title:
        return False

def get_idport(issue_title, issue_desc):   
    is3par = if_3par(issue_title)
    print(is3par)
    if is3par == True:
        print(issue_desc['id'])
        return is3par, issue_desc['id']
    else: 
        print(issue_desc['ObjectKeyValue'])
        return is3par, issue_desc['ObjectKeyValue']

time.sleep(3)
is3par, idport = get_idport(issue_title, issue_desc)

with open("copied_text.txt", "w") as file:
    file.write("Id / Port: " + idport + " , CI: " + ci_name + "\n")

    for _ in range(27):
        action_chains.send_keys(Keys.TAB)
        time.sleep(0.1)
    action_chains.send_keys(Keys.RETURN)

    update_desc = get_update(ci_name, is3par, idport, credentials)

    file.write(update_desc + "\n")

