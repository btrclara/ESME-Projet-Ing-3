from flask import Flask, request, jsonify
import os
import csv
import math
import time
import pickle
import json
import speech_recognition as sr
from gtts import gTTS
from subprocess import call


app = Flask(__name__)
sensor_values = []
ready1 = False
ready2 = False
sensor_values2 = []
all_sensors = []
ready_app = False

@app.route('/sensor2', methods=['POST'])
              
def handle_sensor_data():
        global sensor_values
        global sensor_values2
        global ready1
        global ready2
        global all_sensors
        global ready_app
        global data_app
        if len (sensor_values) == 0 and ready_app == True :
            ready1 = True
            print("Ready1")
            print("Prédiction dans 3 secondes")
#             for i in range (3):
            time.sleep(1)
#                 print(i)
        if len(sensor_values) < 5 and ready1 == True and ready_app == True:
            data = request.get_json('data')
            data = list(data.values())
            sensor_values.append(data)
        if len(sensor_values) == 5 and ready_app == True:
            mean2 =calculate_average(sensor_values)
            std2 = calculate_std_deviation(sensor_values)
            mean2.extend(std2)
            all_sensors = mean2
            mp = open_model()
            audio = prediction(all_sensors, mp)
            #commande_vocale(audio[0])
            print(audio)
            all_sensors = []
            sensor_values = []
            if data_app == "0" or data_app == "1":
                ready_app = False
            #ready_app = False
        return 'Données recues'


def write_csv(data):
    filename = '/home/pi/Desktop/Projet_gant-main/Projet_gant-main/real_time_system/data_clara.csv'
    if not os.path.exists(filename):
        open(filename, 'a').close
    if os.stat(filename).st_size == 0:
        with open('data_clara.csv', 'w', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow(['ax','ay','az','gx','gy','gz','flex0','flex1','flex2','flex3','flex4','duree','mot'])
    with open('data_clara.csv', 'a',newline = '') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)
                
def calculate_average(all_sensors):
    averages = []
    for i in range(len(all_sensors[0])):
        sum = 0
        count = 0
        for j in range(len(all_sensors)):
            sum += all_sensors[j][i]
            count += 1
        averages.append(sum / count)
    return averages

def calculate_std_deviation(all_sensors):
    std_deviations = []
    averages = calculate_average(all_sensors)
    for i in range(len(all_sensors[0])):
        sum_of_squares = 0
        count = 0
        for j in range(len(all_sensors)):
            sum_of_squares += (all_sensors[j][i] - averages[i]) ** 2
            count += 1
        std_deviations.append(math.sqrt(sum_of_squares / (count - 1)))
    return std_deviations

def open_model():
        with open('model_pickle_BDD_Thomas6', 'rb') as f:
            mp = pickle.load(f)
            return mp

def prediction(all_sensors, mp):
        value1, value2, value3, value4, value5, value6, value7, value8,value9,value10,value11,value12,value13,value14,value15,value16,value17,value18,value19,value20,value21,value22 = all_sensors[0],all_sensors[1],all_sensors[2],all_sensors[3],all_sensors[4],all_sensors[5],all_sensors[6],all_sensors[7],all_sensors[8],all_sensors[9],all_sensors[10],all_sensors[11],all_sensors[12],all_sensors[13],all_sensors[14],all_sensors[15],all_sensors[16],all_sensors[17],all_sensors[18],all_sensors[19],all_sensors[20],all_sensors[21]
        print(mp.predict([[value1, value2, value3, value4, value5, value6, value7, value8,value9,value10,value11,value12,value13,value14,value15,value16,value17,value18,value19,value20,value21,value22]]))
        prediction = mp.predict([[value1, value2, value3, value4, value5, value6, value7, value8,value9,value10,value11,value12,value13,value14,value15,value16,value17,value18,value19,value20,value21,value22]])
        return prediction

def commande_vocale(prediction):
    language = 'fr'
    myobj = gTTS(text=prediction, lang=language, slow=False)
    myobj.save("test.mp3")
    command = "mpg123 test.mp3"
    call([command], shell = True)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    global ready_app
    global data_app
    data_app = request.data.decode('utf-8')
    print('Received data:', data_app)
    if (data_app == "1"):
          ready_app = True
          return ""
    if (data_app =="2"):
        ready_app = True
        return ""
    if (data_app == "0"):
        ready_app = False
        return ""
    


        
    
    if (a != ""):
        return a
    else:
        return ""

    


        
def launchRaspberry():
    print("lancement code raspberry")
    
def speechToText():
    global a
    # Créer un objet de reconnaissance vocale
    r = sr.Recognizer()
    
    # Enregistrer l'audio à partir du microphone
    with sr.Microphone() as source:
        print("Parlez maintenant...")
        audio = r.listen(source)
    
    # # Reconnaissance vocale avec Google
    try:
        a = r.recognize_google(audio, language="fr-FR")
        print("Reconnaissance vocale : " + a)
        return a
        #request.get('http://192.168.1.16:1300', a)
    except sr.UnknownValueError:
        print("Google Speech Recognition n'a pas pu comprendre l'audio")
    except sr.RequestError as e:
        print("Impossible d'obtenir la reconnaissance vocale de Google; {0}".format(e))




if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')
