import time
import pyautogui
import datetime
import pyperclip

jservers = [
    "frg-wjump.frg.mcloud.entsvcs.com",
    "deg-wjump.deg.mcloud.entsvcs.com",
    "acr-wjump.acr.mcloud.entsvcs.com",
    "wyn-wjump.wyn.mcloud.entsvcs.com",
]

switch_cmds = [
    "portshow",
    "sfpshow",
    "porterrshow",
]

threepar_cmds = [
    "showalert",
    "showalert -f",
]


def get_jserver(ci_name, jservers):
    print(ci_name)
    if "frg" in ci_name or "ida" in ci_name:
        return jservers[0]
    elif "edc" in ci_name or "deg" in ci_name:
        return jservers[1]
    elif "acr" in ci_name or "crd" in ci_name:
        return jservers[2]
    elif "wyn" in ci_name or "dxs" in ci_name:
        return jservers[3]

def run_commands(commands, idport):
    if commands == switch_cmds:
        for command in commands:
            pyautogui.write(f'{command} {idport}', interval=0.05)
            pyautogui.press("enter")
            time.sleep(5)
    else:
        for command in commands:
            pyautogui.write(command, interval=0.05)
            pyautogui.press("enter")
            time.sleep(5)

def get_update(ci_name, is3par, idport, credentials):
    # Open Remote Desktop Connection app
    pyautogui.hotkey("win", "r")
    time.sleep(1)
    pyautogui.typewrite("mstsc")
    pyautogui.press("enter")
    time.sleep(2)

    # Input credentials and connect
    js_name = get_jserver(ci_name, jservers)
    pyautogui.typewrite(js_name)
    print(js_name)
    pyautogui.press("enter")
    time.sleep(5)
    pyautogui.typewrite(credentials["password"])
    pyautogui.press("enter")
    time.sleep(20)
    pyautogui.press("enter")
    time.sleep(15)
    pyautogui.click(x=400, y=400)

    # Open Putty
    pyautogui.hotkey("win", "r")
    time.sleep(1)
    pyautogui.typewrite("putty")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(2)

    # Input system name for switch
    pyautogui.typewrite(ci_name)
    pyautogui.press("enter")
    time.sleep(10)

    # Login to second remote desktop with credentials
    # while True:
    #     screen_width, screen_height = pyautogui.size()
    #     screen = pyautogui.screenshot()
    #     if "login as:" in pyautogui.locateOnScreen(screen,minSearchTime=2,region=['0','0',screen_width/2,screen_height/2 ]):
    #         break
    

    pyautogui.typewrite(credentials["username"], interval=0.1)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.typewrite(credentials["password"], interval=0.3)
    pyautogui.press("enter")
    time.sleep(15)

    # # Wait for Putty to load
    # while True:
    #     screen_width, screen_height = pyautogui.size()
    #     screen = pyautogui.screenshot()
    #     if f":{credentials['username']}>" in pyautogui.locateOnScreen(screen,minSearchTime=2,region=['0','0',screen_width/2,screen_height/2 ]):
    #         break
        
    if is3par == True:
        run_commands(threepar_cmds, idport)
    elif is3par == False:
        run_commands(switch_cmds, idport)
    else: 
        pyautogui.alert(text='', title='Not a Valid CI. Program Terminated', button='OK')
        SystemExit

    # Copy output and paste in notepad file
    pyautogui.hotkey("winleft", "left")
    time.sleep(1)
    pyautogui.rightClick(x=11, y=11)
    time.sleep(1)

    for _ in range(13):
        pyautogui.press("down")
    pyautogui.press("enter")
    time.sleep(2)

    # Capture clipboard content before closing Putty and RDP window
    clipboard_content = pyperclip.paste()

    # Close Putty and Remote Desktop Connection
    pyautogui.hotkey("alt", "f4")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.hotkey("alt", "f4")
    time.sleep(5)

    pyautogui.click(x=1400, y=850)
    return clipboard_content