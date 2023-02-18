import sys 
import numpy as np
import pandas as pd
from numpy import newaxis
import sys
import matplotlib.pyplot as plt
from keras.layers.core import Dense, Activation, Dropout
#from keras.layers.recurrent import LSTM, GRU
from keras.layers.rnn import LSTM, GRU
from keras.models import Sequential
from keras import optimizers
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

plt.switch_backend('agg')


# Load the dataset
path = 'data_test.csv'
col_name = ['ax', 'ay', 'az', 'gx', 'gy', 'gz', 'flex', 'date', 'time', 'class']
dataset = pd.read_csv(path, names=col_name)
print(dataset)

# Convert data type
#dataset["class"] = pd.to_numeric(dataset["class"] , errors="ignore")
#dataset["class"] = dataset["class"].astype(float)
#dataset["class"] = dataset["class"].astype(int)
#dataset["class"] = dataset["class"].astype(object).astype(float)
lb = LabelEncoder()
dataset['class'] = lb.fit_transform(dataset['class'])
dataset['date'] = pd.to_datetime(dataset['date'], format='%Y-%m-%d-%H-%M-%S')
print(dataset)

# Create new column : subclass for every set of movements (30 movements = 1 subclass)
n = len(dataset.index)
count = 0
dataset['subclass'] = [count if i % 30 != 0 else 1 - count for i in range(1, n+1)] # alterner les valeurs 1 et 0 toutes les 30 lignes
count = 1 - count
dataset = dataset[['ax', 'ay', 'az', 'gx', 'gy', 'gz', 'flex', 'date', 'time', 'subclass', 'class']]
print(dataset)



dataset.shape
dataset.head()  # displaying the first 5 records of our dataset
dataset.info()  # prints information about a DataFrame (index dtype, columns, non-null values, memory usage)
dataset.describe()  # to view some basic statistical details of a DataFrame or a series of numeric values
dataset['class'].value_counts()  # checks the number of rows that belongs to each class

'''
# Prep data
def series_to_supervised(data, n=len(dataset)):
	dff = pd.DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n):
		cols.append(dff.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = pd.concat(cols, axis=1)
	agg.columns = names
    # réunir en sous groupe les lignes toutes les 3000ms ou chaque 30 lignes ?
'''

Enrol_window = 30 #100
print ('enrol window set to',Enrol_window )


# Support functions
sc = MinMaxScaler(feature_range=(0,1))
def load_data(datasetname, column, seq_len, normalise_window):
    # A support function to help prepare datasets for an RNN/LSTM/GRU
    data = datasetname.loc[:,column]

    sequence_length = seq_len + 1
    result = []
    for index in range(len(data) - sequence_length):
        result.append(data[index: index + sequence_length])
    
    if normalise_window:
        #result = sc.fit_transform(result)
        result = normalise_windows(result)

    result = np.array(result)

    #Last 10% is used for validation test, first 90% for training
    # splitting dataset 
    '''
    X is having all the dependent variables.
    Y is having an independent variable (in our case ‘class’ is an independent variable).
    '''
    row = round(0.9 * result.shape[0])
    train = result[:int(row), :]
    np.random.shuffle(train) # shouldn't shuffle as group of rows go together ?
    x_train = train[:, :-1] # all rows and column except the last column
    y_train = train[:, -1] # only column "class"
    x_test = result[int(row):, :-1]
    y_test = result[int(row):, -1]

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1)) # "1" en 2ème argument??
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1)) # "1" en 2ème argument??
    # We reshaped the input into the 3D format as expected by LSTMs, namely [samples, timesteps, features]
    return [x_train, y_train, x_test, y_test]


def normalise_windows(window_data):
    # A support function to normalize a dataset
    normalised_data = []
    for window in window_data:
        normalised_window = [((float(p) / float(window[0])) - 1) for p in window]
        normalised_data.append(normalised_window)
    return normalised_data


def predict_sequence_full(model, data, window_size):
    #Shift the window by 1 new prediction each time, re-run predictions on new window
    curr_frame = data[0]
    predicted = []
    for i in range(len(data)):
        predicted.append(model.predict(curr_frame[newaxis,:,:])[0,0])
        curr_frame = curr_frame[1:]
        curr_frame = np.insert(curr_frame, [window_size-1], predicted[-1], axis=0)
    return predicted


def predict_sequences_multiple(model, data, window_size, prediction_len):
    #Predict sequence of <prediction_len> steps before shifting prediction run forward by <prediction_len> steps
    prediction_seqs = []
    for i in range(int(len(data)/prediction_len)):
        curr_frame = data[i*prediction_len]
        predicted = []
        for j in range(prediction_len):
            predicted.append(model.predict(curr_frame[newaxis,:,:])[0,0])
            curr_frame = curr_frame[1:]
            curr_frame = np.insert(curr_frame, [window_size-1], predicted[-1], axis=0)
        prediction_seqs.append(predicted)
    return prediction_seqs


def plot_results(predicted_data, true_data): 
    fig = plt.figure(facecolor='white') 
    ax = fig.add_subplot(111) 
    ax.plot(true_data, label='True Data') 
    plt.plot(predicted_data, label='Prediction') 
    plt.legend() 
    plt.show() 

    

def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    #Pad the list of predictions to shift it in the graph to it's correct start
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
        plt.legend()
    plt.show()


print ('Support functions defined')


# Prepare the dataset
feature_train, label_train, feature_test, label_test = load_data(dataset, 'class', Enrol_window, False)
print ('Datasets generated')

# The model I would like to test (specify LSTM, GRU or RNN)
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(feature_train.shape[1],1)))
model.add(Dropout(0.2))
model.add(LSTM(100, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(1, activation = "linear"))

model.compile(loss='mse', optimizer='adam')

print ('model compiled')
print (model.summary())


#Train the model
model.fit(
    feature_train, 
    label_train, 
    batch_size=512, 
    epochs=10, 
    validation_data = (feature_test, label_test))
#Note that in order to improve the model, one has to adjust epochs and batch_size


#Let's use the model and predict the wave
predictions= predict_sequence_full(model, feature_test, Enrol_window)
plot_results(predictions,label_test)

# Evaluate the trained model
# score = model.evaluate(feature_test, label_test, verbose=0)
# print("Test loss:", str(score)[0])
# print("Test accuracy:", score[1])
from sklearn import metrics
y_pred = np.rint(model.predict(feature_test).flatten()) #flatten() necessary ?

print("Test accuracy:", metrics.accuracy_score(label_test, y_pred))