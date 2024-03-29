from machine import Pin
import machine
import dht

dht_pin = Pin(14)  # D5 GPIO 14


def get_readings():
    readings = {}
    dht_sensor = dht.DHT22(dht_pin)
    dht_sensor.measure()
    return """<!doctype html><html><head> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"> <meta http-equiv="refresh" content="1"> <link rel="icon" href="data:,"> <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"> <style>#temp-sense{margin: auto; width: 30% !important;}body{background-color: darkslateblue}</style> </head> <body> <div id='temp-sense' class="container-fluid"> <h3 style="color: white">Temperature Sensor</h3> <table class="table table-bordered table-dark table-hover text-center"> <thead class="thead-dark"> <tr> <th scope="col">MEASUREMENT</th> <th scope="col">VALUE</th> </tr></thead> <tbody> <tr><td>Temp. Celsius</td><td><span>"""
    + '{0:3.1f}'.format(dht_sensor.temperature()) + """ C</span></td></tr><tr><td>Humidity</td><td><span>"""
    + str(dht_sensor.humidity()) + """%</span></td></tr> </tbody> </table> </div><script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script> <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script> <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script> </body> </html>"""



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
            request = str(request)
            print('Content = %s' % request)
            response = get_readings()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
        except OSError as e:
            conn.close()
            print('Connection closed')


main()
# print(get_readings())
