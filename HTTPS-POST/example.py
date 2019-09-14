from machine import Pin
import machine
import dht 
import json

sensor = dht.DHT22(Pin(14))

def parse(s):
  out = ''
  i = 0
  while(i<len(s)):
    if s[i] == '%':
      h = s[i+1:i+3]
      character = chr(int(h, 16))
      out += character
      i += 2
    else:
      out += s[i]
    i += 1      
  return out
  
def get_params(req):
  req = req.decode('utf-8')
  req = req.split('\r\n')
  
  sparam = req[0].split(' ')

  params = sparam[1][1:]
  if len(params) == 0 or params[0] != '?':
    print("No request parameters")
    return {}
  params = params[1:].split('&')
  parameters = {}
  for param in params:
    k, v = parse(param).split('=')
    parameters[k] = v
  print(parameters)
  return parameters

def get_readings():  
  sensor.measure()
  readings = {
    'temperature' :sensor.temperature(),
    'humidity' : sensor.humidity()
  }
  return json.dumps(readings)

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
      # conn.settimeout(1.0)
      print('Got a connection from %s' % str(addr))
      request = conn.recv(1024)
      conn.settimeout(None)            
      params = get_params(request)
      conn.send('HTTP/1.1 200 OK\n')
      conn.send('Content-Type: text/html\n')
      conn.send('Connection: close\n\n')
      if 'readings' in params:
        conn.sendall(get_readings())
      else:
        conn.sendall(web_page())
      conn.close()
    except OSError as e:
      conn.close()
      print('Connection closed')
main()
# print(get_readings())
