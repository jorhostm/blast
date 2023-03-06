import pickle
import gzip
from tensorflow import keras

from training_utils import *
keras.utils.set_random_seed(69)

dataset = load_datasets()

jobs = ['1-HV_1p5_T7_15' ,'1-HV_1p5_T7_10' ,'4-45_1p5_T7_15']
#jobs = dataset.keys()
#jobs = ["1-22p5_1p5_T6_15", "4-HV_1p5_T7_15", "4-HV_1p5_T7_10"]
#jobs = ["1-22p5_1p5_T6_15", "4-HV_1p5_T7_15"]
plags = [dataset[job]["PLAG"] for job in jobs]
ns = [dataset[job]["N"] for job in jobs]
ps = [dataset[job]["P"] for job in jobs]
    
x_train,x_val, y_train, y_val, X_norms, Y_norms = prepare_dataset(lagp=plags, n=ns, p=ps)
callback = keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True) 

model = make_model(2,8, "relu")
history = model.fit(
x_train,
y_train,
batch_size=1024,
epochs=50,
validation_data=(x_val, y_val),
callbacks=[]
)

para = {"model":model, "history":history.history, "X_norms":X_norms, "Y_norms":Y_norms}

with gzip.open("para.pkl.gz","r+b") as f:
        dic = pickle.load(f)
        dic["para5"] = para

with gzip.open("para.pkl.gz","w+b") as f:
        pickle.dump(dic, f)