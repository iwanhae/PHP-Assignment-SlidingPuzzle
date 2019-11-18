from bottle import get, post, run, template, request
from pprint import pprint
from puzzle2Map import puzzle2Map
import os, time, math
import tensorflow as tf
import numpy as np
import enum

class Action(enum.Enum):
    NONE = 0
    Up = -1
    Down = 1
    Right = 2
    Left = -2

print("Load model")
model  = tf.keras.models.load_model("model")
print("Load model\tFinished")

ActionTable = {
    0: -2,
    1: -1,
    2: 1,
    3: 2
}

@get('/')
def index():
    return template('<b>Hello {{name}}</b>!', name="World")
@post('/')
def evaluate():
    start = time.time()
    state = np.array(request.json["state"])   # pylint: disable=unsubscriptable-object

    Map = np.array([puzzle2Map(state)])
    Feed = Map.reshape(len(Map), 22, 22, 1)

    Y = model.predict(Feed)[0]
    pprint(Y)
    action = Action(ActionTable[np.argmax(Y)])
    end = time.time()
    return {"action" : action.name, "Y" : Y.tolist(), "time": math.ceil((end-start)*1000)}

run(host='localhost', port=8080)