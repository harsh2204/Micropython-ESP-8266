# This file is executed on every boot (including wake-boot from deepsleep)
import os
import uos, machine

#import esp
#esp.osdebug(None)

#import webrepl
#webrepl.start()

import gc
gc.collect()

# Uncomment the following to run the example on boot
#exec(open('./example.py').read(),globals())