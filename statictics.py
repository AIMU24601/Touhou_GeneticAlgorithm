import numpy as np
import matplotlib.pyplot as plt

length = list()
for i in range(5, 115, 5):
    name = "population_gen_"+ str(i) + ".npy"
    print(name)
    a = np.load(name)
    #print(a[0])
    length.append(len(a[0]))
print(length)

x = np.arange(5, 115, 5)

plt.scatter(x, length)
plt.ylabel("Time step")
plt.xlabel("Generation")
plt.show()