

def get_pointcloud_pythreejs(xyz, colors):
    import pythreejs

    points_geometry = pythreejs.BufferGeometry(
        attributes=dict(
            position=pythreejs.BufferAttribute(xyz, normalized=False),
            color=pythreejs.BufferAttribute(list(map(tuple, colors)))))

    points_material = pythreejs.PointsMaterial(
        vertexColors='VertexColors')

    return pythreejs.Points(
        geometry=points_geometry,
        material=points_material)


def get_polylines_pythreejs(polylines):
    import pythreejs
    lines = []
    for x in polylines:
        line_geometry = pythreejs.Geometry(
            vertices=x["vertices"])
        line = pythreejs.Line(
            geometry=line_geometry,
            material=pythreejs.LineBasicMaterial(color=x["color"]),
            type='LinePieces')
        lines.append(line)

    return lines


def get_camera_pythreejs(centroid, xyz, width, height):
    import pythreejs
    camera = pythreejs.PerspectiveCamera(
        fov=90,
        aspect=width / height,
        position=tuple(centroid + [0, abs(xyz.max(0)[1]), abs(xyz.max(0)[2]) * 1.5]),
        up=[0, 0, 1])
    camera.lookAt(tuple(centroid))
    return camera

def get_orbit_controls(camera, centroid):
    import pythreejs
    orbit_controls = pythreejs.OrbitControls(controlling=camera)
    orbit_controls.target = tuple(centroid)
    return orbit_controls

def get_scene():
    pass


def plot_PyntCloud_pythreejs(PyntCloud):
    pass