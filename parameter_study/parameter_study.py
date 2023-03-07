import pickle
from tensorflow import keras

from training_utils import *
keras.utils.set_random_seed(69)

dataset = load_datasets()
db = dataset["1-22p5_1p5_T6_15"]
PLAG = db["PLAG"]
P = db["P"]
N = db["N"]
labels = db["labels"]

x_train,x_val, y_train, y_val, X_norms, Y_norms = prepare_dataset(lagp=PLAG, n=N, p=P)
callback = keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True) 

layers = [1,2,3,4]
neurons = [4,8,16,32]
acts = ["tanh", "relu"]

model_dict = dict()
history_dict = dict()


for act in acts:
    for layer in layers:
        for neuron in neurons:
            key = f"{act}_{layer}_{neuron}"
            print(key)
            model = make_model(layer,neuron, act, name=key)
            model_dict[key] = model
            history = model.fit(
                x_train,
                y_train,
                batch_size=1024,
                epochs=50,
                validation_data=(x_val, y_val),
                callbacks=[callback]
            )
            history_dict[key] = history

parameter_dict = {"models":model_dict, "history":history_dict, "X_norms":X_norms, "Y_norms":Y_norms}
with open(f"para.pkl", "wb") as f:
        pickle.dump(parameter_dict, f)