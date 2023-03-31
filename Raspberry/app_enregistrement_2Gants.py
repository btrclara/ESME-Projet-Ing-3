from flask import Flask, request
import os
import csv
import time
import math

app = Flask(__name__)
sensor_values = []
ready1 = False
ready2 = False
sensor_values2 = []
all_sensors = []
nb_sample = 5

@app.route('/sensor', methods=['POST'])
              
def handle_sensor_data():
        global sensor_values
        global sensor_values2
        global ready1
        global ready2
        global all_sensors
        global nb_sample
        if len(sensor_values) == 0:
            ready1 = True
            print("Ready1")
        if  len(sensor_values2) == 0 and len(sensor_values) == 0 and ready1 == True:            
            print("Enregistrement dans 5 secondes")
            for i in range (5):
                time.sleep(1)
                print(i)
        if len(sensor_values) < nb_sample and ready1 == True and ready2 == True:
            data = request.get_json('data')
            data = list(data.values())
            sensor_values.append(data)

        if len(sensor_values) == nb_sample and len(sensor_values2) == nb_sample:
            for i in range(len(sensor_values)):
                row = sensor_values[i] + sensor_values2[i]
                all_sensors.append(row)
            write_csv(all_sensors)
            print(all_sensors)
            all_sensors = []
            sensor_value = []
            sensor_values2 = []
            ready1 = False
            ready2 = False
        return 'Données recues'

@app.route('/sensor2', methods=['POST'])
              
def handle_sensor_data2():
        global sensor_values2
        global sensor_value
        global ready1
        global ready2
        global all_sensors
        global nb_sample
        if len(sensor_values2) == 0 and ready2 == False:
            ready2 = True
            print("Ready2")
        if  len(sensor_values2) == 0 and len(sensor_values) == 0 and ready2 == True:            
            print("Enregistrement dans 5 secondes")
            for i in range (5):
                time.sleep(1)
                print(i)
        if len(sensor_values2) < nb_sample and ready2 == True and ready1 == True:
            data = request.get_json('data')
            data = list(data.values())
            sensor_values2.append(data)
        if len(sensor_values) == nb_sample and len(sensor_values2) == nb_sample:
            for i in range(len(sensor_values)):
                row = sensor_values[i] + sensor_values2[i]
                all_sensors.append(row)
            write_csv(all_sensors)
            print(all_sensors)
            all_sensors = []
            sensor_value = []
            sensor_values2 = []
            ready2 = False
            ready = False
        return 'Données recues'

def write_csv(data):
    filename = '/home/pi/Desktop/Projet_gant-main/Projet_gant-main/real_time_system/data2.csv'
    if not os.path.exists(filename):
        open(filename, 'a').close
    if os.stat(filename).st_size == 0:
        with open('data2.csv', 'w', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow(['ax','ay','az','gx','gy','gz','flex0','flex1','flex2','flex3','flex4','ax2','ay2','az2','gx2','gy2','gz2','flex5','flex6','flex7','flex8','flex9'])
    with open('data2.csv', 'a',newline = '') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)
                


            
if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')