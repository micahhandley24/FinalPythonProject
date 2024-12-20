import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,2 * 3.14, 100)
y = np.sin(5*x)

plt.plot(x,y)
plt.title("Sine Wave")
plt.grid()
plt.show()