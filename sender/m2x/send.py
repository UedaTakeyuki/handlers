import os
import sys
import traceback
import ConfigParser
from m2x.client import M2XClient

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
	stream_id = ini.get("stream",data_name)
	if stream_id is not None:
		client_id = ini.get("client","key")
		device_id = ini.get("device","key")
		if client_id is not None and client_id is not None:
			client = M2XClient(key=client_id)
			device = client.device(device_id)
			stream = device.stream(stream_id)
			print (stream.add_value(value))
