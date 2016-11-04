
from IPython.display import IFrame

import numpy as np
TEMPLATE = """
<!DOCTYPE html>
<head>

<title>PyntCloud</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">
<style>
body {{
	color: #cccccc;
	font-family: Monospace;
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

		var positions = new Float32Array({positions});

		var colors = new Float32Array({colors});

		var points_size = {points_size};

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

		var geometry = new THREE.BufferGeometry();
		geometry.addAttribute( 'position', new THREE.BufferAttribute( positions, 3 ) );
		geometry.addAttribute( 'color', new THREE.BufferAttribute( colors, 3 ) );
		geometry.computeBoundingSphere();

		var material = new THREE.PointsMaterial( {{ size: points_size, vertexColors: THREE.VertexColors }} );

		points = new THREE.Points( geometry, material );
		scene.add( points );


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

def plot_points(xyz, colors=None, size=0.1, axis=True):

	positions = xyz.reshape(-1).tolist()

	camera_position = xyz.max(0) + abs(xyz.max(0))

	look = xyz.mean(0)

	if colors is None:
		colors = [1,0.5,0] * len(positions)

	elif len(colors.shape) > 1:
		colors = colors.reshape(-1).tolist()

	if axis:
		axis_size = xyz.ptp() * 1.5
	else:
		axis_size = 0

	with open("plot_points.html", "w") as html:
		html.write(TEMPLATE.format(
			camera_x=camera_position[0],
			camera_y=camera_position[1],
			camera_z=camera_position[2],
			look_x=look[0],
            look_y=look[1],
            look_z=look[2],
			positions=positions,
			colors=colors,
			points_size=size,
			axis_size=axis_size))

	return IFrame("plot_points.html",width=800, height=800)
