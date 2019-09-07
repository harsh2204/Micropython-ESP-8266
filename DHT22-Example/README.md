# DHT-22 Example

This is a basic example of the popular DHT22 temperature and humidity sensor.

#### Prerequisites

- ESP8266-based board or any micropython compatible board. In this case we will use the NodeMCU V3.
- DHT22 / DHT11
- 10kΩ resistor (usually comes with the DHT22/11 module)
- Breadboard
- Jumper Wires

#### Hookup Guide

![DHT22-Hookup](https://raw.githubusercontent.com/harsh2204/Micropython-ESP-8266/master/DHT22-Example/circuit_diagram.png)

Note that the third pin on DHT22 and DHT11 are NC (No connection). Also R1 is a pull up resistor connected to 3V3 (obviously? [read this for more on pull up resistors](https://learn.sparkfun.com/tutorials/pull-up-resistors/all)). To elaborate on why we must add a pull up resistor, due to the [NTC](http://www.resistorguide.com/ntc-thermistor/) (Negative Thermal Coefficient) Thermistor inside the sensor, we always need some current flowing through the thermistor which means that we need to connect a high value resistor to pass some current through the data line.

While that may have sounded complicated, this is a very simple setup. However, do keep in mind that unlike most Arduino-esque boards, NodeMCU's digital pin number (eg. D5) is not the same as the GPIO pin number which is used by µPython, which is 14 in this case. Refer to [this](https://circuits4you.com/wp-content/uploads/2017/12/nodemcu-pinout.png) pinout diagram for the GPIO pins for their respective digital pins.

### Code

Since this is the first guide in the series, I will try to give a quick overview of µPython. µPython is very similar to Python3 as it was written with the syntactic elegance and zen of python in mind. Therefore, if you have experience coding in python, you can probably skip this guide, read and understand the code without trouble.

#### µPython Crash Course
```python

```