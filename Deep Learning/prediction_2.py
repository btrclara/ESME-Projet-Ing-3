import pickle
import os
import time

def open_model():
        with open('model_pickle_BDD', 'rb') as f:
            mp = pickle.load(f)
            return mp
        
def prediction(value1, value2, value3, value4, value5, value6, value7, value8,value9,value10,value11,value12,value13,value14,value15,value16,value17,value18,value19,value20,value21,value22, mp):
        print(mp.predict([[value1, value2, value3, value4, value5, value6, value7, value8,value9,value10,value11,value12,value13,value14,value15,value16,value17,value18,value19,value20,value21,value22]]))
        prediction = mp.predict([[value1, value2, value3, value4, value5, value6, value7, value8,value9,value10,value11,value12,value13,value14,value15,value16,value17,value18,value19,value20,value21,value22]])
        return prediction

def Run():
        #value1, value2, value3, value4, value5, value6, value7, value8,value9,value10,value11,value12,value13,value14,value15,value16,value17,value18,value19,value20,value21,value22 = 0.604,0.235436,-0.022,0.14856,0.864,0.134462,7.0,12.884099,1.6,15.883954,-21.6,30.851256,610.0,17.088007,669.6,109.344867,597.8,114.680862,614.8,87.725139,610.2,136.666382
        value1, value2, value3, value4, value5, value6, value7, value8,value9,value10,value11,value12,value13,value14,value15,value16,value17,value18,value19,value20,value21,value22 = -0.418,0.020494,0.356,0.008944,0.922,0.016432,-1.6,1.516575,2.6,1.516575,-1.4,3.646917,463.6,2.302173,723.2,7.293833,686.6,12.054045,684.8,11.649034,702.6,13.10725        
        mp = open_model()
        audio = prediction(value1, value2, value3, value4, value5, value6, value7, value8,value9,value10,value11,value12,value13,value14,value15,value16,value17,value18,value19,value20,value21,value22, mp)
        print(audio)
Run()