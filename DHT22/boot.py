# This file is executed on every boot (including wake-boot from deepsleep)
import os
import uos, machine

#import webrepl
#webrepl.start()

import gc
# gc.enable() We can enable automatic garbage collection
gc.collect()

# Uncomment the following to run the example on boot
#exec(open('./example.py').read(),globals())