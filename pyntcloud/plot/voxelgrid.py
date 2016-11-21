
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

        var camera_x = {camera_x};
		var camera_y = {camera_y};
		var camera_z = {camera_z};

        var look_x = {look_x};
        var look_y = {look_y};
        var look_z = {look_z};

		var X = new Float32Array({X});
        var Y = new Float32Array({Y});
        var Z = new Float32Array({Z});

        var R = new Float32Array({R});
        var G = new Float32Array({G});
        var B = new Float32Array({B});

        var S_x = {S_x};
        var S_y = {S_y};
        var S_z = {S_z};

        var n_voxels = {n_voxels};
        var axis_size = {axis_size};

        container = document.getElementById( 'container' );

        scene = new THREE.Scene();

        camera = new THREE.PerspectiveCamera( 90, window.innerWidth / window.innerHeight, 0.1, 1000 );
        camera.position.x = camera_x;
        camera.position.y = camera_y;
        camera.position.z = camera_z;
        camera.up = new THREE.Vector3( 0, 0, 1 );	

        if (axis_size > 0){{
            var axisHelper = new THREE.AxisHelper( axis_size );
		    scene.add( axisHelper );
        }}

        var geometry = new THREE.BoxGeometry( S_x, S_z, S_y );

        for ( var i = 0; i < n_voxels; i ++ ) {{            
            var mesh = new THREE.Mesh( geometry, new THREE.MeshBasicMaterial() );
            mesh.material.color.setRGB(R[i], G[i], B[i]);
            mesh.position.x = X[i];
            mesh.position.y = Y[i];
            mesh.position.z = Z[i];
            scene.add(mesh);
        }}
        
        renderer = new THREE.WebGLRenderer( {{ antialias: false }} );
        renderer.setPixelRatio( window.devicePixelRatio );
        renderer.setSize( window.innerWidth, window.innerHeight );

        controls = new THREE.OrbitControls( camera, renderer.domElement );
        controls.target.copy( new THREE.Vector3(look_x, look_y, look_z) );
        camera.lookAt( new THREE.Vector3(look_x, look_y, look_z));

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


def plot_voxelgrid(v_grid, cmap="Oranges", axis=False):

    scaled_shape = v_grid.shape / min(v_grid.shape)

    # coordinates returned from argwhere are inversed so use [:, ::-1]
    points = np.argwhere(v_grid.vector)[:, ::-1] * scaled_shape

    s_m = plt.cm.ScalarMappable(cmap=cmap)
    rgb = s_m.to_rgba(v_grid.vector.reshape(-1)[v_grid.vector.reshape(-1) > 0])[:,:-1]

    camera_position = points.max(0) + abs(points.max(0))
    look = points.mean(0)
    
    if axis:
        axis_size = points.ptp() * 1.5
    else:
        axis_size = 0

    with open("plotVG.html", "w") as html:
        html.write(TEMPLATE.format( 
            camera_x=camera_position[0],
            camera_y=camera_position[1],
            camera_z=camera_position[2],
            look_x=look[0],
            look_y=look[1],
            look_z=look[2],
            X=points[:,0].tolist(),
            Y=points[:,1].tolist(),
            Z=points[:,2].tolist(),
            R=rgb[:,0].tolist(),
            G=rgb[:,1].tolist(),
            B=rgb[:,2].tolist(),
            S_x=scaled_shape[0],
            S_y=scaled_shape[2],
            S_z=scaled_shape[1],
            n_voxels=sum(v_grid.vector.reshape(-1) > 0),
            axis_size=axis_size))

    return IFrame("plotVG.html",width=800, height=800)
