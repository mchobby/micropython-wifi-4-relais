#
# Just activates the relay while the corresponing button is pressed down
#
from machine import Pin
import time
led = Pin( "LED", Pin.OUT )

# Pinout declaration for buttons & Relais
INPUTS = (18,19,20,21)
OUTPUTS= (15,14,13,12)

lst = []
for i,o in zip(INPUTS,OUTPUTS):
	lst.append( (Pin(i,Pin.IN, Pin.PULL_UP), Pin(o,Pin.OUT)) )
while True:
	for i,o in lst:
		# Set output to True when button is pressed
		o.value( not(i.value()) )
	led.toggle()
	time.sleep_ms(200)
