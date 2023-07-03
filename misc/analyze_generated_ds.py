from numpy import load
import numpy as np
import matplotlib.pyplot as plt

x = load('./Results/3-7/7_numchannel-700/generate_dataset/testX_4ms_dummy.npy')
y = load('./Results/3-7/7_numchannel-700/generate_dataset/testY_4ms_dummy.npy')
np.savetxt("testX[0]_4ms_dummy.csv", x[0], delimiter=",")
print('x.shape: ', x.shape)
print('y.shape: ', y.shape)
for i in range(len(y)):
    print('x[i][1]: ', x[i][1])
    print('x[i][0]: ', x[i][0])
    print('y[i]: ', y[i])
    plt.scatter(x[i][1], x[i][0], s=1, c='black')
    plt.xlabel('Time (s)')
    plt.ylabel('Channel')
    plt.title('Label ' + str(y[i]) + ', sample ' + str(i))
    plt.show()
    # plt.savefig('./Results/3-7/6/train_label_' + str(hf['root']['labels'][i]) + '_sample_' + str(i) + '.png')