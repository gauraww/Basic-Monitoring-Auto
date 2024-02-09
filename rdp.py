import time
import pyautogui
import PySimpleGUI
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


def get_jserver(ci_name):
    if ci_name.contains("frg") or ci_name.contains("ida"):
        return jservers[0]
    elif ci_name.contains("deg") or ci_name.contains("edc"):
        return jservers[0]
    elif ci_name.contains("acr") or ci_name.contains("crd"):
        return jservers[0]
    elif ci_name.contains("dxs") or ci_name.contains("wyn"):
        return jservers[3]

def run_commands(commands):
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

    jserver = get_jserver(ci_name)

    # Input credentials and connect
    pyautogui.typewrite(jserver)
    pyautogui.press("enter")
    time.sleep(4)
    pyautogui.typewrite(credentials["password"])
    pyautogui.press("enter")
    time.sleep(15)
    pyautogui.press("enter")
    time.sleep(15)
    pyautogui.click(x=300, y=300)

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
    time.sleep()

    # Login to second remote desktop with credentials
    while True:
        time.sleep(1)  # Adjust the sleep time as needed
        screen = pyautogui.screenshot()
        if "login as:" in pyautogui.image_to_string(screen):
            break

    pyautogui.typewrite("gsingh369")
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.write("Lenovo@26129282")
    pyautogui.press("enter")

    # Wait for Putty to load
    while True:
        time.sleep(1)  # Adjust the sleep time as needed
        screen = pyautogui.screenshot()
        if f":{credentials["username"]}>" in pyautogui.image_to_string(screen):
            break

    if is3par == True:
        run_commands(threepar_cmds)
    elif is3par == False:
        run_commands(switch_cmds)
    else: 
        PySimpleGUI.popup_auto_close("NOT a Valid CI. Program Terminated", auto_close_duration=10)
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
    time.sleep(3)

    pyautogui.click(x=1400, y=850)
    return clipboard_content
