import os
import torch.utils.data as data
from ..load_3D import load_3D


VALID_EXTENSIONS = [
    'OFF',
    'OBJ',
    'PCD',
    'PLY'
]


def is_3D_file(filename):
    return filename.split(".")[-1].upper() in VALID_EXTENSIONS


def find_classes(dir):
    classes = [d for d in os.listdir(
        dir) if os.path.isdir(os.path.join(dir, d))]
    classes.sort()
    class_to_idx = {classes[i]: i for i in range(len(classes))}
    return classes, class_to_idx


def make_dataset(dir, class_to_idx):
    dataset = []
    for target in os.listdir(dir):
        d = os.path.join(dir, target)
        if not os.path.isdir(d):
            continue

        for root, _, fnames in sorted(os.walk(d)):
            for fname in fnames:
                if is_3D_file(fname):
                    path = os.path.join(root, fname)
                    item = (path, class_to_idx[target])
                    dataset.append(item)

    return dataset


class ClassificationFolder(data.Dataset):

    def __init__(self, root, transform=None, target_transform=None, load_3D_kwargs={}):
        classes, class_to_idx = find_classes(root)
        dataset = make_dataset(root, class_to_idx)

        self.root = root
        self.dataset = dataset
        self.classes = classes
        self.class_to_idx = class_to_idx
        self.transform = transform
        self.target_transform = target_transform
        self.load_3D_kwargs = load_3D_kwargs

    def __getitem__(self, index):
        path, target = self.dataset[index]
        three_dim = load_3D(path, **self.load_3D_kwargs)
        if self.transform is not None:
            three_dim = self.transform(three_dim)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return three_dim, target

    def __len__(self):
        return len(self.dataset)
