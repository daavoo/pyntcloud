
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
				
				camera = new THREE.PerspectiveCamera( 90, window.innerWidth / window.innerHeight, 1, 1000 );
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

				var material = new THREE.PointsMaterial( {{ size: 0.1, vertexColors: THREE.VertexColors }} );

				points = new THREE.Points( geometry, material );

				scene.add( points );
				
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

def plot3D(xyz, colors=None):

    positions = (xyz - xyz.mean(0)).reshape(-1).tolist()
    camera_position = xyz.max(0) + abs(xyz.max(0))

    if colors is None:
        colors = [255,0,0] * len(positions)
    
    elif len(colors.shape) > 1:
        colors = colors.reshape(-1).tolist()

    with open("plot3D.html", "w") as html:
        html.write(TEMPLATE.format(camera_x=camera_position[0],
									camera_y=camera_position[1],
									camera_z=camera_position[2],
									positions=positions,
									colors=colors))

    return IFrame("plot3D.html",width=800, height=800)
