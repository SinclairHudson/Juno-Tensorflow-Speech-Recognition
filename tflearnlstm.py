import tflearn
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import format
saveDIR = "/media/sinclair/SINCLAIR32/TestZone/Models"
learning_rate = 0.0001
training_iters = 30000  # steps
batch_size = 64

height = 128  # number of frequencies measured
length = 59  # (max) length of utterance ?length of the sample
classes = 5  # google, messenger, youtube, gmail, silence

i = 0

# Network building
net = tflearn.input_data([None, length, height])
net = tflearn.lstm(net, 128*4, dropout=0.5)
net = tflearn.fully_connected(net, classes, activation='softmax')
net = tflearn.regression(net, optimizer='adam', learning_rate=learning_rate, loss='categorical_crossentropy')
model = tflearn.DNN(net, tensorboard_verbose=0)

## add this "fix" for tensorflow version errors
for x in tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES): tf.add_to_collection(tf.GraphKeys.VARIABLES, x )
# Training
test_batch_x, test_batch_y = format.get_batch_long(100)
while i < training_iters:
        i = i+1
        trainX, trainY = format.get_batch_long(64)
        model.fit(trainX, trainY, n_epoch=100, validation_set=(test_batch_x, test_batch_y),
                  show_metric=True, batch_size=batch_size)
        model.save("Longmodels/tflearnlstm.model")
