import sys
import os.path

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../www")

from model import User, Comment, Blog, next_id
blogs = [
        Blog(id='1', name='Test Blog')
    ]

print("asedf")
print(os.path.abspath(__file__))
print(os.path.dirname(os.path.abspath(__file__)))

print(" ==== ")
print((os.path.dirname(os.path.abspath(__file__)) + "../www"))
print((os.path.dirname(os.path.abspath(__file__)) + "/../../www"))
print(" ====2222222222 ")
