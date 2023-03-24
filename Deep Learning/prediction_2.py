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
        value1, value2, value3, value4, value5, value6, value7, value8,value9,value10,value11,value12,value13,value14,value15,value16,value17,value18,value19,value20,value21,value22 = -0.518,0.676439,-0.404,0.116962,0.55,0.544748,0.2,1.30384,-0.8,6.058052,-5.6,16.456002,290.0,2.345208,673.2,9.654015,827.0,9.192388,756.6,3.435113,674.2,12.255611        
        mp = open_model()
        audio = prediction(value1, value2, value3, value4, value5, value6, value7, value8,value9,value10,value11,value12,value13,value14,value15,value16,value17,value18,value19,value20,value21,value22, mp)
        print(audio)
Run()

# Calculer la précision du modèle
#accuracy = accuracy_score(y_test, y_pred)
#print('Précision du modèle: {:.2f}%'.format(accuracy*100))

#print('Precision: %.3f' % precision_score(y_test, y_pred))

#print('Recall: %.3f' % recall_score(y_test, y_pred))

#print('Accuracy: %.3f' % accuracy_score(y_test, y_pred))

#print('F1 Score: %.3f' % f1_score(y_test, y_pred))