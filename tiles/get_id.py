import win32process
import wmi
import win32gui

c = wmi.WMI()

import configparser
import json

import os.path
path1 = R"%USERPROFILE%\Desktop\repo\codes.ini"
path2 = R"%USERPROFILE%\AppData\Local\apploggingservice\app_events.json"

def get_app_path(hwnd):
    """Get applicatin path given hwnd."""
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in c.query('SELECT ExecutablePath FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
            exe = p.ExecutablePath
            break
    except:
        return None
    else:
        return exe

def get_target_window(wintext):
    if wintext == "":
        win2find = input('enter name of window to find')
        whnd = win32gui.FindWindowEx(None, None, None, str(win2find))
    else:
        win2find = wintext
        whnd = win32gui.FindWindowEx(None, None, None, str(wintext))
    whnd = win32gui.FindWindowEx(None, None, None, win2find)
    if not (whnd == 0):
        return whnd

def update_get_id(app, get_id, handle):
    dictionary = {
        "app": app,
        "active": get_id,
        "handle": handle,
        }
    json_object = json.dumps(dictionary, indent=4)
    with open(os.path.expandvars(path2), "w") as outfile:
        outfile.write(json_object)
    outfile.close()
    
while True:
    get_id = False
    config = configparser.ConfigParser()
    config.read(os.path.expandvars(path1))
    wintext = config['app']['App']
    window = win32gui.GetForegroundWindow()
    #print(wintext)
    hwnd = get_target_window(wintext)
    if window == hwnd:
        get_id = True
    else:
        get_id = False
    #print(hwnd)
    epath = get_app_path(hwnd)
    update_get_id(wintext, get_id, hwnd)
