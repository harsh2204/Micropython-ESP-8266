import time
from machine import Pin
import machine
import dht 
import ujson
import urequests


dht_pin = Pin(14) #D5 GPIO 14
rain_pin = 12     #D6 GPIO 12
sun_pin = 2       #D4 GPIO 2
soil_pin = 4      #D2 GPIO 4

class analogMux(object):
    def __init__(self, digital_pin, analog_pin=0, warmup_time=50):
      self.dpin = Pin(digital_pin, Pin.OUT)
      self.dpin.off()
      self.apin = machine.ADC(analog_pin)
      self.warmup_time = warmup_time
    def __enter__(self):
        self.dpin.on()
        time.sleep_ms(self.warmup_time)
        return self.apin
    def __exit__(self, *args):        
        self.dpin.off()

# Courtesy https://www.raspberrypi.org/forums/viewtopic.php?t=149371
def valmap(value, istart, istop, ostart, ostop):
  return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
  
def get_readings(data_log=False):
  readings = {}
  dht_sensor = dht.DHT22(dht_pin)
  dht_sensor.measure()
  
  readings["temperature"] = dht_sensor.temperature()
  readings["humidity"] = dht_sensor.humidity()
  
  # Reading analog values sequentially since there is only one analog pin on our board

  with analogMux(rain_pin) as p:
    readings["rain"] = round(valmap(p.read(), 930, 50, 0, 100))
    
  with analogMux(sun_pin) as p:   
    readings["sunlight"] = round(valmap(p.read(), 0, 1024, 0, 100))
  
  with analogMux(soil_pin) as p:       
    readings["soil"] = round(valmap(p.read(), 0, 1024, 0, 100))
  
  # Data logging to google drive.
  # The IFTTT key is stored in a file named 'key.ini'   
  if (data_log):
    url = "https://maker.ifttt.com/trigger/tree-readings/with/key/"+ open('key.ini', 'r').read().strip()
    headers = {'Content-Type': 'application/json'}
    data = {'value1' : ' ||| '.join([str(x) for x in readings.values()])}
    urequests.post(url, data=ujson.dumps(data), headers=headers)
  
  return ujson.dumps(readings) #important to encode the data before sending it.

def web_page():
  f = open('index.html')
  html = f.read()
  f.close()
  return html


def main():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', 80))
  s.listen(5)
  while True:
    try:
      if gc.mem_free() < 102000:
        gc.collect()
      conn, addr = s.accept()
      #conn.settimeout(1.0)
      print('Got a connection from %s' % str(addr))
      request = conn.recv(1024)
      conn.settimeout(None)
      request = str(request)
      readings = request.find('/readings')
      print('Content = %s' % request)
      if readings== 6:        
        response = get_readings()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: application/json\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
      else:
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
      conn.close()
    except OSError as e:
      conn.close()
      print('Connection closed')
      
main()
#print(get_readings())