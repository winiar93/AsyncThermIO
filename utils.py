import network
import urequests as requests
import time
import uasyncio
    
WIFI_SSID = '****'
WIFI_PASS = '****'
HTTP_HEADERS = {'Content-Type': 'application/json'}
THINGSPEAK_WRITE_API_KEY = 'example_api_key'

def connect_wifi() -> bool:
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASS)
    
    print(f'Wifi connection status {sta_if.isconnected()}')
    return sta_if.active()
    
def send_data_payload_sync(payload) -> int:
    try:
        r = requests.post('http://api.thingspeak.com/update?api_key=' + THINGSPEAK_WRITE_API_KEY, json=payload, headers=HTTP_HEADERS)
        r.close()
        return r.status_code
        
    except Exception as e:
        print(e)

        
    
    

