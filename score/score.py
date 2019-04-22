import json
import numpy as np
import keras
from keras.models import load_model

from azureml.core.model import Model

def init():
    global model
    # retreive the path to the model file using the model name
    model_path = Model.get_model_path('model.h5')
    model=load_model(model_path)

def run(raw_data):
    data = np.array(json.loads(raw_data)['data'])
    # make prediction
    y_hat = model.predict(data).tolist()
    #y_hat = np.argmax(y_hat, axis=1)
    return json.dumps(y_hat)