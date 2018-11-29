from umqtt.simple import MQTTClient
import time
import network
import dht
from machine import I2C, Pin
import mpu6050

i2c = I2C(scl=Pin(5), sda=Pin(4))

d = dht.DHT22(Pin(12))

Atgy = 0


config = {"wifiSSID": "alpha12",
          "wifiPass": "fisicafisica",
          "ip": "192.168.137.1",
          "nodeId": "esp1"}

#inputPin = machine.Pin(15, machine.Pin.IN)
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(config['wifiSSID'], config['wifiPass'])

    

def mp():
    global i2c
    accelerometer = mpu6050.accel(i2c)
    g = accelerometer.get_values()
    return g

pass



def medir():
    global d
    d.measure()
    return d.temperature()
pass


def sub_cb(topic, msg):
    print(msg, topic)


def main(server=config['ip']):
    global g
    global Atgy
    time.sleep(3)
    c = MQTTClient('esp8266_01', server)
    c.set_callback(sub_cb)
    try:
        c.connect()
        while True:
            t = str(medir())
            c.publish("temp","temp "+t)
            time.sleep(1)
            g = mp()
            Atgy = str(g["GyY"])
            c.publish("gx","giro " + Atgy)            
    except OSError:
        main()



    c.disconnect()

g = mp()

main()
