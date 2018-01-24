import numpy as np
from numpy import newaxis
import os
import random
import librosa
import re
filelist = os.listdir("/media/sinclair/SINCLAIR32/TestZone/DataSet/MixedTape")

def get_audio_array(path):
    y, sr = librosa.load(path,sr=20000,mono=True)
    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
    return S
def get_label(filename):
    for i, c in enumerate(filename):
        if c.isdigit():
            index = i
            break
    return filename[0:i]
def get_vector_label(stringlabel):
    if stringlabel == "Juno":
        return np.array([1,0,0])
    elif stringlabel == "Silence":
        return np.array([0,1,0])
    elif stringlabel == "Talking":
        return np.array([0,0,1])


    elif stringlabel == "LongSilence":
        return np.array([1,0,0,0,0])
    elif stringlabel == "Google":
        return np.array([0,1,0,0,0])
    elif stringlabel == "Messenger":
        return np.array([0,0,1,0,0])
    elif stringlabel == "YouTube":
        return np.array([0,0,0,1,0])
    elif stringlabel == "Gmail":
        return np.array([0,0,0,0,1])
def get_name_label(array):
    if array == np.array([1,0,0]):
        return "Juno"
    elif array == np.array([0,1,0]):
        return "Silence"
    elif array == np.array([0,0,1]):
        return "Talking"
def get_batch(batch_size):
    x = np.array(get_audio_array("MixedTape/Juno0.wav"))
    y = np.array([1,0,0]).reshape(3)
    for i in range(batch_size-1):
        #X creation
        index = random.randint(0,len(filelist)-1)
        filename = filelist[index]
        x = np.dstack((x,get_audio_array("MixedTape/"+filename)))
        betterx = np.swapaxes(x,0,2)
        y = np.dstack((y,get_vector_label(get_label(filename))))
        bettery = np.swapaxes(y,1,2)
    bettery = bettery.reshape(bettery.shape[1:])
    return betterx, bettery

#long part comes in here

filelistlong = os.listdir("/media/sinclair/SINCLAIR32/TestZone/DataSet/LongMixedTape")

def get_batch_long(batch_size):
    x = np.array(get_audio_array("LongMixedTape/LongSilence0.wav"))
    y = np.array([1,0,0,0,0]).reshape(5)
    for i in range(batch_size-1):
        #X creation
        index = random.randint(0,len(filelistlong)-1)
        filename = filelistlong[index]
        x = np.dstack((x,get_audio_array("LongMixedTape/"+filename)))
        betterx = np.swapaxes(x,0,2)
        y = np.dstack((y,get_vector_label(get_label(filename))))
        bettery = np.swapaxes(y,1,2)
    bettery = bettery.reshape(bettery.shape[1:])
    return betterx, bettery


def test(index):
    x = np.array(get_audio_array("Stream/Stream"+str(index)+".wav"))
    betterx= x[:,:,newaxis]
    betterx = np.swapaxes(betterx, 0,2)
    return betterx
def testlong(index):
    x = np.array(get_audio_array("StreamLong/StreamLong"+str(index)+".wav"))
    betterx= x[:,:,newaxis]
    betterx = np.swapaxes(betterx, 0,2)
    return betterx
def translate(a):
    irecord = 0
    record = a[0][0]
    for x in range(0,5):
        if a[0][x] > record:
            record = a[0][x]
            irecord = x

    if irecord == 0:
        print("No command?")
    elif irecord == 1:
        google()
    elif irecord == 2:
        messenger()
    elif irecord == 3:
        youtube()
    elif irecord == 4:
        gmail()
        
def google():
    os.system("chromium-browser")
def messenger():
    os.system("chromium-browser https://www.messenger.com/t/hillary.tang.00")
def gmail():
    os.system("chromium-browser https://mail.google.com/mail/u/0/#inbox")  
def youtube():
    os.system("chromium-browser https://www.youtube.com/feed/subscriptions")     
    
        
