import h5py
import numpy as np
import matplotlib.pyplot as plt

hf = h5py.File('./Results/3-7/7_numchannel-700/shd_test.h5', 'r')
print(hf.keys())
# # My data
print(hf['root'].keys())
print(hf['root']['spikes'].keys())
print(hf['root']['spikes']['times'].shape)
print(hf['root']['spikes']['units'].shape)
print(hf['root']['labels'])
units = np.array(hf.get('root').get('spikes').get('units'))
times = np.array(hf.get('root').get('spikes').get('times'))

# # OG data
# print(hf['labels'].shape)
# print(hf['spikes'].keys())
# units = np.array(hf.get('spikes').get('units'))
# times = np.array(hf.get('spikes').get('times'))
# np.savetxt("og_test_times.csv", times, delimiter=",")

print(len(units))
print(len(times))
for i in range(len(units)):
    print('units: ', len(units[i]))
    print('times: ', len(times[i]))
    plt.scatter(times[i], units[i], s=1, c='black')
    plt.xlabel('Time (s)')
    plt.ylabel('Channel')
    plt.title('Label ' + str(hf['root']['labels'][i]) + ', sample ' + str(i))
    plt.savefig('./Results/3-7/7_numchannel-700/test_label_' + str(hf['root']['labels'][i]) + '_sample_' + str(i) + '.png') 
    plt.show()
