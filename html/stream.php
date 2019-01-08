<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">
		<title>Autonomous Wheelchair</title>
		<link rel="shortcut icon" href="media/favicon.ico" />	
		<link rel="stylesheet" href="style/style.css">
		
	</head>

	<body>	
	
 	<header>
		<br>
		<h1>Autonomous Electric Wheelchair</h1>
		
		<div class="header" id="myHeader">
			
			<h2>Camera Streams</h2>
		
			<ul>
				<li><a href="index.php">Home</a></li>
				<li><a class="active"  href="stream.php">Stream</a></li>
				<li><a href="auto.php">Auto Navigation</a></li>
				<li><a href="manual.php">Manual Navigation</a></li>
				<li><a href="about.php">About</a></li>
				<li><a href="stats.php">Logging</a></li>
			</ul>
		</div>
	</header>
	

	<script>
			function getClientHost() {
				  var host = location.hostname;
				  var streamURL = "http://"+host+":8082/?action=stream"; 

				  document.getElementById("floorStream").src = streamURL;
				  document.getElementById("floorStreamLink").href= streamURL;

				  streamURL = "http://"+host+":8081/?action=stream"; 
				  document.getElementById("depthStream").src = streamURL;
				  document.getElementById("depthStreamLink").href= streamURL;

				  streamURL = "http://"+host+":8080/?action=stream"; 
				  document.getElementById("overviewStream").src = streamURL;
				  document.getElementById("overviewStreamLink").href= streamURL;
			}

		window.onload = getClientHost;

	</script>	
	
	<div class="streams">
  		<div class="stream">
		  
		  <h3><a id="overviewStreamLink" href="http://xavier.local:8080/?action=stream">Microsoft Kinect RGB Image</a></h3>
		  <img id="overviewStream" src="http://xavier.local:8080/?action=stream" width="70%" alt="Image not found" onerror="this.onerror=null;this.src='media/nostream.jpg';" />
		  </div>

  		<div class="stream">
		  
		  <h3><a id="depthStreamLink" href="http://xavier.local:8081/?action=stream">Microsoft Kinect Depth Image</a></h3>			
		  <img id="depthStream" src="http://xavier.local:8081/?action=stream" width="70%" alt="Image not found" onerror="this.onerror=null;this.src='media/nostream.jpg';" />
		  </div>

  		<div class="stream">
		  
		  <h3><a id="floorStreamLink" href="http://xavier.local:8082/?action=stream">Webcam Floor Image</a></h3>
		  <img id="floorStream" src="http://xavier.local:8082/?action=stream" width="70%" alt="Image not found" onerror="this.onerror=null;this.src='media/nostream.jpg';" />
		  </div>
	</div>

	<footer>
		<br>
		<p>&copy; Copyright 2018, Queen's University Belfast | Ryan McCartney</p>
		<a href="https://www.qub.ac.uk">
		<img src="media/QUB Logo.jpg" style="max-width:8%;height:auto;">
		</a>	
	</footer>

	<br>
		
	</body>
</html> 

