import h5py
import numpy as np
import os

def create_h5_file(file_name, data, labels):
    with h5py.File(file_name, 'w') as file:
        # Create the root group
        root_group = file.create_group('root')

        # Create the spikes group
        spikes_group = root_group.create_group('spikes')

        # Create the times dataset as a compound datatype
        times_dataset = spikes_group.create_dataset('times', data=data['times'], dtype=h5py.special_dtype(vlen=np.dtype('float64')))

        # Create the units dataset as a compound datatype
        units_dataset = spikes_group.create_dataset('units', data=data['units'], dtype=h5py.special_dtype(vlen=np.dtype('int64')))

        # Create the labels dataset
        labels_dataset = root_group.create_dataset('labels', data=labels, dtype='int32')
        
        file.close()

def split_train_test(data_folder, train_ratio=0.95):
    # todo: put two speakers completely in the test set
    all_files = os.listdir(data_folder)
    np.random.seed(45)
    np.random.shuffle(all_files)
    train_files = all_files[:int(train_ratio * len(all_files))]
    test_files = all_files[int(train_ratio * len(all_files)):]

    return train_files, test_files

def create_data_structure(data_folder, train_files, test_files):
    def extract_label(file_name):
        label = file_name.split('_')[-1].split('-')[-1].split('.')[0]
        return int(label)
    
    train_data = {'times': [], 'units': []}
    test_data = {'times': [], 'units': []}
    train_labels = []
    test_labels = []

    for filename in train_files:
        data = np.load(os.path.join(data_folder, filename), allow_pickle=True)
        # indices = np.where(data['arr_0'][1] != 0, data['arr_0'][1])
        # print('indices: ', indices)
        train_data['times'].append(data['arr_0'][0])
        train_data['units'].append(data['arr_0'][1])
        label = extract_label(filename)
        train_labels.append(label)
        # print('label: ', label)
        # print('train_data times: ', train_data['times'])
        # print('train_data units: ', train_data['units'])

    for filename in test_files:
        data = np.load(os.path.join(data_folder, filename), allow_pickle=True)
        # indices = np.where(data['arr_0'] == 1)
        test_data['times'].append(data['arr_0'][0])
        test_data['units'].append(data['arr_0'][1])
        label = extract_label(filename)
        test_labels.append(label)

    return train_data, train_labels, test_data, test_labels

# Set the paths and filenames
# Replace with appropriate path names
data_folder = r'misc/data/num_channel_700'
train_h5_filename = 'shd_train.h5'
test_h5_filename = 'shd_test.h5'

# Split the files into train and test sets
train_files, test_files = split_train_test(data_folder, train_ratio=0.6)
print('train_files: ', train_files)
print('test_files: ', test_files)
print('Number of train files: {}'.format(len(train_files)))
print('Number of test files: {}'.format(len(test_files)))

# Create the data structure for train and test sets
train_data, train_labels, test_data, test_labels = create_data_structure(data_folder, train_files, test_files)
print('train_data: ', len(train_data['times']))
print('train_labels: ', len(train_labels))
print('test_data: ', len(test_data['times']))
print('test_labels: ', len(test_labels))

# Create the train .h5 file
create_h5_file(train_h5_filename, train_data, train_labels)

# Create the test .h5 file
create_h5_file(test_h5_filename, test_data, test_labels)
