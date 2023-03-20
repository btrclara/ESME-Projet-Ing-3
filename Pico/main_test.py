import network
import json
import time
import socket
from secrets import secrets
from imu import MPU6050
import utime
from machine import Pin, I2C , ADC , PWM

host, port =('192.168.241.234', 1234)
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
imu = MPU6050(i2c)
spi = machine.SPI(0, baudrate=1000000, polarity=0, phase=0, sck=machine.Pin(18), mosi=machine.Pin(19), miso=machine.Pin(16))
cs = machine.Pin(17, machine.Pin.OUT)
cs.value(1)
Sampling_frequency = 0.1
nb_sample = 15

def run():
    wlan_connection = connect_to_wlan(secrets)
    
    if wlan_connection.isconnected():
        print("Successfully connected to wlan")
        socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_conn.connect((host, port))
        print("Ok")
        
        while True:
            print("Ok")
            time.sleep(1)
            
            try:
                print("Ok")
                mot = input("Quel mot compté vous enregistrez?\n")
                t_debut = time.ticks_ms()
                data = []
                for i in range (nb_sample):
                    times = utime.localtime()
                    ax,ay,az,gx,gy,gz,flex0,flex1,flex2,flex3,flex4 = get_sensor_values()
                    t_fin = time.ticks_ms()
                    duree = t_fin - t_debut
                    date = str(times[0])+"-"+str(times[1])+"-"+str(times[2])+"\b"+str(times[3])+":"+str(times[4])+":"+str(times[5])
                    data_ligne =[ax,ay,az,gx,gy,gz,flex0,flex1,flex2,flex3,flex4,duree,mot]
                    #data = "Bonjour, je suis le client"
                    data.append(data_ligne)
                    json_data = json.dumps(data)
                    utime.sleep(Sampling_frequency)
                    i += 1
                send_data(socket_conn, json_data)
                time.sleep(1)
                break
            except Exception as e:
                print("Connexion au serveur refusé")
                print(e)
                
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
        ax=round(imu.accel.x,2)
        ay=round(imu.accel.y,2)
        az=round(imu.accel.z,2)
        gx=round(imu.gyro.x)
        gy=round(imu.gyro.y)
        gz=round(imu.gyro.z)
        flex_value0 = read_adc(0)
        flex_value1 = read_adc(1)
        flex_value2 = read_adc(2)
        flex_value3 = read_adc(3)
        flex_value4 = read_adc(4)
        
        return ax,ay,az,gx,gy,gz,flex_value0,flex_value1,flex_value2,flex_value3,flex_value4
        
def send_data(socket_conn, json_data):
    encoded_data = json_data.encode("utf8")
    socket_conn.sendall(encoded_data)

def connect_to_wlan(secrets: dict):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets['ssid'], secrets['pw'])
    
    return wlan

if __name__ == "__main__":
    run()