import requests
from Puzzle import Puzzle, Action
import numpy as np

p = Puzzle(4, 4)
p.data = np.array([[1,2,3,4],
                   [5,6,7,8],
                   [9,10,11,12],
                   [13,14,15,0]])
ans = np.array([[0, 1, 2, 3],
                [4, 5, 6, 7],
                [8, 9, 10, 11],
                [12, 13, 14, 15]])

# p.data = np.array([[7, 2, 6],
#                   [5, 4, 1],
#                   [3, 8, 0]])
# ans = np.array([[0, 1, 2],
#                [3, 4, 5],
#                [6, 7, 8]])

count = 0
while True:
    count += 1
    res = requests.post("http://127.0.0.1:8080",
                        json={"state": p.getArray().tolist()}).json()
    action = Action[res["action"].upper()]
    print(action)

    p.Slide(action)
    print(count)
    print(p.getArray())
    print(res["Y"])
    print()
    if np.abs(ans - p.getArray()).max() == 0:
        break
