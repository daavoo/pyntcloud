
from IPython.display import IFrame

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

		container = document.getElementById( 'container' );

		camera = new THREE.PerspectiveCamera( 90, window.innerWidth / window.innerHeight, 0.1, 1000 );
		camera.position.x = {camera_x};
		camera.position.y = {camera_y};
		camera.position.z = {camera_z};

		scene = new THREE.Scene();

		var geometry = new THREE.BufferGeometry();

		var positions = new Float32Array({positions});
		var colors = new Float32Array({colors});

		geometry.addAttribute( 'position', new THREE.BufferAttribute( positions, 3 ) );
		geometry.addAttribute( 'color', new THREE.BufferAttribute( colors, 3 ) );
		geometry.computeBoundingSphere();

		var material = new THREE.PointsMaterial( {{ size: {points_size}, vertexColors: THREE.VertexColors }} );

		points = new THREE.Points( geometry, material );

		scene.add( points );

		var axis_size = {axis_size};
		var axis_x = {axis_x};
		var axis_y = {axis_y};
		var axis_z = {axis_z};

		var x_geometry = new THREE.Geometry();
		x_geometry.vertices.push(new THREE.Vector3(axis_x, axis_y, axis_z));
		x_geometry.vertices.push(new THREE.Vector3(axis_x + axis_size, axis_y, axis_z));
		var x_material = new THREE.LineBasicMaterial({{ color: 0xff0000 }});
		var x_axis = new THREE.Line(x_geometry, x_material);
		scene.add(x_axis);

		var y_geometry = new THREE.Geometry();
		y_geometry.vertices.push(new THREE.Vector3(axis_x, axis_y, axis_z));
		y_geometry.vertices.push(new THREE.Vector3(axis_x, axis_y + axis_size, axis_z));
		var y_material = new THREE.LineBasicMaterial({{ color: 0x0000ff }});
		var y_axis = new THREE.Line(y_geometry, y_material);
		scene.add(y_axis);

		var z_geometry = new THREE.Geometry();
		z_geometry.vertices.push(new THREE.Vector3(axis_x, axis_y, axis_z));
		z_geometry.vertices.push(new THREE.Vector3(axis_x, axis_y, axis_z + axis_size));
		var z_material = new THREE.LineBasicMaterial({{color: 0x00ff00}});
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

def plot_points(xyz, colors=None, size=0.1, axis=True):
	# swap y-z
	points = xyz[:,[0,2,1]]
	points[:,-1] *= -1


	positions = points.reshape(-1).tolist()
	camera_position = points.max(0) + abs(points.max(0))

	if colors is None:
		colors = [1,0.5,0] * len(positions)

	elif len(colors.shape) > 1:
		colors = colors.reshape(-1).tolist()

	if axis:
		axis_size = points.ptp() * 1.5
		axis_position = points.min(0)
	else:
		axis_size = 0

	with open("plot_points.html", "w") as html:
		html.write(TEMPLATE.format(
			camera_x=camera_position[0],
			camera_y=camera_position[1],
			camera_z=camera_position[2],
			positions=positions,
			colors=colors,
			points_size=size,
			axis_size=axis_size,
			axis_x=axis_position[0],
			axis_y=axis_position[1],
			axis_z=axis_position[2]))

	return IFrame("plot_points.html",width=800, height=800)
