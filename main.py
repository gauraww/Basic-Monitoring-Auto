import time
import json
import rdp
import pyperclip
import PySimpleGUI as pg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

with open('credentials.json') as f:
    credentials = json.load(f)

# Use the same user profile as the native Chrome browser
options = webdriver.ChromeOptions()
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
time.sleep(25)

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
for i in issue_title.split(","):
    if "=" in i:
        key, value = i.split("=")
        issue_desc[key] = value
    else:
        continue

is3par = None

def if_3par(issue_title):
    if issue_title.contains('HP_3PAR'):
        is3par = True
        return True
    elif issue_title.contains('Fabric Performance') or issue_title.contains('Port Health'):
        is3par = False
        return False

def get_idport(issue_title):   
    if if_3par() == True:
        return issue_desc["id"]
    else: return issue_desc["ObjectKeyValue"]
    
idport = get_idport(issue_title)

with open("copied_text.txt", "w") as file:
    file.write("Id / Port: " + idport + " , CI: " + ci_name + "\n")
    file.close()

for _ in range(27):
    action_chains.send_keys(Keys.TAB)
    time.sleep(0.1)
action_chains.send_keys(Keys.RETURN)

update_desc = rdp.get_update(ci_name, is3par, idport, credentials)


