Small set of scripts to read Mijia temperature and humidity sensores and export data to MQTT

Each message is sent to a MQTT topic.
There the data is transformed and send to Domoticz and InfluxDB, based on a flow created in node-red


```
sudo apt-get update && sudo apt-get upgrade -y
sudo rpi-update
#
sudo apt-get install -y python3-pip git
sudo pip3 install bluepy
sudo pip3 install paho-mqtt
sudo pip3 install btlewrap

*/2 * * * * python3 /home/pi/homelab/xiaomi/data-read.py >/dev/null 2>&1```
