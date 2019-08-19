# Complete project details at https://RandomNerdTutorials.com

from machine import Pin
import machine
import dht 


#sensor = dht.DHT11(Pin(14))
# Complete project details at https://RandomNerdTutorials.com

def get_dht_readings():
  sensor = dht.DHT22(Pin(14))
  sensor.measure()
  readings = {
    'temperature' :sensor.temperature(),
    'humidity' : sensor.humidity()
  }
  return readings

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
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    get_readings = request.find('/readings')
    print('Content = %s' % request)
    if get_readings == 6:
      response = get_dht_readings()
      conn.send('HTTP/1.1 200 OK\n')
      conn.send('Content-Type: application/json\n')
      conn.send('Connection: keep-alive\n\n')
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



