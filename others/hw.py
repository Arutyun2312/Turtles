import random
from numpy import exp
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1.0 / (1.0 + exp(-0.2 * x))

def f(x):
    return sigmoid(x - 30)

def g(x):
    return sigmoid(-x + 70)
 
# should plot a point with probability in %
def should_plot(probability):
    max = 100
    return random.randrange(0, max) > (max - probability)


x_values = list(map(lambda n: n / 10, range(0, 1000)))

def plot(probability, function, markersize=2):
    global x_values
    plt.plot(x_values, list(map(lambda x : function(x) if should_plot(probability) else None, x_values)), label='lol', markersize=markersize, marker='o')

plot(100, g)
plot(100, f)
plot(5, lambda x : f(x) + g(x) - 1, 10)
plt.legend(['g(x)', 'f(x)', 'f(x) + g(x) - 1'])

plt.show()
