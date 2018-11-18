import os
import sys
import traceback
import requests
import ConfigParser
import subprocess
from incremental_counter import Counter
from m2x.client import M2XClient

# Const
configfile = os.path.dirname(os.path.abspath(__file__))+'/send2m2x.ini'

# get settings
ini = ConfigParser.SafeConfigParser()
ini.read(configfile)

# https://code.i-harness.com/en/q/aea99
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

er_on = str2bool(ini.get("error_recovery", "recover_on")) # error_recovery

# error_counter
if er_on:
  c = Counter(ini.get("error_recovery", "counterfile"))

def reset_device():
  global ini
  subprocess.Popen(ini.get("error_recovery", "recover_command"), shell=True)

def inc_network_ioerror():
  global c, ini
  if c.inc() >= int(ini.get("error_recovery", "threshold")):
    reset_device()

def reset_network_ioerror():
  global c, ini
  c.reset()

def error_report():
  info=sys.exc_info()
  print (traceback.format_exc(info[0]))

def handle(data_source_name, data_name, value):
  global ini
  try:
    stream_id = ini.get("stream",data_name)
    if stream_id is not None:
      client_id = ini.get("client","key")
      device_id = ini.get("device","key")
      if client_id is not None and client_id is not None:
        client = M2XClient(key=client_id)
        device = client.device(device_id)
        stream = device.stream(stream_id)
        print (stream.add_value(value))
        if er_on:
          reset_network_ioerror()
  except requests.ConnectionError as e:
    error_report()
    if er_on:
      inc_network_ioerror()
  except:
    error_report()
    if er_on:
      reset_network_ioerror()
