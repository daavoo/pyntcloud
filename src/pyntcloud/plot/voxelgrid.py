import os
import shutil

import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
try:
    import pythreejs
except ImportError:
    pythreejs = None
try:
    from IPython.display import display
except ImportError:
    display = None
try:
    from IPython.display import IFrame
except ImportError:
    IFrame = None


def get_voxelgrid_pythreejs(xyz, colors):
    vertices = np.array(np.meshgrid([-0.5, 0.5],
                                    [-0.5, 0.5],
                                    [-0.5, 0.5]),
                        dtype=np.float32).T.reshape(-1, 3)
    faces = np.array([[0, 3, 2], [0, 1, 3],   # front
                      [1, 7, 3], [1, 5, 7],   # right
                      [5, 6, 7], [5, 4, 6],   # back
                      [4, 2, 6], [4, 0, 2],   # left
                      [2, 7, 6], [2, 3, 7],   # top
                      [4, 1, 0], [4, 5, 1]],  # bottom
                     dtype=np.uint32)
    colors = pythreejs.InstancedBufferAttribute(array=colors,
                                                meshPerAttribute=3)
    offsets = pythreejs.InstancedBufferAttribute(array=xyz,
                                                 meshPerAttribute=3)

    instanced_geometry = pythreejs.InstancedBufferGeometry(
        attributes={
            "position": pythreejs.BufferAttribute(array=vertices),
            "index": pythreejs.BufferAttribute(array=faces.ravel()),
            "offset": offsets,
            "color": colors,
        })

    material = pythreejs.ShaderMaterial(
        vertexShader='''
    precision highp float;
    attribute vec3 offset;
    varying vec3 vPosition;
    varying vec4 vColor;
    void main(){

        vPosition = position + offset;
        vColor = vec4( color, 1 );
        gl_Position = projectionMatrix * modelViewMatrix * vec4( vPosition, 1.0 );
    }
    ''',
        fragmentShader='''
    precision highp float;
    varying vec4 vColor;
    void main() {
        gl_FragColor = vec4( vColor );
    }
    ''',
        vertexColors='VertexColors',
        transparent=False
    )

    return pythreejs.Mesh(instanced_geometry, material, frustumCulled=False)


def get_centroid_and_camera_position(points):
    centroid = points.mean(0)
    abs_y_max = abs(points.max(0)[1])
    abs_z_max = abs(points.max(0)[2])
    position = tuple(centroid + [0, abs_y_max, abs_z_max * 1.5])

    return centroid, position


def plot_voxelgrid_with_matplotlib(voxelgrid, feature_vector, cmap='Oranges'):
    if plt is None:
        raise ImportError("matplotlib is required for 2d plotting")

    z_dim = voxelgrid.x_y_z[2]
    fig, axes = plt.subplots(int(np.ceil(z_dim / 4)),
                             np.min((z_dim, 4)),
                             figsize=(20, 20))
    plt.tight_layout()
    for i, ax in enumerate(axes.flat if z_dim > 1 else [plt.gca()]):
        if i < z_dim:
            ax.imshow(feature_vector[:, :, i],
                      cmap=cmap,
                      interpolation="nearest")
            ax.set_title("Level " + str(i))
        else:
            ax.axis('off')


def plot_voxelgrid_with_pythreejs(voxel_centers,
                                  voxel_colors,
                                  width,
                                  height,
                                  **kwargs):
    if pythreejs is None:
        raise ImportError("pythreejs is needed for plotting with pythreejs backend.")
    if display is None:
        raise ImportError("IPython is needed for plotting with pythreejs backend.")

    centroid, camera_position = get_centroid_and_camera_position(voxel_centers)
    camera = pythreejs.PerspectiveCamera(fov=90,
                                         aspect=width/height,
                                         position=camera_position,
                                         up=[0, 0, 1])
    mesh = get_voxelgrid_pythreejs(voxel_centers, voxel_colors)
    scene = pythreejs.Scene(children=[camera, mesh], background=None)
    controls = pythreejs.OrbitControls(controlling=camera,
                                       target=tuple(centroid))
    camera.lookAt(tuple(centroid))
    renderer = pythreejs.Renderer(scene=scene,
                                  camera=camera,
                                  controls=[controls],
                                  width=width,
                                  height=height)
    display(renderer)


def plot_voxelgrid(voxelgrid,
                   d=3,
                   mode="binary",
                   backend='pythreejs',
                   cmap='Oranges',
                   **kwargs):
    feature_vector = voxelgrid.get_feature_vector(mode)

    # Plot 2D
    if d == 2:
        return plot_voxelgrid_with_matplotlib(voxelgrid,
                                              feature_vector,
                                              cmap)
    elif d != 3:
        raise ValueError("d must be 2 or 3")

    # Voxelgrid colors
    if mode != 'binary' and plt is None:
        raise ImportError("matplotlib is required for non-binary plotting")
    elif mode != 'binary':
        s_m = plt.cm.ScalarMappable(cmap=cmap)
        flattened = feature_vector.ravel()
        rgba = s_m.to_rgba(flattened[np.nonzero(flattened)])
        voxel_colors = rgba[:, :3].astype(np.float32)
    elif voxelgrid.colors is not None:
        voxel_colors = (voxelgrid.voxel_colors / 255).astype(np.float32)
    else:
        voxel_colors = np.full((voxelgrid.n_voxels, 3), 200, dtype=np.int)

    # Plot 3D
    feature_vector = voxelgrid.get_feature_vector(mode)
    scaled_shape = np.asarray(voxelgrid.shape) / min(voxelgrid.shape)
    voxel_centers = (np.argwhere(feature_vector) * scaled_shape).astype(np.float32)

    if backend == 'pythreejs':
        plot_voxelgrid_with_pythreejs(
            voxel_centers, voxel_colors, **kwargs)
    elif backend == 'threejs':
        plot_voxelgrid_with_threejs(
            voxel_centers, voxel_colors, scaled_shape, **kwargs)
    else:
        raise NotImplementedError("{} backend is not supported".format(backend))
