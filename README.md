# AsyncThermIO
An IoT-based temperature monitoring solution using DHT22 sensor for data collection using asynchronous programming.

## Project details

This project is based on Pico S2 device that runs micropython in version v1.19.1 - firmware available [HERE](https://micropython.org/download/LOLIN_S2_PICO/)

The sensor used to collect temperature and humidity is DHT22.

The script is running in an event loop and sensor data are collectedevery second and showing output on oled screen but at the same time there is a task that sends data to ThingSpeak cloud every 5min.
