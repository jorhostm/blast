import numpy as np
from tensorflow import keras
import pickle
import gzip

def make_model(inputs=3, num_layers=1, num_neurons=8, act="tanh", opt="Nadam", loss="mse", name:str=None):
    if name:
        model = keras.Sequential(name=name)
    else:
        model = keras.Sequential()
    model.add(keras.Input(shape=(inputs,)))
    for layer in range(num_layers):
        model.add(keras.layers.Dense(num_neurons, activation=act))
    model.add(keras.layers.Dense(1, activation="linear"))

    model.compile(optimizer=opt, loss=loss)
    return model


if __name__ == "__main__":
    """
    keras.utils.set_random_seed(69)
    data = np.load("data.npz")
    train = data["train"]
    x = np.array(train[:,:-1])
    y = np.array(train[:,-1])

    callback = keras.callbacks.EarlyStopping(monitor="val_loss", patience=15, restore_best_weights=True)

    layers = [1,2,3,4]
    neurons = [8,16,32,64]
    neurons = [128,256,512,1028]
    acts = ["tanh", "relu"]

    model_dict = dict()
    history_dict = dict()

    for act in acts:
        for layer in layers:
            for neuron in neurons:
                key = f"{act}_{layer}_{neuron}"
                print(key)
                model = make_model(7, layer, neuron, act, name=key)
                model_dict[key] = model
                history = model.fit(
                    x,
                    y,
                    batch_size=32,
                    epochs=50,
                    validation_split=0.15,
                    callbacks=[callback],
                    shuffle=True
                )
                history_dict[key] = history.history
                parameter_dict = {"models":model_dict, "history":history_dict}
                with gzip.open(f"para3.pkl.gz", "w+b") as f:
                        pickle.dump(parameter_dict, f)
    """
    keras.utils.set_random_seed(69)
    #data = np.load("data.npz")
    with gzip.open("train.pkl.gz", "rb") as fp:
         dic = pickle.load(fp)

    with gzip.open("all_4_64.pkl.gz","rb") as fp:
        dic2 = pickle.load(fp)
    train = dic["data"]
    x = train[:,:-1]
    y = train[:,-1]

    callback = keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)

    key = f"relu_3_64"
    print(key)
    #model = make_model(7, 4, 64, "relu", name=key)
    model = dic2["model"]
    history = model.fit(
        x,
        y,
        batch_size=128,
        epochs=50,
        validation_split=0.15,
        callbacks=[callback],
        shuffle=True
    )
    parameter_dict = {"model":model, "history":history.history}
    with gzip.open(f"all_4_64_2.pkl.gz", "w+b") as f:
            pickle.dump(parameter_dict, f)