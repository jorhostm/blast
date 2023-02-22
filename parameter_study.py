import fileinput
import sys
import glob

import numpy as np
import matplotlib.pyplot as plt
import pickle
import tensorflow.keras as keras

from training_utils import *
keras.utils.set_random_seed(69)

# Load all the data
dataset = dict()
for job in glob.iglob('*.npz'):
    jobname = job.split('.')[0]
    db = np.load(job)
    keys = jobname.split('_')
    dic = dataset
    for i in range(len(keys)-1):
        dic_next = dic.get(keys[i])
        if not dic_next:
            dic_next = dict()
            dic[keys[i]] = dic_next
        dic = dic_next
    dic[keys[-1]] = db

db = dataset["1-22p5"]["1p5"]["T6"]["15"]
PLAG = db["PLAG"]
P = db["P"]
N = db["N"]
labels = db["labels"]

x_train,x_val, y_train, y_val, X_norms, Y_norms = prepare_dataset(lagp=PLAG, n=N, p=P)
callback = keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True) 

layers = [1,2,3,4]
neurons = [25,50,100,200]
acts = ["tanh", "relu"]

model_dict = dict()
history_dict = dict()


for act in acts:
    for layer in layers:
        for neuron in neurons:
            length = 1
            while length <= 10:
                key = f"{act}_{layer}_{neuron}"
                print(key)
                model = make_model(layer,neuron, act)
                model_dict[key] = model
                history = model.fit(
                    x_train,
                    y_train,
                    batch_size=256,
                    epochs=50,
                    validation_data=(x_val, y_val),
                    callbacks=[callback]
                )
                length = len(history.history["loss"])
            history_dict[key] = history

parameter_dict = {"models":model_dict, "history":history_dict}
with open(f"para.pkl", "wb") as f:
        pickle.dump(parameter_dict, f)