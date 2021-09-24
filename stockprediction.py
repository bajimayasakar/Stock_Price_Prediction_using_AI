#numpy for scientific computation
#Matplotlib for plotting graphs
#pandas for loading and maanipulationg datasets
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

#load the dataset

dataset_train = pd.read_csv('ADBL.csv')
training_set = dataset_train.iloc[:, 1:2].values

#check the head of the dataset to confirm the use of datasets
dataset_train.head()


#feature scaling

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled =sc.fit_transform(training_set)


#creating data with Timesteps

X_train = []
y_train = []
for i in range(60, 1150):
    X_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])

X_train, y_train =np.array(X_train), np.array(y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))


#building the LSTM
#Dropout layer to prevent overfitting



from tensorflow.keras import layers
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout


regressor = Sequential()

regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

regressor.add(Dense(units = 1))

regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)



#predicting future stock using test training_set

dataset_test = pd.read_csv('')
real_stock_price = dataset_test.iloc[:, 1:2].values


#After making the predictions we use inverse_transform to get back the stock prices in normal readable format.

dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
for i in range(60, 76):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

#plotting the result

plt.plot(real_stock_price, color = 'black', label = 'ADBL Stock Prices')
plt.plot(predicted_stock_price, color = 'red', label = 'Predicted Stock Prices')
plt.title('ADBL Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('ADBL Stock Price')
plt.legend()
plt.show()






    
