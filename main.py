from machine import Pin
from time import ticks_ms, ticks_diff

__version__ = "0.0.5"

# Pinout declaration for buttons & Relais
INPUTS = (18,19,20,21)
OUTPUTS= (15,14,13,12)

BTN_DEBOUNCE_MS = 250

# Associate buttons (input) with relais (output) and last state change (ms)
btn_relais = []

def btn_pressed( btn_pin ):
	""" callback: Toggle the ouput when button is pressed """
	for entry in btn_relais: # btn,relay,ticks
		if btn_pin == entry[0]: # Right button
			if ticks_diff( ticks_ms(), entry[2] ) > BTN_DEBOUNCE_MS:
				entry[1].toggle() # toggle relay
				entry[2] = ticks_ms()
				return

print( "Starting main.py" )
print( "version: %s" % __version__ )
if ('wifi_mode' in dir()):
	if wifi_mode == None:
		print("wifi_mode: %s. Exiting main!" % wifi_mode )
		import sys
		sys.exit(0)
else:
	print("wifi_mode not declared in boot.py. Exiting main!" )
	import sys
	sys.exit()


print( "Initializing hardware!")
# Create ressources & attach handler
for i,o in zip(INPUTS,OUTPUTS):
	btn = Pin(i, Pin.IN, Pin.PULL_UP )
	btn.irq( handler=btn_pressed, trigger=Pin.IRQ_FALLING )
	relay = Pin( o, Pin.OUT, value=0)
	btn_relais.append( [btn, relay, ticks_ms()] )

print( "Current Network config" )
import network
sta = network.WLAN( network.STA_IF )
if sta.active():
	print( sta )
ap = network.WLAN( network.AP_IF )
if ap.active():
	print( ap )

print( "Starting WebServer" )
from microWebSrv import MicroWebSrv

# ----------------------------------------------------------------------------

@MicroWebSrv.route('/')
def _httpHandlerIndex(httpClient, httpResponse, args={}) :
	httpResponse.WriteResponsePyHTMLFile('www/index.pyhtml', headers=({'Cache-Control': 'no-cache'}), vars={'__version__':__version__, 'httpClient':httpClient} )

@MicroWebSrv.route('/status')
def _httpHandlerEditWithArgs(httpClient, httpResponse, args={}) :
	global btn_relais
	index_entries = list(enumerate( btn_relais )) # create a zip of (index, [btn, relay, ticks_ms()] )
	httpResponse.WriteResponsePyHTMLFile('www/status.pyhtml', headers=({'Cache-Control': 'no-cache'}),
			vars={'__version__':__version__, 'httpClient':httpClient, 'index_entries':index_entries} )

@MicroWebSrv.route('/status', 'POST')
def _httpHandlerEditWithArgs(httpClient, httpResponse, args={}) :
	global btn_relais

	formData  = httpClient.ReadRequestPostedFormData()
	btn_action = formData["btn_action"]
	print( "Action %s" % btn_action )
	for i in range( 4 ):
		if btn_action == 'ON%i'%(i+1):
			btn_relais[i][1].on()
			break
		if (btn_action == 'OFF%i'%(i+1)) or (btn_action == 'ALL_OFF'):
			btn_relais[i][1].off()

	# Redraw the screen
	index_entries = list(enumerate( btn_relais )) # create a zip of (index, [btn, relay, ticks_ms()] )
	httpResponse.WriteResponsePyHTMLFile('www/status.pyhtml', headers=({'Cache-Control': 'no-cache'}),
			vars={'__version__':__version__, 'httpClient':httpClient, 'index_entries':index_entries} )

@MicroWebSrv.route('/api/status')
@MicroWebSrv.route('/api/status/<relay>')
def _httpHandlerEditWithArgs(httpClient, httpResponse, args={}) :
	global btn_relais

	relais = {}
	if 'relay' in args:
		try:
			idx = int( args['relay'] )
		except:
			idx = -1
		if 1<=idx<=4:
			relais[ str(idx) ] = btn_relais[idx-1][1].value()
		else:
			return httpResponse.WriteResponseJSONError( 400, "400: invalid #relay" )
	else:
		# all the relay
		for i in range( 4 ):
			relais[ str(i+1) ]= btn_relais[i][1].value()
	# btn_relais[i][1].on()
	#	if (btn_action == 'OFF%i'%(i+1)) or (btn_action == 'ALL_OFF'):
	httpResponse.WriteResponseJSONOk( obj=relais, headers=({'Cache-Control': 'no-cache'}) )

@MicroWebSrv.route('/api/relay/all/<value>')
def _httpHandlerEditWithArgs(httpClient, httpResponse, args={}) :
	global btn_relais

	try:
		val = int( args['value'] )
	except:
		val = -1
	if not( 0<=val<=1 ):
		return httpResponse.WriteResponseJSONError( 400, "400: invalid value" )

	for i in range(4):
		btn_relais[i][1].value( val )
	httpResponse.WriteResponseJSONOk( obj=1, headers=({'Cache-Control': 'no-cache'}) )

@MicroWebSrv.route('/api/relay/<index>/<value>')
def _httpHandlerEditWithArgs(httpClient, httpResponse, args={}) :
	global btn_relais

	try:
		idx = int( args['index'] )
	except:
		idx = -1
	if not( 1<=idx<=4 ):
		return httpResponse.WriteResponseJSONError( 400, "400: invalid #relay" )
	try:
		val = int( args['value'] )
	except:
		val = -1
	if not( 0<=val<=1 ):
		return httpResponse.WriteResponseJSONError( 400, "400: invalid value" )

	btn_relais[idx-1][1].value( val )
	httpResponse.WriteResponseJSONOk( obj=1, headers=({'Cache-Control': 'no-cache'}) )



# ----------------------------------------------------------------------------

srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= False
#srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start()
