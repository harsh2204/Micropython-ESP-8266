from machine import Pin
import machine
import dht 
import ujson
import urequests

def get_readings():
  sensor = dht.DHT22(Pin(14)) #D5
  sensor.measure()
  readings = {
    "temperature" :sensor.temperature(),
    "humidity" : sensor.humidity(),
    "rain": 0,        #TODO Implement
    "soil": 99.2,     #TODO Implement
    "sunlight": 33.3  #TODO Implement
  }
  # Data logging to google drive.
  # The IFTTT key is stored in a file named 'key'   
  url = f"https://maker.ifttt.com/trigger/tree-readings/with/key/{open('key', 'r').read().strip()}"
  headers = {'Content-Type': 'application/json'}
  data = {'value1' : ' ||| '.join([str(x) for x in readings.values()])}
  r = urequests.post(url, data=ujson.dumps(data), headers=headers)
  return ujson.dumps(readings) #important to encode the data before sending it.

def web_page():
  f = open('index.html')
  html = f.read()
  f.close()
  return html

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
    get_readings = request.find('/readings')
    print('Content = %s' % request)
    if get_readings == 6:
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
