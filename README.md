# Juno-Tensorflow-Speech-Recognition

This repo is my first dive into a large Tensorflow Voice Recognition Process, created to be a personal assistant similar to Amazon Alexa or Google Assistant.
##Dependencies
Tensorflow
TFLearn
librosa
skikit-image
numpy
pyaudio (portaudio)

## The Current Process
1. Start a stream of audio, recording overlapping instances of 0.8 second recordings
2. Save this stream of audio to a .wav file and instantly run it through a RNN
3. This RNN Classifes the audio as either silence, talking, or a call for it's name, "Juno"
4. If RNN predicts that its name has been called, it instantly starts recording a longer audio clip from the audio stream.
5. That longer audio clip is then put through a LSTM neural network classifier to classify the sound right after the name being called as "YouTube", "Messenger", "Google", "Gmail", or silence, no command.
6. The command mapped to one of these outputs is then executed.

## Current Goals
1. Make the RNN initial classifier way more accurate. Currently there are a lot of false positives, with random noise. Possibly need to change the Neural Network structure, dataset, training time, training variables, etc. It needs to have less of a tolerance for its name being called.
2. Add more functions, for more functionality

## Long-Term Goals
1. Get analysis for full sentence commands, such as "what is the weather today?" This will need some large NLP, as well as a much better NLP process, to accurately predict the full sentence instead of just the word.
2. Get the whole project onto a RPi3, for portability and usability even when the main PC is off.
