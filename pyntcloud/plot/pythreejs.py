

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
