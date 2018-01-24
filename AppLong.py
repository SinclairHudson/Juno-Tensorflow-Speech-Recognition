import tflearn
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import format
class LSTM:
    def __init__(self):
        print("Starting LSTM")
        saveDIR = "/media/sinclair/SINCLAIR32/TestZone/Models"
        learning_rate = 0.0001
        training_iters = 300000  # steps
        batch_size = 64

        height = 128  # number of frequencies measured
        length = 59  # (max) length of utterance ?length of the sample
        classes = 5  # google, messenger, youtube, gmail, silence


        # Network building
        net = tflearn.input_data([None, length, height])
        net = tflearn.lstm(net, 128*4, dropout=0.5)
        net = tflearn.fully_connected(net, classes, activation='softmax')
        net = tflearn.regression(net, optimizer='adam', learning_rate=learning_rate, loss='categorical_crossentropy')
        self.model = tflearn.DNN(net, tensorboard_verbose=0)

        for x in tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES): tf.add_to_collection(tf.GraphKeys.VARIABLES, x )
        self.model.load("LongModels/tflearnlstm.model")
        print("jacked up and good to go!")
    def get_pred(self,index):
        test_x=format.testlong(index)
        return self.model.predict(test_x)
