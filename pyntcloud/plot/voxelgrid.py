
import numpy as np

from IPython.display import IFrame
from matplotlib import pyplot as plt

TEMPLATE = """
<!DOCTYPE html>
<head>

<title>PyntCloud</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">
<style>
    body {{
        color: #cccccc;font-family: Monospace;
        font-size: 13px;
        text-align: center;
        background-color: #050505;
        margin: 0px;
        overflow: hidden;
    }}
    #logo_container {{
        position: absolute;
        top: 0px;
        width: 100%;
    }}
    .logo {{
        max-width: 20%;
    }}
</style>

</head>
<body>

<div>
    <img class="logo" src="https://media.githubusercontent.com/media/daavoo/pyntcloud/master/docs/data/pyntcloud.png">
</div>

<div id="container">
</div>

<script src="http://threejs.org/build/three.js"></script>
<script src="http://threejs.org/examples/js/Detector.js"></script>
<script src="http://threejs.org/examples/js/controls/OrbitControls.js"></script>
<script src="http://threejs.org/examples/js/libs/stats.min.js"></script>

<script>

    if ( ! Detector.webgl ) Detector.addGetWebGLMessage();

    var container, stats;
    var camera, scene, renderer;
    var points;

    init();
    animate();

    function init() {{

        container = document.getElementById( 'container' );

        camera = new THREE.PerspectiveCamera( 90, window.innerWidth / window.innerHeight, 0.1, 1000 );
        camera.position.x = {camera_x};
        camera.position.y = {camera_y};
        camera.position.z = {camera_z};

        var X = new Float32Array({X});
        var Y = new Float32Array({Y});
        var Z = new Float32Array({Z});

        var R = new Float32Array({R});
        var G = new Float32Array({G});
        var B = new Float32Array({B});

        scene = new THREE.Scene();

        var geometry = new THREE.BoxGeometry( {S_x}, {S_y}, {S_z} );
        for ( var i = 0; i < {n_voxels}; i ++ ) {{            

            var mesh = new THREE.Mesh( geometry, new THREE.MeshBasicMaterial( {{opacity:0.8, transparent:true}}) );
            mesh.material.color.setRGB(R[i], G[i], B[i]);

            mesh.position.x = X[i];
            mesh.position.y = Y[i];
            mesh.position.z = Z[i];

            scene.add(mesh);
        }}
        
        var axis_size = {axis_size};
        var axis_x = {axis_x};
        var axis_y = {axis_y};
        var axis_z = {axis_z};

        var x_geometry = new THREE.Geometry();
        x_geometry.vertices.push(new THREE.Vector3(axis_x, axis_y, axis_z));
        x_geometry.vertices.push(new THREE.Vector3(axis_x + axis_size, axis_y, axis_z));
        var x_material = new THREE.LineBasicMaterial({{
            color: 0xff0000
        }});
        var x_axis = new THREE.Line(x_geometry, x_material);
        scene.add(x_axis);

        var y_geometry = new THREE.Geometry();
        y_geometry.vertices.push(new THREE.Vector3(axis_x, axis_y, axis_z));
        y_geometry.vertices.push(new THREE.Vector3(axis_x, axis_y + axis_size, axis_z));
        var y_material = new THREE.LineBasicMaterial({{
            color: 0x0000ff
        }});
        var y_axis = new THREE.Line(y_geometry, y_material);
        scene.add(y_axis);

        var z_geometry = new THREE.Geometry();
        z_geometry.vertices.push(new THREE.Vector3(axis_x, axis_y, axis_z));
        z_geometry.vertices.push(new THREE.Vector3(axis_x, axis_y, axis_z + axis_size));
        var z_material = new THREE.LineBasicMaterial({{
            color: 0x00ff00
        }});
        var z_axis = new THREE.Line(z_geometry, z_material);
        scene.add(z_axis);


        renderer = new THREE.WebGLRenderer( {{ antialias: false }} );
        renderer.setPixelRatio( window.devicePixelRatio );
        renderer.setSize( window.innerWidth, window.innerHeight );

        controls = new THREE.OrbitControls( camera, renderer.domElement );

        container.appendChild( renderer.domElement );

        window.addEventListener( 'resize', onWindowResize, false );
    }}

    function onWindowResize() {{
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize( window.innerWidth, window.innerHeight );
    }}

    function animate() {{
        requestAnimationFrame( animate );
        render();
    }}

    function render() {{
        renderer.render( scene, camera );
    }}
</script>
</body>
</html>
"""


def plot_voxelgrid(v_grid, cmap="hsv", axis=True):

    scaled_shape = v_grid.shape / min(v_grid.shape)

    n_x = int(len(v_grid.segments[0]) - 1)
    n_y = int(len(v_grid.segments[1]) - 1)
    n_z = int(len(v_grid.segments[2]) - 1)

    # get nonzero voxels / swap y-z
    points = (np.argwhere(v_grid.vector.reshape(n_z,n_y,n_x)) * scaled_shape[::-1])[:,[2,0,1]]
    points[:,-1] *= -1

    s_m = plt.cm.ScalarMappable(cmap=cmap)

    rgb = s_m.to_rgba(v_grid.vector[v_grid.vector > 0])[:,:-1]

    camera_position = points.max(0) + abs(points.max(0))
    
    if axis:
        axis_size = points.ptp() * 1.5
        axis_position = points.min(0) - scaled_shape / 2
    else:
        axis_size = 0

    with open("plotVG.html", "w") as html:
        html.write(TEMPLATE.format( camera_x=camera_position[0],
                                    camera_y=camera_position[1],
                                    camera_z=camera_position[2],
                                    X=points[:,0].tolist(),
                                    Y=points[:,1].tolist(),
                                    Z=points[:,2].tolist(),
                                    R=rgb[:,0].tolist(),
                                    G=rgb[:,1].tolist(),
                                    B=rgb[:,2].tolist(),
                                    S_x=scaled_shape[0],
                                    S_y=scaled_shape[2],
                                    S_z=scaled_shape[1],
                                    n_voxels=sum(v_grid.vector > 0),
                                    axis_size=axis_size,
                                    axis_x=axis_position[0],
                                    axis_y=axis_position[1],
                                    axis_z=axis_position[2]))
    return IFrame("plotVG.html",width=800, height=800)

