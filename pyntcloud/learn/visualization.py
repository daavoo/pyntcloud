import numpy as np
from matplotlib import pyplot as plt

def plot_feature_vector(feature_vector, cmap="Oranges"):
    fig, axes= plt.subplots(int(np.ceil(feature_vector.shape[0] / 4)), 4, figsize=(8,20))
    plt.tight_layout()
    for i, ax in enumerate(axes.flat):
        if i >= len(feature_vector):
            break
        ax.imshow(feature_vector[:, :, i], cmap=cmap, interpolation="none")
        ax.set_title("Level " + str(i))