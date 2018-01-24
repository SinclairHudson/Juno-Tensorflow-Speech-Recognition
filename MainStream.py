import pyaudio
import wave
import time
import Application
import format
import struct
import AppLong
import tensorflow as tf
FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 0.8
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, output=True,
                    frames_per_buffer=CHUNK)
frames0 = []
frames1 = []
commandframes0 = []
commandframes1 = []
i = 0
LSTM = AppLong.LSTM() #do not reverse, bricks lol
brain = Application.RNN()
halt = 0

while True:
    data = stream.read(CHUNK)
    frames1.append(data)
    frames0.append(data)
    commandframes0.append(data)
    commandframes1.append(data)
    if(len(commandframes0) == 64):
        print("recording ended, processing...")
        waveFile = wave.open("StreamLong/StreamLong0.wav", 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(commandframes0))
        waveFile.close()
        a = LSTM.get_pred(0) #1,5 Array
        format.translate(a)
        print(a)
        
    if(len(commandframes1) == 64):
        print("recording ended, processing...")
        waveFile = wave.open("StreamLong/StreamLong1.wav", 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(commandframes1))
        waveFile.close()
        a = LSTM.get_pred(1) #1,5 Array
        format.translate(a)
        print(a)
        
    if i % 34 == 0:
        if (len(frames0)==34):
            waveFile = wave.open("Stream/Stream0.wav", 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames0))
            waveFile.close()
            print(brain.get_pred(0))
            if(brain.get_pred(0)==0 and halt < 0):
                print("starting recording")
                halt = 80
                commandframes0 = [] #start command frames to be analysed
        frames0 = []
    if (i+17) % 34 == 0:
        if (len(frames1)==34):
            waveFile = wave.open("Stream/Stream1.wav", 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames1))
            waveFile.close()
            print(brain.get_pred(1))
            if(brain.get_pred(1)==0 and halt < 0):
                print("starting recording")
                halt = 80
                commandframes1 = [] #start command frames to be analysed
        frames1 = []      
    i = i + 1
    halt = halt -1
