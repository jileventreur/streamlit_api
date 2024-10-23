import pickle
import numpy as np
import os
import tensorflow_hub as hub

#init global variable
with open('resources/multiLabelBinarizer.pkl', 'rb') as file:
  mlb = pickle.load(file)
with open('resources/model.pkl', 'rb') as file:
  model = pickle.load(file)

os.environ["TF_KERAS"]='1'

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

def feature_USE_fct(sentence, b_size) :
    features = embed([sentence])
    return features

def prepross(question:str):
  batch_size = 10
  features_USE = feature_USE_fct(question, batch_size)
  return features_USE

_max_tags_predicted = 5

def predict(question:str):
  features = prepross(question)
  y_predicted = model.predict_proba(features)
  best_proba = np.argsort(y_predicted[0])[-_max_tags_predicted:]
  y_predicted = np.array([[int(idx in best_proba) for idx in range(len(y_predicted[0]))]])
  predicted_tags = mlb.inverse_transform(y_predicted)
  return predicted_tags[0]