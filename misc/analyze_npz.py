from numpy import load
import numpy as np
import matplotlib.pyplot as plt

data = load('./Results/26-6/lang-english_speaker-00_trial-0_digit-3.npz')
np.savetxt("example_npz.csv", data['arr_0'], delimiter=",")

print('data.files: ', data.files)
lst = data.files
for item in lst:
    print(item)
    print(data[item])

plt.plot(data['arr_0'][0], data['arr_0'][1], ls="none", marker=".", color="black")
plt.show()   