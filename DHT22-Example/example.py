from machine import Pin
import dht 
import time

dht_pin = Pin(14) #D5 GPIO 14
refresh_rate = 2  #Seconds (DHT22 maximum sampling rate)

dht_sensor = dht.DHT22(dht_pin)

def get_readings():
  dht_sensor.measure()
  
  temperature = dht_sensor.temperature()
  humidity = dht_sensor.humidity()
  # temperature = temperature * (9/5) + 32.0  #Fahrenheit
 
  return temperature, humidity


def main():
  print('Checking temperature every ' + str(refresh_rate) + 'seconds')
  while True:
    try:
      temp, hum = get_readings()
      print("Temperature " + str(temp) + "°C  |  Humidity " + str(hum) + "%")
      time.sleep(refresh_rate)
    except KeyboardInterrupt:
      break

main()