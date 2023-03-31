from imu import MPU6050
from secrets import secrets
import network
import time
import utime
from machine import Pin, I2C , ADC , PWM
import urequests as requests
import json
from collections import OrderedDict

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
imu = MPU6050(i2c)
spi = machine.SPI(0, baudrate=1000000, polarity=0, phase=0, sck=machine.Pin(18), mosi=machine.Pin(19), miso=machine.Pin(16))
cs = machine.Pin(17, machine.Pin.OUT)
cs.value(1)
#Sampling_frequency = 0.1
nb_sample = 5
        
def Run() :
    wlan_connection = connect_to_wlan(secrets)
    
    if wlan_connection.isconnected():
        print("Successfully connected to wlan")
        while True:
                for i in range (nb_sample):
                    response = requests.post('http://192.168.78.234:5000/sensor2', data=get_sensor_values())
                    print(response.text)
                    #time.sleep(Sampling_frequency)
    else:
        print("Fail to connect to wlan, ensure that network is 2.4 Ghz")

def read_adc(channel):
    cs.value(0)
    cmd = bytearray([1, (8 + channel) << 4, 0])
    resp = bytearray(3)
    spi.write_readinto(cmd, resp)
    cs.value(1)
    val = (resp[1] << 8) | resp[2]
    return val

def get_sensor_values():
    sensor_data = OrderedDict([
        ("ax", round(imu.accel.x,2)),
        ("ay", round(imu.accel.y,2)),
        ("az", round(imu.accel.z,2)),
        ("gx", round(imu.gyro.x)),
        ("gy", round(imu.gyro.y)),
        ("gz", round(imu.gyro.z)),
        ("flex_value0", read_adc(0)),
        ("flex_value1", read_adc(1)),
        ("flex_value2", read_adc(2)),
        ("flex_value3", read_adc(3)),
        ("flex_value4", read_adc(4)),
    ])

    return json.dumps(sensor_data)
    
def connect_to_wlan(secrets: dict):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets['ssid'], secrets['pw'])
    
    return wlan
        
if __name__ == "__main__":
    Run()
    