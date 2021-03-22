import pandas as pd
import numpy as np

Columns = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32]
TableOutput = pd.read_excel("appearance_data_tottenham.xlsx",usecols=Columns)

# split into input (X) and output (y) variables
x = np.array(TableOutput.iloc[:,:-1].values)
y = np.array(TableOutput.iloc[:,-1].values)
y = [x for x in y if str(x) != 'nan']

from numpy.random import seed
from tensorflow.random import set_seed
set_seed(0)
seed(0)

print(x)
print(y)

iris = TableOutput

print('num classes:', len(np.unique(y)))
print(x.shape)
print(len(y))
num_features = x.shape[1]
num_classes = len(np.unique(y))

import matplotlib.pyplot as plt


from keras.utils import to_categorical

y = to_categorical(y)


from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.25)

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD

model = Sequential()

model.add(Dense(12, input_dim=num_features, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer=SGD(learning_rate=0.01), metrics=['accuracy'])

history = model.fit(x_train, y_train, epochs=500)

loss, accuracy = model.evaluate(x_test, y_test)

plt.plot(history.history['loss'])
plt.xlabel('epochs')
plt.ylabel('loss')
plt.show()

plt.plot(history.history['accuracy'])
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.show()