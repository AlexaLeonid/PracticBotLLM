import random
import string
import numpy as np
import matplotlib.pyplot as plt


def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def draw_graph(x):
    """

    :param x:
    :return:
    sp = plt.subplot(222)
    plt.plot(x, np.cos(x), 'g')
    plt.axis('equal')
    plt.grid(True)
    plt.title(r'$\cos(x)$')
    plt.show()
    """

    x = np.linspace(-5, 5, 100)
    y = numexpr.evaluate(message.text)  # message.text = 'x**2'
    plt.plot(x, y, 'r')
    plt.savefig('plot_name.png', dpi=300)
    bot.send_photo(message.chat.id, photo=open('plot_name.png', 'rb'))
    plt.plot(x, y, 'r')


