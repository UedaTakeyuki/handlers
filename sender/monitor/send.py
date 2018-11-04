# coding:utf-8 Copy Right Atelier Grenouille © 2018 -
#
import os
import sys
import traceback
import requests
import ConfigParser
import urllib3
from urllib3.exceptions import InsecureRequestWarning
# refer http://73spica.tech/blog/requests-insecurerequestwarning-disable/
urllib3.disable_warnings(InsecureRequestWarning)

# Const
configfile = os.path.dirname(os.path.abspath(__file__))+'/send.ini'

# get settings
ini = ConfigParser.SafeConfigParser()
ini.read(configfile)

def error_report():
  info=sys.exc_info()
  print (traceback.format_exc(info[0]))

def handle(data_source_name, data_name, value):
  global ini
  try:
    r = requests.post(ini.get("server", "url"), 
                      data={'valueid': ini.get("valueid", data_name), 'value': value},
                      timeout=10,
                      verify=False)
  except:
    error_report()
  print r.text
