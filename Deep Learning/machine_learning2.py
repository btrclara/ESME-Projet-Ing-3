# 1. Importing libraries

import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
sns.set_palette('husl')
import matplotlib.pyplot as plt
import pickle

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report, plot_confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
# 2. Loading Iris data

# path = 'BDD_final_v2_sans_other.csv'  # path of the dataset
# col_name = ['doigt_1', 'doigt_2', 'doigt_3', 'doigt_4', 'doigt_5', 'class']  # creates the list of column name
# dataset = pd.read_csv(path, names=col_name)  # pandas read_csv() is used for reading the csv file

path = 'dataset.csv'
#col_name = ['ax', 'ay', 'az', 'gx', 'gy', 'gz', 'flex', 'date', 'time', 'class']
col_name = ['ax', 'ay', 'az', 'gx', 'gy', 'gz', 'flex1', 'flex2', 'flex3', 'flex4', 'flex5', 'duree', 'class']

dataset = pd.read_csv(path, names=col_name)

# Convert data type & remove unwanted columns
#lb = LabelEncoder()
#dataset['class'] = lb.fit_transform(dataset['class'])
#dataset = dataset.drop(columns =['date', 'time'])
dataset = dataset.drop(columns =['duree'])

print(dataset)

# Group by subclass (every 30 lines)
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

# 3. Summarize the Dataset
dataset.shape
dataset.head()  # displaying the first 5 records of our dataset
dataset.info()  # prints information about a DataFrame (index dtype, columns, non-null values, memory usage)
dataset.describe()  # to view some basic statistical details of a DataFrame or a series of numeric values
#dataset['class'].value_counts()  # checks the number of rows that belongs to each class


# 5. Model Building- part 1

# 5.1 Splitting the dataset
'''
X is having all the dependent variables.
Y is having an independent variable (here in this case ‘class’ is an independent variable).
'''
X = dataset.drop(['class_class'], axis=1)
y = dataset['class_class']
print(f'X shape: {X.shape} | y shape: {y.shape} ')

# 5.2 Train Test split
'''
Splitting our dataset into train and test using train_test_split(), what we are doing here is taking 80% of 
data to train our model, and 20% that we will hold back as a validation dataset
'''
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)

# 5.3 Model Creation
'''
We don’t know which algorithms would be best for this problem.
Let’s check each algorithm in loop and print its accuracy, so that we can select our best algorithm
'''
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVC', SVC(gamma='auto')))
models.append(('RandomForestClassifier', RandomForestClassifier()))
# evaluate each model in turn
results = []
model_names = []
for name, model in models:
    kfold = StratifiedKFold(n_splits=2, random_state=1, shuffle=True) # quelle valeur de n_split mettre ?? 
    cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
    results.append(cv_results)
    model_names.append(name)
    print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))

# 6. Model Building- part 2

model = RandomForestClassifier()
X_train = X_train.values
model.fit(X_train, y_train)
prediction = model.predict(X_test)
accuracy_score(y_test, prediction)
classification_report(y_test, prediction)
print(f'Test Accuracy: {accuracy_score(y_test, prediction)}')
print(f'Classification Report: \n {classification_report(y_test, prediction)}')
plot_confusion_matrix(model, X_test, y_test)
plt.show()
with open('model_pickle_BDD' , 'wb') as f :
 pickle.dump(model,f)

with open('model_pickle_BDD' , 'rb') as f :
  mp = pickle.load(f)

