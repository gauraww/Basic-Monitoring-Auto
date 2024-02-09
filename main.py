import time
import subprocess
import pyperclip
import PySimpleGUI as pg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# Replace with your SM9 login details
username = "gsingh369"
mailid = "gaurav.singh9@dxc.com"
ssopass = "Kiran@26129282"
password = "Iphone@26129282"
sm9url = "https://am.svcs.entsvcs.net/sm/index.do"

# Use the same user profile as the native Chrome browser
options = webdriver.ChromeOptions()
options.add_argument(r"C:\Users\gsingh369\AppData\Local\Google\Chrome\User Data")

# Initialize WebDriver and HPsm plugin
driver = webdriver.Chrome(options=options)
driver.get(sm9url)
wait = WebDriverWait(driver, 120)
action_chains = ActionChains(driver)

# Use WebDriverWait to wait for the element to be present before trying to interact with it
email_field_xpath = '/html/body/div[2]/main/div[2]/div/div/div[2]/form/div[1]/div[3]/div/div[2]/span/input'
email_field = wait.until(EC.presence_of_element_located((By.XPATH, email_field_xpath)))
email_field.send_keys(mailid)
email_field.send_keys(Keys.RETURN)

# Use WebDriverWait to wait for the element to be present before trying to interact with it
ssopass_field_xpath = '/html/body/div[2]/main/div[2]/div/div/div[2]/form/div[1]/div[4]/div/div[2]/span/input'
ssopass_field = wait.until(EC.presence_of_element_located((By.XPATH, ssopass_field_xpath)))
ssopass_field.send_keys(ssopass)
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
iss_title = copy_item(14).split(",")
issue_desc = {}
for i in iss_title:
    if "=" in i:
        key, value = i.split("=")
        issue_desc[key] = value
    else:
        continue

with open("copied_text.txt", "w") as file:
    file.write(ci_name + "\n")
    for key, value in issue_desc.items():
        file.write(f"{key}: {value}\n")

for _ in range(24):
    action_chains.send_keys(Keys.TAB)
    time.sleep(0.1)
action_chains.send_keys(Keys.RETURN)

# Close the browser
driver.quit()

