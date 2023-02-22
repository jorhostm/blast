import numpy as np
import tensorflow.keras as keras

from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split

def make_model(num_layers=1, num_neurons=8, act="tanh", opt="Nadam", loss="mse"):
    model = keras.Sequential()
    model.add(keras.Input(shape=(2,)))
    for layer in range(num_layers):
        model.add(keras.layers.Dense(num_neurons, activation=act))
    model.add(keras.layers.Dense(1, activation="linear"))

    model.compile(optimizer=opt, loss=loss)
    return model

def prepare_dataset(lagp, n, p, test_size=0.15):
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