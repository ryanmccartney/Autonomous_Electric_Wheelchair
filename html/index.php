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
	
		<h3>Autonomous Electric Wheelchair Project</h3>
		<p>This project allows full autonomous control of an electric wheelchair. This web interface allows the user to access debug information, issue commands and take manual control of the wheelchair if necessary.</p>
		<p>See the various sections of this interface for further controls.</p>
		
		<hr>

		<h3>Live Stream of Wheelchair Enviroment</h3>
		<div class="stream">
		<img src="http://xavier.local:8080/?action=stream">
		</div>

		<hr>

		<h3>Manual Control of Wheelchair</h3>
		<p>Manual control of the wheelchair is accessible from the menu at the top of this page.</p>
	
		<hr>

		<h3>Emergency Stop</h3>
		<img src="media/Emergency Stop Off.png" style="max-width:80%;height:auto;align:center;" alt="" id="emergency" onclick="changeImage();"/>

		<script>
			var off = "media/Emergency Stop Off.png";
			var	on = "media/Emergency Stop On.png";
			var serialData = "0,0,STOP"
			var sendData = "scripts/serialSend.php?serialData="+ serialData;

			function changeImage(){
				alert(window.document.emergency.src);

				if(document.emergency.src==off){
					document.emergency.src=on;
					sendData('0,0,STOP')				
				}

				else if(document.emergency.src==on){
					document.emergency.src=off;
				}
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

