# -*- coding: utf-8 -*-
"""Gender Detection through morphometry of Eyes

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jUMX889DS0C6tR7RqNDjDwnvqmici0JV

# **Areeb Adnan Khan**

# **Loading Libraries**
All Python capabilities are not loaded to our working environment by default (even they are already installed in your system). So, we import each and every library that we want to use.

We chose alias names for our libraries for the sake of our convenience (numpy --> np and pandas --> pd, tensorlow --> tf).

Note: You can import all the libraries that you think will be required or can import it as you go along.

Data Pre-processing

It is necessary to bring all the images in the same shape and size, also convert them to their pixel values because all machine learning or deep learning models accepts only the numerical data. Also we need to convert all the labels from categorical to numerical values.

AND:

Building Model & Hyperparameter tuning
Now we are finally ready, and we can train the model.
"""

from google_drive_downloader import GoogleDriveDownloader as gdd

gdd.download_file_from_google_drive(file_id='1f7uslI-ZHidriQFZR966_aILjlkgDN76',
dest_path='content/eye_gender_data.zip',
unzip=True)


import cv2
import os
import csv
import numpy as np
import sys
import tensorflow as wtf
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from tensorflow.keras import datasets, layers, models, losses, Model


EPOCHS = 100
IMG_WIDTH = 30
IMG_HEIGHT = 30
TEST_SIZE = 0.25


def main():

    # Get image arrays and labels for all image files
    images, labels = load_data('/content/content/eye_gender_data/train','/content/content/eye_gender_data/Training_set.csv')

    # Split data into training and testing sets
    labels = wtf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    filename = 'Eyes_model_4.h5'
    model.save(filename)
    print(f"Model saved to {filename}.")


def load_data(data_dir,filename):

    with open(filename,'r') as f:
        reader = csv.reader(f)
        fields = next(reader)
        rows = {}
        for row in reader:
            rows[row[0]] = row[1]
    #print(rows)
    #n = 0
    images = []
    lables = []
    for files in os.walk(data_dir):
        names = list(files)[2]
        #print(names)
        for img in names :
            #print(img,rows[n][0])
            #print(img,rows[img])
            image = cv2.imread(os.path.join(files[0], img))
            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
            #print(image)
            images.append(image)
            lables.append(1 if rows[img] == 'male' else 0)  
            #print(img,lables[n])
            #n+=1
    return(images,lables)

load_data('/content/content/eye_gender_data/train','/content/content/eye_gender_data/Training_set.csv')


def get_model():

    model = wtf.keras.Sequential(
    [
        wtf.keras.layers.Conv2D(32 ,(3,3) ,activation = "relu", input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)),
        wtf.keras.layers.MaxPooling2D(pool_size = (3,3)),
        wtf.keras.layers.Conv2D(32 ,(3,3) ,activation = "relu", input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)),   
        wtf.keras.layers.MaxPooling2D(pool_size = (2,2)),
        wtf.keras.layers.Conv2D(32 ,(3,3) ,activation = "relu", input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)),
        wtf.keras.layers.Flatten(),
        wtf.keras.layers.Dense(200, activation = "relu"),
        wtf.keras.layers.Dropout(0.5),
        wtf.keras.layers.Dense(2, activation = "softmax")
    ])
    model.compile(optimizer = "adam", loss = "categorical_crossentropy", metrics=["accuracy"])
    return model

if __name__ == "__main__":
   main()


# res = pd.DataFrame(predictions) #preditcions are nothing but the final predictions of your model on input features of your new unseen test data
# res.index = test_new.index # its important for comparison. Here "test_new" is your new test dataset
# res.columns = ["classification"]

# # To download the csv file locally
# from google.colab import files
# res.to_csv('prediction_results.csv', inplace = False)         
# files.download('prediction_results.csv')

def empty_csv():
    with open("/content/content/result.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(("label", ))

"""## **Data Pre-processing on test_data**
--------------------------------------------
### **Make Prediction on Test Dataset**


"""

import csv

model = wtf.keras.models.load_model('Eyes_model_4.h5')
empty_csv()
for name, blank, files in os.walk('/content/content/eye_gender_data/test'):
    files.sort(key = lambda x: int(x.split("_")[1][:-4]))
    for img in files:
        image = cv2.imread(os.path.join(name, img))
        image = cv2.resize(image, (30, 30))
        classification = model.predict([np.array(image).reshape(1,30,30,3)]).argmax()
        with open("/content/content/result.csv", "a") as f:
            writer = csv.writer(f)
            if classification == 1:
                writer.writerow(("male", ))
            else:
                writer.writerow(("female",))
print("CSV Created !!")

"""Well Done! 👍
You are all set to make a submission. Let's head to the challenge page to make the submission.
"""

