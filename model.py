import pickle
import numpy as np
import tensorflow as tf
# import tensorflow.keras
# from tensorflow.keras import backend as K
import os

# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# from tensorflow.keras import metrics as kmetrics
# from tensorflow.keras.layers import *
# from tensorflow.keras.models import Model

# # Bert
# import transformers
# from transformers import *
import tensorflow_hub as hub

#init global variable
with open('resources/multiLabelBinarizer.pkl', 'rb') as file:
  mlb = pickle.load(file)
with open('resources/model.pkl', 'rb') as file:
  model = pickle.load(file)

os.environ["TF_KERAS"]='1'

# print(tf.__version__)
# print(tf.__version__)
# print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
# print(tf.test.is_built_with_cuda())
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

def feature_USE_fct(sentence, b_size) :
    features = embed([sentence])
    return features

def prepross(question:str):
  batch_size = 10
  features_USE = feature_USE_fct(question, batch_size)
#   print(features_USE)
  return features_USE

_max_tags_predicted = 5
print(mlb.classes_)

def predict(question:str):
  features = prepross(question)
  y_predicted = model.predict_proba(features)
#   print("BEFORE")
#   print(f'{y_predicted=}')
  best_proba = np.argsort(y_predicted[0])[-_max_tags_predicted:]
#   print(f'{best_proba=}')
  y_predicted = np.array([[int(idx in best_proba) for idx in range(len(y_predicted[0]))]])
#   print("AFTER")
#   print(f'{y_predicted=}')
  predicted_tags = mlb.inverse_transform(y_predicted)
#   print(predicted_tags)
  return predicted_tags[0]