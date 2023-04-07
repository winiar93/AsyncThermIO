import dht
from micropython import const
from machine import Pin, I2C, Signal
from s2pico_oled import OLED
import time
import uasyncio
from utils import connect_wifi, send_data_payload_sync

# Pin Assignments
# SPI
SPI_MOSI = const(35)
SPI_MISO = const(36)
SPI_CLK = const(37)

# I2C
I2C_SDA = const(8)
I2C_SCL = const(9)

# DAC
DAC1 = const(17)
DAC2 = const(18)

# LED
LED = const(10)

# OLED
OLED_RST = const(18)

# BUTTON
BUTTON = const(0)


#led = Signal(LED, Pin.OUT, value=0, invert=True)
button = Pin(BUTTON, Pin.IN, Pin.PULL_UP)
sensor_instance = dht.DHT22(Pin(21))

i2c = I2C(0)
oled = OLED(i2c, Pin(OLED_RST))

def handle_oled_event(message, pos_x, pos_y, on_screen_time) -> None:
    oled.fill(0)
    oled.text(message, pos_x, pos_y, 1)
    oled.show()
    time.sleep(on_screen_time)
    
    
handle_oled_event('Hello my friend !', 5, 17, 2)

wifi_connection_status = connect_wifi()
if wifi_connection_status:
    handle_oled_event('Wifi connected', 0, 17, 2)
else:
    oled.fill(0)
    handle_oled_event('No wifi connection', 0, 17, 2)


def get_measurements(d)-> Tuple[int, int]:
    for _ in range(5):
        try:
            d.measure()
            temp = d.temperature()
            hum = d.humidity()
            if temp != 0 and hum !=0:
                break
        except Exception as e:
            print(e)
        
    return temp, hum


async def http_post_coroutine() -> None:
    delay_s = 180
    while True:
        sensor_temperature, sensor_humidity = get_measurements(sensor_instance)
        payload = {'field1': round(sensor_temperature, 2),'field2': int(sensor_humidity)}
        respone_status_code = send_data_payload_sync(payload=payload)
        if respone_status_code == 200:
            print(f'Payload sended, status: {respone_status_code}')
        else:
            print('Sending payload failed')
        await uasyncio.sleep(delay_s)
        
       
async def main():
    uasyncio.create_task(http_post_coroutine())
    while True:
        try:
            if button.value() == 0:
                handle_oled_event('Button press detected!', 0, 17, 2)
                break
            oled.fill(0)
            sensor_temperature, sensor_humidity = get_measurements(sensor_instance)
            oled.text(f'Temperature {sensor_temperature}', 0, 5, 1)
            oled.text(f'Humidity {sensor_humidity}', 0, 18, 1)
            oled.show()
            await uasyncio.sleep(1)
        except:
            pass
    
    handle_oled_event('Forced script termination !', 0, 17, 2)

uasyncio.run(main())