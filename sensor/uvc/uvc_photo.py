# -*- coding: utf-8 -*-
# original: https://raw.githubusercontent.com/UedaTakeyuki/slider/master/mh_z19.py
#
# © Takeyuki UEDA 2015 -
import os
import subprocess
import ConfigParser
import datetime
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
# refer http://73spica.tech/blog/requests-insecurerequestwarning-disable/
urllib3.disable_warnings(InsecureRequestWarning)

# Const
configfile = os.path.dirname(os.path.abspath(__file__))+'/uvc_photo.ini'

# setting
settings = {
  "folder": "/tmp/",
  "device": "/dev/video0",
  "delay":  "1",
  "skip":   "20",
  "width":  "320",
  "hight":  "240"
}

# termination type
TERMINATOR_DELETEVALUE_AS_FILE=True

def setconfig(ini):
  global settings

  if "photo" in ini.sections():
    if "folder" in dict(ini.items("photo")).keys() and ini.get("photo","folder"):
      settings["folder"] = ini.get("photo","folder")
    if settings["folder"][-1:] != "/":
      settings["folder"] += "/"
    if not os.path.exists(settings["folder"]):
      os.makedirs(settings["folder"]) # keyword "exist_ok" is for 3 

    if "device" in dict(ini.items("photo")).keys() and ini.get("photo","device"):
      settings["device"] = ini.get("photo","device")
    if "delay"  in dict(ini.items("photo")).keys() and ini.get("photo","delay"):
      settings["delay"] = ini.get("photo","delay")
    if "skip"   in dict(ini.items("photo")).keys() and ini.get("photo","skip"):
      settings["skip"] = ini.get("photo","skip")
    if "width"  in dict(ini.items("photo")).keys() and ini.get("photo","width"):
      settings["width"] = ini.get("photo","width")
    if "hight"  in dict(ini.items("photo")).keys() and ini.get("photo","hight"):
      settings["hight"] = ini.get("photo","hight")

if os.path.exists(configfile):
  ini = ConfigParser.SafeConfigParser()
  ini.read(configfile)
  setconfig(ini)

def take_photo():
  global settings
  now = datetime.datetime.now()
  filepath = "{}{}.jpg".format(settings["folder"],now.strftime("%Y%m%d%H%M%S"))
  if os.path.exists(filepath): # remove if old version exist
    os.remove(filepath)

  command_str = "fswebcam {} -d {} -D {} -S {} -r {}x{}".format(filepath,
                                                                  settings["device"],
                                                                  settings["delay"],
                                                                  settings["skip"],
                                                                  settings["width"],
                                                                  settings["hight"])
  p = subprocess.Popen(command_str, stderr = subprocess.PIPE, shell=True)
  p.wait() # wait for finish.

  if not os.path.exists(filepath): # Camera IO erro
    raise IOError(''.join(p.stderr.readlines()))

  return filepath

def read():
  return {"photo": take_photo()}

def is_photo_source(sensor_handlers):
  return 'TERMINATOR_DELETEVALUE_AS_FILE' in dir(sensor_handlers)

def handle(sensor_handlers, data_name, value):
  print ("start handle")
  if is_photo_source(sensor_handlers):
    files = {'upfile': open(value, 'rb')}
    payload = {'viewid': ini.get("server", "view_id")}
    r = requests.post(ini.get("server", "url"), data=payload, files=files, timeout=10, verify=False)
  print ("end handle")
def terminate(sensor_handlers, data_name, value):
  print ("start terminate")
  if is_photo_source(sensor_handlers):
    os.remove(value)
  print ("end terminate")

if __name__ == '__main__':
  value = read()
  print (value)
