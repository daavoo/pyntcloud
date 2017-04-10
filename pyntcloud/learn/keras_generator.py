import os
import threading

import numpy as np

from keras import backend as K

from .load_3D import load_3D
from .transforms import(
    apply_offset,
    apply_transform,
    combine_transforms,  
    flip_axis,                 
    Rx,
    Ry,
    Rz,
    shift_voxels
)        

class VoxelGridDataGenerator(object):
    """Generate minibatches of 3D data data with real-time data augmentation.

    Parameters
    ----------
    x_rotation_range : float, optional (Default None)
        Rotation range in Degrees (0-180) along the x axis.
        Equivalent to 'Roll' in aircraft principal axis.
        
    y_rotation_range : float, optional (Default None)
        Rotation range in Degrees (0-180) along the y axis.
        Equivalent to 'Pitch' in aircraft principal axis.
        
    z_rotation_range : float, optional (Default None)
        Rotation range in Degrees (0-180) along the z axis.
        Equivalent to 'Yaw' in aircraft principal axis.
    
    x_shift_voxel_range : uint, optional (Default None)
        Number of voxels to be shifted along x axis.
        
    y_shift_voxel_range : uint, optional (Default None)
        Number of voxels to be shifted along y axis.
        
    z_shift_voxel_range : uint, optional (Default None)
        Number of voxels to be shifted along z axis.
    
    x_flip : bool, optional (Default False)
        Flip around x axis with random probability
        
    y_flip : bool, optional (Default False)
        Flip around y axis with random probability
    
    z_flip : bool, optional (Default False)
        Flip around z axis with random probability
        
    data_format: str in {'channels_first', 'channels_last'} optional (Default None)
        In 'channels_first' mode, the channels dimension (the depth) is at index 1.
        In 'channels_last' mode it is at index 4.
        It defaults to the `image_data_format` value found in your Keras config
        file at `~/.keras/keras.json`.
        If you never set it, then it will be "channels_last".
    """

    def __init__(self,
                 x_rotation_range=None,
                 y_rotation_range=None,
                 z_rotation_range=None,
                 x_shift_voxel_range=None,
                 y_shift_voxel_range=None,
                 z_shift_voxel_range=None,
                 x_flip=False,
                 y_flip=False,
                 z_flip=False,
                 fill_mode='constant',
                 cval=0.,
                 data_format=None):
        
        if data_format is None:
            data_format = K.image_data_format()
            
        if data_format not in {'channels_last', 'channels_first'}:
            raise ValueError('data_format should be "channels_last" (channel after x , y, z '
                             'or "channels_first" (channel before x, y, z). '
                             'Received arg: ', data_format)
        
        if data_format == 'channels_first':
            self.channel_axis = 1
            self.x_axis = 2
            self.y_axis = 3
            self.z_axis = 4
            
        if data_format == 'channels_last':
            self.x_axis = 1
            self.y_axis = 2
            self.z_axis = 3
            self.channel_axis = 4
            
        self.data_format = data_format
        self.fill_mode = fill_mode
        self.cval = cval
        
        self.x_rotation_range = x_rotation_range
        self.y_rotation_range = y_rotation_range
        self.z_rotation_range = z_rotation_range
        
        self.x_shift_voxel_range = x_shift_voxel_range
        self.y_shift_voxel_range = y_shift_voxel_range
        self.z_shift_voxel_range = z_shift_voxel_range
        
        self.x_flip = x_flip
        self.y_flip = y_flip
        self.z_flip = z_flip

    def flow_from_directory(self, 
                            directory,
                            n_sampling=None,
                            target_size=(32,32,32),
                            voxel_mode="binary",
                            classes=None, 
                            class_mode='categorical',
                            batch_size=32, 
                            shuffle=True, 
                            seed=None,
                            save_to_dir=None,
                            save_prefix='',
                            save_format='npy',
                            follow_links=False):
        
        return DirectoryIterator(
             directory,
             self,
             n_sampling=None,
             target_size=target_size,
             classes=classes, 
             class_mode=class_mode,
             data_format=self.data_format,
             batch_size=batch_size,
             shuffle=shuffle,
             seed=seed,
             save_to_dir=save_to_dir,
             save_prefix=save_prefix,
             save_format=save_format,
             follow_links=follow_links)

    def random_transform(self, voxelgrid):
        # x is a single VoxelGrid, so it doesn't have number at index 0
        x_axis = self.x_axis - 1
        y_axis = self.y_axis - 1
        z_axis = self.z_axis - 1
        channel_axis = self.channel_axis - 1
        
        x, y, z = voxelgrid.shape[x_axis], voxelgrid.shape[y_axis], voxelgrid.shape[z_axis]

        transforms = []

        if self.x_rotation_range is not None:
            theta = np.random.uniform(-self.x_rotation_range, self.x_rotation_range)
            transforms.append(Rx(theta, degrees=True))
            
        if self.y_rotation_range is not None:
            theta = np.random.uniform(-self.y_rotation_range, self.y_rotation_range)
            transforms.append(Ry(theta, degrees=True))
        
        if self.z_rotation_range is not None:
            theta = np.random.uniform(-self.z_rotation_range, self.z_rotation_range)
            transforms.append(Rz(theta, degrees=True))
        
        tx = 0
        ty = 0
        tz = 0
        
        if self.x_shift_voxel_range is not None:
            tx = np.random.uniform(-self.x_shift_voxel_range, self.x_shift_voxel_range)
        
        if self.y_shift_voxel_range is not None:
            ty = np.random.uniform(-self.y_shift_voxel_range, self.y_shift_voxel_range)
        
        if self.z_shift_voxel_range is not None:
            tz =  np.random.uniform(-self.z_shift_voxel_range, self.z_shift_voxel_range)
        
        transforms.append(shift_voxels(tx, ty, tz))
        
        final_transform = apply_offset(combine_transforms(transforms), x, y, z)
        
        voxelgrid = apply_transform(voxelgrid, final_transform, channel_axis, fill_mode=self.fill_mode, cval=self.cval)
        
        if self.x_flip:
            if np.random.random() < 0.5:
                voxelgrid = flip_axis(voxelgrid, x_axis)

        if self.y_flip:
            if np.random.random() < 0.5:
                voxelgrid = flip_axis(voxelgrid, y_axis)
                
        if self.z_flip:
            if np.random.random() < 0.5:
                voxelgrid = flip_axis(voxelgrid, z_axis)

        return voxelgrid


class Iterator(object):

    def __init__(self, n, batch_size, shuffle, seed):
        self.n = n
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.batch_index = 0
        self.total_batches_seen = 0
        self.lock = threading.Lock()
        self.index_generator = self._flow_index(n, batch_size, shuffle, seed)

    def reset(self):
        self.batch_index = 0

    def _flow_index(self, n, batch_size=32, shuffle=False, seed=None):
        # ensure self.batch_index is 0
        self.reset()
        while 1:
            if seed is not None:
                np.random.seed(seed + self.total_batches_seen)
            if self.batch_index == 0:
                index_array = np.arange(n)
                if shuffle:
                    index_array = np.random.permutation(n)

            current_index = (self.batch_index * batch_size) % n
            if n >= current_index + batch_size:
                current_batch_size = batch_size
                self.batch_index += 1
            else:
                current_batch_size = n - current_index
                self.batch_index = 0
            self.total_batches_seen += 1
            yield (index_array[current_index: current_index + current_batch_size],
                   current_index, current_batch_size)

    def __iter__(self):
        # needed if we want to do something like:
        # for x, y in data_gen.flow(...):
        return self

    def __next__(self, *args, **kwargs):
        return self.next(*args, **kwargs)


class DirectoryIterator(Iterator):

    def __init__(self, 
                 directory, 
                 voxelgrid_data_generator,
                 n_sampling=None,
                 target_size=(32,32,32),
                 voxel_mode="binary",
                 data_format=None,
                 classes=None, 
                 class_mode='categorical',
                 batch_size=32, 
                 shuffle=True, 
                 seed=None,
                 save_to_dir=None,
                 save_prefix='',
                 save_format='npy',
                 follow_links=False):
        
        if data_format is None:
            data_format = K.image_data_format()
            
        self.directory = directory
        self.voxelgrid_data_generator = voxelgrid_data_generator
        self.voxel_mode = voxel_mode
        self.target_size = tuple(target_size)
        self.n_sampling = n_sampling

        if data_format == 'channels_first':
            self.voxelgrid_shape = (1,) + self.target_size
        else:
            self.voxelgrid_shape = self.target_size + (1,)

        self.classes = classes
        if class_mode not in {'categorical', 'binary', 'sparse', None}:
            raise ValueError('Invalid class_mode:', class_mode,
                             '; expected one of "categorical", '
                             '"binary", "sparse", or None.')
            
        self.class_mode = class_mode
        self.save_to_dir = save_to_dir
        self.save_prefix = save_prefix
        self.save_format = save_format

        valid_formats = {'MAT', 'NPY', 'NPZ', 'OBJ', 'PLY', 'OFF'}

        if classes is None:
            classes = []
            for subdir in sorted(os.listdir(directory)):
                if os.path.isdir(os.path.join(directory, subdir)):
                    classes.append(subdir)
                    
        self.nb_class = len(classes)
        self.class_indices = dict(zip(classes, range(len(classes))))
        
        # first, count the number of samples and classes
        self.samples = 0
        def _recursive_list(subpath):
            return sorted(os.walk(subpath, followlinks=follow_links), key=lambda tpl: tpl[0])

        for subdir in classes:
            subpath = os.path.join(directory, subdir)
            for root, _, files in _recursive_list(subpath):
                for fname in files:
                    ext = fname.split(".")[-1].upper() 
                    if ext in valid_formats:
                        self.samples += 1
                        
        print('Found {} 3D files belonging to {} classes.'.format(self.samples, self.nb_class))

        # second, build an index of the images in the different class subfolders
        self.filenames = []
        self.classes = np.zeros((self.samples,), dtype='int32')
        i = 0
        for subdir in classes:
            subpath = os.path.join(directory, subdir)
            for root, _, files in _recursive_list(subpath):
                for fname in files:
                    ext = fname.split(".")[-1].upper() 
                    if ext in valid_formats:
                        self.classes[i] = self.class_indices[subdir]
                        i += 1
                        # add filename relative to directory
                        absolute_path = os.path.join(root, fname)
                        self.filenames.append(os.path.relpath(absolute_path, directory))
                        
        super(DirectoryIterator, self).__init__(self.samples, batch_size, shuffle, seed)

    def next(self):
        with self.lock:
            index_array, current_index, current_batch_size = next(self.index_generator)
        # The transformation of images is not under thread lock
        # so it can be done in parallel
        batch_x = np.zeros((current_batch_size,) + self.voxelgrid_shape, dtype=K.floatx())

        # build batch of image data
        for i, j in enumerate(index_array):
            fname = self.filenames[j]
            voxelgrid = load_3D(os.path.join(self.directory, fname),
                                n_sampling=self.n_sampling,
                                target_size=self.target_size,
                                voxel_mode=self.voxel_mode)
            
            voxelgrid = voxelgrid.reshape(self.voxelgrid_shape)
            
            voxelgrid = self.voxelgrid_data_generator.random_transform(voxelgrid)
            batch_x[i] = voxelgrid

        # optionally save augmented images to disk for debugging purposes
        if self.save_to_dir:
            for i in range(current_batch_size):
                v = batch_x[i].reshape(self.target_size)
                fname = '{prefix}_{index}_{hash}.{format}'.format(prefix=self.save_prefix,
                                                                  index=current_index + i,
                                                                  hash=np.random.randint(1e4),
                                                                  format=self.save_format)
                np.save(os.path.join(self.save_to_dir, fname), v)
                
        # build batch of labels
        if self.class_mode == 'sparse':
            batch_y = self.classes[index_array]
        elif self.class_mode == 'binary':
            batch_y = self.classes[index_array].astype(K.floatx())
        elif self.class_mode == 'categorical':
            batch_y = np.zeros((len(batch_x), self.nb_class), dtype=K.floatx())
            for i, label in enumerate(self.classes[index_array]):
                batch_y[i, label] = 1.
        else:
            return batch_x
        return batch_x, batch_y