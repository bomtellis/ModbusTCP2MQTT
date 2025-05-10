#!/usr/bin/env python3

from pymodbus.client import ModbusTcpClient
import paho.mqtt.publish as mqtt
import schedule, time
import json

# Load configuration from json file
try:
    with open("config.json") as f:
        config_raw = f.read()
        config = json.loads(config_raw)
except FileNotFoundError as e:
    print("error", e)


# Modbus is offset by 1. 100 = register 101 on schneider
def startTask():
    msgs = []
    # Loop thru msgs in config
    for item in config["msgs"]:
        # print(item)
        modbus = item["modbus"]

        # Get the modbus value and store it in the result key

        # Setup client from values in msg
        client = ModbusTcpClient(modbus["ip"])
        match modbus["type"]:
            case "coil":
                result = client.read_coils(
                    address=modbus["register_address"],
                    count=modbus["count"],
                    slave=modbus["slave"],
                )
                modbus["result"] = (
                    "on" if result.bits[0] else "off"
                )  # Read the first bit as this corresponds with the selected register

                msgs.append(
                    {
                        "topic": item["topic"],
                        "payload": modbus["result"],
                        "qos": 1,
                        "retain": config["retain"],
                    }
                )
            case _:
                print("Case not found")
        client.close()

    mqtt.multiple(
        msgs,
        config["hostname"],
        config["port"],
        auth=config["auth"],
        tls=config["tls"],
    )


schedule.every(config["runtime"]).seconds.do(startTask)

# Loop task every 5 seconds
# Look thru modbus results then publish to mqtt

if __name__ == "__main__":
    try:
        print("Running Modbus 2 MQTT Bridge")
        print(f"Update frequency: {config['runtime']} seconds")
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        t = 1
