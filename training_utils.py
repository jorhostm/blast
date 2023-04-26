import glob

import numpy as np
from tensorflow import keras
import pandas as pd

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

def prepare_dataset(lagp, n, p, test_size=0.15, split=True):
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

    if split:
        X = np.transpose([lagp_train, n_train])
        Y = np.transpose([p_train])

        X,X_norms = normalize(X, axis=0, norm='max', return_norm=True, copy=False)
        Y,Y_norms = normalize(Y, axis=0, norm='max', return_norm=True, copy=False)

        x_train,x_val, y_train, y_val = train_test_split(X, Y, test_size=test_size)

        return x_train,x_val, y_train, y_val, X_norms, Y_norms
    
    else:
        return lagp_train, n_train, p_train

def load_datasets(folder="datasets"):
    dataset = dict()
    for job in glob.iglob(f"{folder}/*.npz"):
        jobname = job.split('/')[-1].split('.')[0]
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
        plag,n, p = prepare_dataset(lagp=db["PLAG"][:-1], n=db["N"][:-1], p=db["P"][:-1], split=False)
        plag /= X_norms[0]
        n /= X_norms[1]
        p /= Y_norms[0]
        X = np.transpose([plag,n])
        Y = np.transpose([p])
        results = model.evaluate(X,Y, batch_size=Y.shape[0], verbose=0)
        mse.append(results)
        plate.append(paras[0])
        size.append(paras[1])
        mat.append(f"{paras[2]}_{paras[3]}")

    df = pd.DataFrame()
    df["MSE"] = mse
    df["Plate"] = plate
    df["Mesh size"] = size
    df["Material_Amplitude"] = mat
    df["Job"] = dataset.keys()
    
    return df


def to_fortran_from_model(filename):
    """
    Write a text file network weights and bias to use with the FORTAN subroutines.
    It uses a keras model to write the parameters.
    """
#-------------------------------------------------------------------------------------------------------------------------------------
#   DEFINE FILENAME FOR FORTRAN
#-------------------------------------------------------------------------------------------------------------------------------------
    outputname = filename.split('.')[0]+'.ann'
#-------------------------------------------------------------------------------------------------------------------------------------
#   LOAD KERAS MODEL
#-------------------------------------------------------------------------------------------------------------------------------------
    model = keras.models.load_model(filename,compile=False)
#-------------------------------------------------------------------------------------------------------------------------------------
#   OPEN FILE
#-------------------------------------------------------------------------------------------------------------------------------------
    fp = open(outputname,'w')
#-------------------------------------------------------------------------------------------------------------------------------------
#   SET VARIABLES
#-------------------------------------------------------------------------------------------------------------------------------------
    n_layers = len(model.layers)
    k = 0
#-------------------------------------------------------------------------------------------------------------------------------------
#   WRITE LAYERS
#-------------------------------------------------------------------------------------------------------------------------------------
    for layer,k in zip(model.layers,range(0,n_layers)):
        nrow    = np.shape(layer.get_weights()[0])[0]
        ncolumn = np.shape(layer.get_weights()[0])[1]
        activation = layer.get_config()['activation']
        activation_code = get_code_from_activation(activation)
#-------------------------------------------------------------------------------------------------------------------------------------
#       WRITE LAYER PARAMETERS
#-------------------------------------------------------------------------------------------------------------------------------------
        if k == 0:
           fp.write('*input_layer,inputs={},neurons={},activation={}\n'.format(nrow,ncolumn,activation_code))
        elif k==n_layers-1:
           fp.write('*output_layer,outputs={},activation={}\n'.format(ncolumn,activation_code))
        else:
           fp.write('*hidden_layer,number={},neurons={},activation={}\n'.format(k,ncolumn,activation_code))
        for neurons_weight,neurons_bias in zip(np.transpose(layer.get_weights()[0]), layer.get_weights()[1]):
           nparam = len(list(neurons_weight))+1
           fp.write(('{:.8f}, '*nparam +'\n').format(*list(neurons_weight),neurons_bias))
#-------------------------------------------------------------------------------------------------------------------------------------
#   CLOSE FILE
#-------------------------------------------------------------------------------------------------------------------------------------
    fp.close()
    return

def get_code_from_activation(activation):
    """
    Get code name from activation function name
    """
    if activation == 'linear':
       return 0
    elif activation == 'relu':    
       return 1
    elif activation == 'sigmoid':    
       return 2
    elif activation == 'softmax':    
       return 3
    elif activation == 'tanh':
       return 4
    else:
       print('error activation function not defined')
       return []
