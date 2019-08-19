# This file is executed on every boot (including wake-boot from deepsleep)
import os
import uos, machine
from machine import Pin

import network
import dht


try:
  import usocket as socket
except:
  import socket


#import esp

#esp.osdebug(None)


#uos.dupterm(None, 1) # disable REPL on UART(0)

import gc

#import webrepl

#webrepl.start()

gc.collect()


ssid = '[NETWORK-SSID]'
password = '[NETWORK-PASS]'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())


exec(open('./example.py').read(),globals())
#sensor = dht.DHT22(Pin(14))
#sensor = dht.DHT11(Pin(14))

