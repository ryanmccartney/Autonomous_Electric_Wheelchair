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
			
			<h2>Home</h2>
		
			<ul>
				<li><a class="active" href="index.php">Home</a></li>
				<li><a href="stream.php">Stream</a></li>
				<li><a href="auto.php">Auto Navigation</a></li>
				<li><a href="manual.php">Manual Navigation</a></li>
				<li><a href="about.php">About</a></li>
				<li><a href="stats.php">Logging</a></li>
			</ul>
		</div>
	</header>
	
	<div>

		<script>
			function getClientHost() {
				  var host = location.hostname;
				  var streamURL = "http://"+host+":8082/?action=stream"; 
				  document.getElementById("videoStream").src = streamURL;
				  document.getElementById("videoLink").href= streamURL;
			}

		window.onload = getClientHost;

		</script>	
	
		<h3>Autonomous Electric Wheelchair Project</h3>
		<p>This project allows full autonomous control of an electric wheelchair. This web interface allows the user to access debug information, issue commands and take manual control of the wheelchair if necessary.</p>
		<p>See the various sections of this interface for further controls.</p>
		
		<hr>

	

		<h3><a id="videoLink" href="http://xavier.local:8082/?action=stream">Live Stream</a> of Wheelchair Enviroment</h3>
		
		<div class="stream">
		
		<img id="videoStream" src="http://xavier.local:8082/?action=stream" width="25%" alt="Image not found" onclick="getClientHost()" onerror="this.onerror=null;this.src='media/nostream.jpg';" />
		</div>

		<hr>

		<h3>Emergency Stop</h3>
		<img src="media/Emergency Stop Off.png" style="max-width:80%;height:auto;align:center;" alt="" id="emergency" onclick="emergency()"/>
		
		<p><b id="status"></b></p>
		<p><b id="batteryPercent"></p>

		<script src="scripts/jquery.min.js"></script>
		<script src="scripts/sendData.js"></script>
		<script>
			var off = "media/Emergency Stop Off.png";
			var	on = "media/Emergency Stop On.png";

			function emergency(){
			
				document.getElementById("emergency").src=on;
				
				//AJAX EMERGENCY COMMAND
				sendData("0,0,STOP");

				//Wait before resetting emergency stop beutton
				window.setTimeout(resetEmergency,1000);

			}

			function resetEmergency(){

				alert("Emergency Stop Activated. Please OK to reset");			
				document.getElementById("emergency").src=off;
				
				//AJAX EMERGENCY RESET COMMAND
				sendData("0,0,RESET");
			}
		</script>
		
	</div>
	
		<footer>
			<br>
			<p>&copy; Copyright 2018, Queen's University Belfast | Ryan McCartney</p>
			<a href="https://www.qub.ac.uk">
			<img src="media/QUB Logo.jpg" style="max-width:8%;height:auto;">
			</a>
		</footer>
	
	</body>
</html> 

