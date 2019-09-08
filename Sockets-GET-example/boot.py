# This file is executed on every boot (including wake-boot from deepsleep)
import os
import uos, machine
import network

try:
  import usocket as socket
except:
  import socket



import gc
gc.collect()


ssid = '[NETWORK-SSID]'
password = '[NETWORK-PASS]'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print("Connect @ "+station.ifconfig()[0])

# Uncomment the following to run webserver on boot
#exec(open('./example.py').read(),globals())

