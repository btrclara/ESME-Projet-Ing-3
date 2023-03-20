import network
from secrets import secrets
import time
import upip

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets['ssid'], secrets['pw'])
print(wlan.isconnected())
upip.install('micropython-softspi')
print('ok')