import tensorflow as tf 
from scipy.misc import imshow
from scipy.misc import imresize
from keras.models import Sequential
from keras.layers import Dense, Flatten, InputLayer
from sklearn.preprocessing import LabelEncoder
from matplotlib.pyplot import imread
from PIL import Image 
import numpy as np 
import pandas as pd
import os
import random

data_dir='/home/nithin/TensorFlow/AgeDetection'
train = pd.read_csv(os.path.join(data_dir, 'train.csv'))
test = pd.read_csv(os.path.join(data_dir, 'test.csv'))

lb = LabelEncoder()

temp = []
for img_name in train.ID:
    abc=img_name.replace('./Train/','')
    img_path = os.path.join(data_dir, 'Train', abc)
    img = imread(img_path)
    img = imresize(img, (32, 32))
    temp.append(img)
train_x = np.stack(temp)

temp = []
for img_name in test.ID:
    img_path = os.path.join(data_dir, 'Test', img_name)
    img = imread(img_path)
    img = imresize(img, (128, 128))
    temp.append(img)
test_x = np.stack(temp)

train_x = train_x / 255.
test_x = test_x / 255.

train.Class.value_counts(normalize=True)


train_y = lb.fit_transform(train.Class)
print(train_y)
train_y = tf.compat.v2.keras.utils.to_categorical(train_y)

input_num_units = (32, 32, 3)
hidden_num_units = 500
output_num_units = 3

epochs = 10
batch_size = 128
model = Sequential([
  InputLayer(input_shape=input_num_units),
  Flatten(),
  Dense(units=hidden_num_units, activation='relu'),
  Dense(units=output_num_units, activation='softmax'),
])

model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_x, train_y, batch_size=batch_size,epochs=epochs,verbose=1, validation_split=0.2)

i = random.choice(train.index)
print(i)
img_name = train.ID[i]
abc=img_name.replace('./Train/','')
img = imread(os.path.join(data_dir, 'Train', abc))

pred = model.predict_classes(train_x)
pred=pred[i]

if(pred==0):
  print('Original:', train.Class[i], 'Predicted:MIDDLE' )
elif(pred==1):
   print('Original:', train.Class[i], 'Predicted:OLD' )
elif(pred==2):
    print('Original:', train.Class[i], 'Predicted:YOUNG' ) 

imshow(imresize(img, (128, 128)))


