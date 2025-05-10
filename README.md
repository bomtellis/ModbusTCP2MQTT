# Modbus 2 MQTT Bridge

## Configuration
Look at config.json to add in coils to be read on the modbus.

Supply the IP address/hostname, register number, device_id and type

Only coils supported currently.

## WIP
Support for uint16, uint32

## Installation
Install python 3 and run this
`pip install pymodbus paho-mqtt schedule`

then `python app.py`