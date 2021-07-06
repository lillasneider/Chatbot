import random
import json
import pickle
import numpy as np
import tensorflow
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = i
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    print("predict returning", return_list)
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    result = "huh?"
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result, tag

print("model_load")

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
# print("intents", intents)

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')
print("How can I help you today?")

# Welcoming user stage (see process diagram)

customerName = ""
personalDetailsProvided = False
while not personalDetailsProvided:
    message = input("").strip()
    if message != "":
        print("user:", message)
        ints = predict_class(message)
        res, tag = get_response(ints, intents)
        if 'name' in tag:
            print(res)
            message = input("").strip()
            customerName = message
            personalDetailsProvided = True
        elif 'delivery' in tag:
            print(res)
            pickedDelivery = True
        elif 'collection' in tag:
            print(res)
            pickedCollection = True
        elif 'address' in tag:
            print(res)
            message = input("").strip()
            customerAddress = message
            addressProvided = True
        else:
            print(res)

if customerName != "":
    print(customerName)

# We now have the customer's name and delivery or collection

#if pickedDelivery:
    # loop to get delivery information (address, phone number)

#if pickedCollection:
    # already have name



print("What would you like to order?")

customerOrderFinnish = ""
pizzaDetailsProvided = False
while not pizzaDetailsProvided:
    message = input("").strip()
    if message != "":
        print("user:", message)
        ints = predict_class(message)
        res = get_response(ints, intents)
        if 'pizza' in res:
            print(res)
            message = input("").strip()
            customerOrderFinnish = message
            pizzaDetailsProvided = True
        else:
            print(res)

print(customerOrderFinnish)


