import socket
  
import network 
import esp
import gc

esp.osdebug(None)
gc.collect()

ssid = 'K61_4149'
password = 'brian1001'
 
station = network.WLAN(network.STA_IF)
 
station.active(True)
station.connect(ssid, password)
 
while station.isconnected() == False:
    pass
 
print('Connection successful')
print(station.ifconfig())
