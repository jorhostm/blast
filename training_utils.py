import glob

import numpy as np
from tensorflow import keras
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split

def make_model(num_layers=1, num_neurons=8, act="tanh", opt="Nadam", loss="mse", name:str=None):
    if name:
        model = keras.Sequential(name=name)
    else:
        model = keras.Sequential()
    model.add(keras.Input(shape=(2,)))
    for layer in range(num_layers):
        model.add(keras.layers.Dense(num_neurons, activation=act))
    model.add(keras.layers.Dense(1, activation="linear"))

    model.compile(optimizer=opt, loss=loss)
    return model

def prepare_dataset(lagp, n, p, test_size=0.15):
    if isinstance(lagp, list):
        assert len(lagp) == len(n) and len(lagp) == len(p)
        plags = list()
        ns = list()
        ps = list()
        for i in range(len(lagp)):
            lagp_i = np.ones_like(p[i])
            for j,k in enumerate(lagp[i][:,1]):
                lagp_i[j] *= k
    
            plags.append(lagp_i.flatten())
            ns.append(n[i].flatten())
            ps.append(p[i].flatten())
            
        
        lagp_train = np.concatenate(plags)
        p_train = np.concatenate(ps)
        n_train = np.concatenate(ns)
    
    else:
        lagp_train = np.ones_like(p)
        for i,k in enumerate(lagp[:,1]):
            lagp_train[i] *= k

        lagp_train = lagp_train.flatten()
        p_train = p.flatten()
        n_train = n.flatten()

    X = np.transpose([lagp_train, n_train])
    Y = np.transpose([p_train])

    X,X_norms = normalize(X, axis=0, norm='max', return_norm=True, copy=False)
    Y,Y_norms = normalize(Y, axis=0, norm='max', return_norm=True, copy=False)

    x_train,x_val, y_train, y_val = train_test_split(X, Y, test_size=test_size)

    return x_train,x_val, y_train, y_val, X_norms, Y_norms
"""
def load_datasets():
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

    return dataset
"""
def load_datasets(folder="datasets"):
    dataset = dict()
    for job in glob.iglob(f"{folder}/*.npz"):
        jobname = job.split('/')[1].split('.')[0]
        db = np.load(job)
        dataset[jobname] = db

    return dataset

def evaluate_model(model, dataset, X_norms, Y_norms):
    mse = list()
    plate = list()
    size = list()
    mat = list()
    for jobname, db in dataset.items():
        paras = jobname.split('_')
        x_train,x_val, y_train, y_val, x_norms, y_norms = prepare_dataset(lagp=db["PLAG"], n=db["N"], p=db["P"])
        X = np.concatenate([x_train,x_val])
        Y = np.concatenate([y_train,y_val])
        X[:,0] *= x_norms[0]/X_norms[0]
        X[:,1] *= x_norms[1]/X_norms[1]
        Y[:,0] *= y_norms[0]/Y_norms[0]
        results = model.evaluate(X,Y, batch_size=Y.shape[0])
        mse.append(results)
        plate.append(paras[0])
        size.append(paras[1])
        mat.append(f"{paras[2]}_{paras[3]}")

    df = pd.DataFrame()
    df["MSE"] = mse
    df["Plate"] = plate
    df["Mesh size"] = size
    df["Material_Amplitude"] = mat
    
    return df