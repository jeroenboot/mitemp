#!/usr/bin/python3
from mitemp.mitemp_bt.mitemp_bt_poller import MiTempBtPoller
from mitemp.mitemp_bt.mitemp_bt_poller import MI_TEMPERATURE, MI_HUMIDITY, MI_BATTERY
from btlewrap.bluepy import BluepyBackend
from bluepy.btle import BTLEException
import traceback
import configparser
import os
import json
import datetime

from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

workdir = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read("{0}/devices.ini".format(workdir))
devices = config.sections()



#INFLUXDB
url = "https://westeurope-1.azure.cloud2.influxdata.com"
token = "FS8hSyUmBlhOuQOpZVFqfs5dnFDEOBmUFoZLsQ1K296U55Xf9gJhVT1cXPA1G-83x4074S5QpoeLgroWKtlQ4g=="
org = "1f225e11cad1e4dd"
bucket = "a0e36d09e3bacaa3"
client = InfluxDBClient(url=url, token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)



for device in devices:

    mac = config[device].get("device_mac")
    poller = MiTempBtPoller(mac, BluepyBackend, ble_timeout=config[device].getint("timeout", 10))

    try:
        temperature = poller.parameter_value(MI_TEMPERATURE)
        humidity = poller.parameter_value(MI_HUMIDITY)
        battery = poller.parameter_value(MI_BATTERY)

        data = json.dumps({
            "temperature": temperature,
            "humidity": humidity,
            "battery": battery
        })

        print(datetime.now(), device, " : ", data)

        point = Point("sensordata") \
            .tag("device", device) \
            .field("temp", temperature) \
            .field("hum", humidity) \
            .field("battery", battery) \
            .time(datetime.utcnow(), WritePrecision.NS)

        write_api.write(bucket, org, point)


    except BTLEException as e:
        print("Error connecting to device {0}: {1}".format(device, str(e)))
    except Exception as e:
        print("Error polling device {0}. Device might be unreachable or offline.".format(device))
        print(traceback.print_exc())
