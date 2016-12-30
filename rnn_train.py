"""
Given a saved output of predictions or pooled features from our CNN,
train an RNN (LSTM) to examine temporal dependencies.
"""
from collections import deque
from rnn_utils import get_network, get_data
from sklearn.model_selection import train_test_split
from tflearn.data_utils import to_categorical
from random import shuffle
import tflearn
import numpy as np
import pickle
import sys

def main(filename, frames, batch_size, num_classes, input_length):
    """From the blog post linked above."""
    # Get our data.
    X_train, X_test, y_train, y_test = get_data(filename, frames, num_classes, input_length)

    # Get sizes.
    num_classes = len(y_train[0])

    # Get our network.
    net = get_network(frames, input_length, num_classes)

    # Train the model.
    model = tflearn.DNN(net, tensorboard_verbose=0)
    model.fit(X_train, y_train, validation_set=(X_test, y_test),
              show_metric=True, batch_size=batch_size, snapshot_step=100)

    # Save it.
    model.save('rnn.tflearn')

if __name__ == '__main__':
    filename = 'data/cnn-features-frames-1.pkl'
    frames = 40
    batch_size = 32
    num_classes = 2
    input_length = 2048

    main(filename, frames, batch_size, num_classes, input_length)
