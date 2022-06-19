import numpy as np
import matplotlib.pyplot as plt

mean = list()
deviation = list()
for i in range(1, 25, 1):
    name = "stats_gen_"+ str(i) + ".npy"
    a = np.load(name)
    mean.append(a)
print("mean: {}".format(mean))

x = np.arange(1, 25, 1)

plt.scatter(x, mean)
plt.ylabel("Time step")
plt.xlabel("Generation")
plt.show()