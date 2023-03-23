from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
import joblib

#test_data = pd.read_csv("dataset.csv")
'''
path = 'dataset.csv'
col_name = ['ax', 'ay', 'az', 'gx', 'gy', 'gz', 'flex1', 'flex2', 'flex3', 'flex4', 'flex5', 'duree', 'class']
dataset = pd.read_csv(path, names=col_name)

lb = LabelEncoder()
dataset['class'] = lb.fit_transform(dataset['class'])
dataset = dataset.drop(columns =['duree'])

dataset = dataset.groupby(dataset.index // 5).agg({
    "ax": [("ax_mean", "mean"), ("ax_std", "std")], 
    "ay": [("ay_mean", "mean"), ("ay_std", "std")], 
    "az": [("az_mean", "mean"), ("az_std", "std")], 
    "gx": [("gx_mean", "mean"), ("gx_std", "std")],
    "gy": [("gy_mean", "mean"), ("gy_std", "std")],
    "gz": [("gz_mean", "mean"), ("gz_std", "std")],
    "flex1": [("flex1_mean", "mean"), ("flex1_std", "std")],
    "flex2": [("flex2_mean", "mean"), ("flex2_std", "std")],
    "flex3": [("flex3_mean", "mean"), ("flex3_std", "std")],
    "flex4": [("flex4_mean", "mean"), ("flex4_std", "std")],
    "flex5": [("flex5_mean", "mean"), ("flex5_std", "std")],
    "class": [("class", "first")],})

dataset.columns = dataset.columns.map('_'.join)
'''

# Charger les données de test
#X_test = ... # Données de test
#y_test = ... # Labels de test
#X_test = dataset.drop("class", axis=1)
#y_test = dataset["class"]

#X = dataset.drop(['class_class'], axis=1)
#y = dataset['class_class']

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)
X_test = [[0.604,0.235436,-0.022,0.14856,0.864,0.134462,7.0,12.884099,1.6,15.883954,-21.6,30.851256,610.0,17.088007,669.6,109.344867,597.8,114.680862,614.8,87.725139,610.2,136.666382]]
# = [[600,600,600,600,600]]

# Charger le modèle préalablement entraîné
#model = RandomForestClassifier()
#model.load('model_pickle_BDD.pkl') # nom du fichier contenant le modèle préalablement entraîné

with open('model_pickle_BDD', 'rb') as f:
    model = pickle.load(f) # nom du fichier contenant le modèle préalablement entraîné
    print('OK')



# Effectuer la prédiction sur les données de test
print(model.predict(X_test))

# Calculer la précision du modèle
#accuracy = accuracy_score(y_test, y_pred)

#print('Précision du modèle: {:.2f}%'.format(accuracy*100))
#print(y_pred)