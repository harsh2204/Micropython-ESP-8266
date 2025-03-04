DHT-22 Example

This is a basic example of the popular DHT22 temperature and humidity sensor.

Table of Contents
---
- [Table of Contents](#table-of-contents)
    - [Prerequisites](#prerequisites)
    - [Hookup Guide](#hookup-guide)
  - [Code](#code)
    - [µPython Basics](#%C2%B5python-basics)
    - [`boot.py`](#bootpy)
    - [`example.py`](#examplepy)
---

#### Prerequisites

- ESP8266-based board or any micropython compatible board. In this case we will use the NodeMCU V3.
- DHT22 / DHT11
- 10kΩ resistor (usually comes with the DHT22/11 module)
- Breadboard
- Jumper Wires

#### Hookup Guide

![DHT22-Hookup](https://raw.githubusercontent.com/harsh2204/Micropython-ESP-8266/refs/heads/master/DHT22/circuit_diagram.png)

Note that the third pin on DHT22 and DHT11 are NC (No connection). Also R1 is a pull up resistor connected to 3V3 (obviously? [read this for more on pull up resistors](https://learn.sparkfun.com/tutorials/pull-up-resistors/all)). To elaborate on why we must add a pull up resistor, due to the [NTC](http://www.resistorguide.com/ntc-thermistor/) (Negative Thermal Coefficient) Thermistor inside the sensor, we always need some current flowing through the thermistor which means that we need to connect a high value resistor to pass a tiny amount of current through the data line.

While that may have sounded complicated, this is a very simple setup. However, do keep in mind that unlike most Arduino-esque boards, NodeMCU's digital pin number (eg. D5) is not the same as the GPIO pin number which is used by µPython, which is 14 in this case. Refer to [this](https://circuits4you.com/wp-content/uploads/2017/12/nodemcu-pinout.png) pinout diagram for the GPIO pins for their respective digital pins.

### Code

Since this is the first guide in the series, I will try to give a quick overview of µPython. µPython is very similar to Python3 as it was written with the syntactic elegance and zen of python in mind. Therefore, if you have experience coding in python, you can probably skip this guide, read and understand the code without any trouble.

#### µPython Basics

We will get straight into general board control and GPIO pins, which is mainly what you need for this example. The most important module required for controling the board is the `machine` module. This module holds a whole host of useful methods and classes including `Pin`, `ADC`, etc. There are standar python modules like `sys` and `os` as well which are not used as much as the `machine` module, however you can check what board you're running on by running `sys.platform`. Anyway, back to `machine`:

```python
>>> from machine import Pin
>>> led_pin = Pin(14, Pin.OUT)
>>> led_pin.on()
>>> led_pin.off()
```

The code is quite verbose in terms of the function names and their actualy functionality, which means with most things you can use `dir` on the class/object, and you don't even have to look at documentation. 

We can also read from digital pins by using the `Pin.IN` mode and calling the read function. We can also set a weak pull up/down resistor which uses a high value internal resistor (47k-100k) on the pin. We can read the signal on the pin using the `read` function.

```python
>>> sensor_pin = Pin(14, Pin.IN)
>>> print(sensor_pin.value()) # Returns a 0/1 -> (HIGH/LOW)
```

We can do some more cool things with `Pin.IN` mode like setting up interrupts. However, that is a topic for later.

#### `boot.py`

This file contains code that runs every boot (including wake-boot from deepsleep). This file should only contain code essential for boot up (eg. wifi setup, bootup display, etc). Therefore for the most part, the contents of this file will remain the same after a point.

```python
import os
import uos, machine
```

These modules are mainly used by your ide to get information about your device and get a list of the files on your board.

```python
import gc

#gc.enable() We can enable automatic garbage collection
gc.collect()
```

We run a garbage collection before starting any new programs.

#### `example.py`

```python
from machine import Pin
import dht 
import time
```

The `dht` module is packaged with all the ports of µPython, and while µPy tries to include all the basic modules for common use cases, there times when you have to download and copy modules from the internet or even write your own modules due to the limited maturity of this µPy. We will use the `time` module for setting our sampling rate by delaying the reading timings.

```python
dht_pin = Pin(14) #D5 GPIO 14
refresh_rate = 2  #Seconds (DHT22 maximum sampling rate)

dht_sensor = dht.DHT22(dht_pin)
```

We must instantiate a class from the `dht` module to get the sensor instance which will allow us to make readings. The module supports both DHT11 and 22 sensors, and thus contains two classes `DHT11` and `DHT22` both of which take one input parameter of the `Pin` object.

```python
def get_readings():
  dht_sensor.measure()
  
  temperature = dht_sensor.temperature()
  humidity = dht_sensor.humidity()
  # temperature = temperature * (9/5) + 32.0  #Fahrenheit
 
  return temperature, humidity
```

The `get_readings` function just runs the sequence of commands required for acquiring the temperature and humitidty and returns them. The return type is a tuple, which means we can assign these values to individual variables, this is commonly refered as 'tuple unpacking' or 'multiple assignment'.

```python
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
```

It's a common practice in programming to define a `main` function that defines the overall control flow of your program and is called when running the file. Here, we also use a `try/except` block to handle `KeyboardInterrupt` for when we want to stop the main loop. Note that we convert `int` values to `str` explicitly since µPy does not support implicit string conversion of integers and floats when adding with strings. Also, the `time.sleep` function just pause the code execution for any number of seconds which is passed in as an input parameter. Note that `main` is called at the end of the file which means it will run everytime the file is run.
