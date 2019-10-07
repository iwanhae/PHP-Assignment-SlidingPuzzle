import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras import Model
import numpy as np
import random

from actionEnum import Action
from memory import Memory, Event


def lossFunction(target, action, predict):
    one_hot = tf.one_hot(action, 4, 1.0, 0.0)
    Q_value = tf.reduce_sum(tf.multiply(predict, one_hot), axis=1)
    cost = tf.reduce_mean(tf.square(target - Q_value))
    return cost


class DQNModel(Model):

    def __init__(self):
        super(DQNModel, self).__init__()
        self.flatten = Flatten()
        self.d1 = Dense(15, activation='relu')
        self.d2 = Dense(15, activation='relu')
        self.d3 = Dense(10, activation='relu')
        self.d4 = Dense(4, activation='relu')
        self.loss_object = tf.keras.losses.SparseCategoricalCrossentropy()
        self.optimizer = tf.keras.optimizers.Adam()

    def train(self, states, actions, targets):
        with tf.GradientTape() as tape:
            predictions = self(states)
            loss = lossFunction(targets, actions, predictions)
            print("Loss", loss)
        gradients = tape.gradient(loss, self.trainable_variables)
        self.optimizer.apply_gradients(
            zip(gradients, self.trainable_variables))

    def test_step(self, state, target):
        predictions = self(state)
        t_loss = self.loss_object(target, predictions)
        return t_loss

    def call(self, x):
        x = self.flatten(x)
        x = self.d1(x)
        x = self.d2(x)
        x = self.d3(x)
        x = self.d4(x)
        return x
