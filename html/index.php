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
		<h2>Control Interface</h2>
		
		<ul>
			<li><a class="active" href="index.php">Home</a></li>
			<li><a href="auto.php">Autonomous</a></li>
			<li><a href="manual.php">Manual</a></li>
			<li><a href="about.php">About</a></li>
		</ul>
	</div>
	</header>

		
	<div class="content">
	
	<h3>Autonomous Electric Wheelchair Project</h3>
	<p>This project allows full autonomous control of an electric wheelchair. This web interface allows the user to access debug information, issue commands and take manual control of the wheelchair if necessary.</p>
	<p>See the various sections of this interface for further controls.</p>
	
	<div class="stream">
	<img src="http://xavier.local:8080/?action=stream">
	</div>

	<h3>Manual Control of Wheelchair</h3>
	
	
	
	
	<br>
	
	
	<h3>Emergency Stop</h3>
	
	<img onclick="stop" src="media/Emergency Stop Off.png" style="max-width:80%;height:auto;align:center;">
	<br>
	
	
	</div>
	
	<footer>
		
		<br>
		<p>&copy; Copyright 2018, Queen's University Belfast | Ryan McCartney</p>
		<a href="https://www.qub.ac.uk">
		<img src="media/QUB Logo.jpg" style="max-width:8%;height:auto;">
		</a>
		
	</footer>
	
	<script>
		window.onscroll = function() {myFunction()};

		var header = document.getElementById("myHeader");
		var sticky = header.offsetTop;

		function myFunction() {
			if (window.pageYOffset > sticky) {
				header.classList.add("sticky");
			} else {
				header.classList.remove("sticky");
			}
		}
	</script>
	
	</body>

</html> 

