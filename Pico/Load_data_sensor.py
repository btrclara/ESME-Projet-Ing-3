from imu import MPU6050
import time
import utime
from machine import Pin, I2C , ADC , PWM

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
imu = MPU6050(i2c)
spi = machine.SPI(0, baudrate=1000000, polarity=0, phase=0, sck=machine.Pin(18), mosi=machine.Pin(19), miso=machine.Pin(16))
cs = machine.Pin(17, machine.Pin.OUT)
cs.value(1)
Sampling_frequency = 0.1
nb_sample = 30
        
def Run() :
    while True:
        mot = input("Quel mot compté vous enregistrez?\n")
        t_debut = time.ticks_ms() 
        for i in range (nb_sample):
            times = utime.localtime()
            ax,ay,az,gx,gy,gz,flex0,flex1,flex2,flex3,flex4 = get_sensor_values()
            t_fin = time.ticks_ms()
            duree = t_fin - t_debut
            date = str(times[0])+"-"+str(times[1])+"-"+str(times[2])+"\b"+str(times[3])+":"+str(times[4])+":"+str(times[5])
            print(str(ax)+","+str(ay)+","+str(az)+","+str(gx)+","+str(gy)+","+str(gz)+","+str(flex0) + ","
                  +str(flex1)+","+str(flex2)+","+str(flex3)+","+str(flex4)+","+str(date)+","+str(duree)+","+str(mot))
            #write_csv (ax,ay,az,gx,gy,gz,flex,times,duree,mot)
            #SEND_DATA()
            utime.sleep(Sampling_frequency)
            i += 1
        break
    
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
    

        
if __name__ == "__main__":
    Run()
    file.close()