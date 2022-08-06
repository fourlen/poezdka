import numpy as np
import random

def generate():
    random.seed(12345)
    return random.randint(0, 1e12)
    return random.choice(list(np.arange(int(1e6))))

print(generate())