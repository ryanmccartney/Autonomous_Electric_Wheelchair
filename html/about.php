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
			
			<h2>Operational Data Logging </h2>
		
			<ul>
				<li><a href="index.php">Home</a></li>
				<li><a href="stream.php">Stream</a></li>
				<li><a href="auto.php">Auto Navigation</a></li>
				<li><a href="manual.php">Manual Navigation</a></li>
				<li><a class="active" href="about.php">About</a></li>
				<li><a href="stats.php">Logging</a></li>
			</ul>
		</div>
	</header>
	
	<div class="content">

	<p>The Autonomous wheelchair project makes use of a number of freely avalible software libraries and tools documented below.</p>
	
	<div class="markdown">
	<?php
		include 'scripts/Parsedown.php';
		
		$file = fopen('readme.html', 'w');

		$html = file_get_contents('README.md');
		$Parsedown = new Parsedown();
		fwrite($file,($Parsedown->text($html)));
	?>
	<iframe src="readme.html" hieght="100%" width="80%" style="border:none; overflow:hidden;"></iframe>
	</div>

	</div>
	
	<footer>
	
	<br>
	<p>&copy; Copyright 2018, Queen's University Belfast | Ryan McCartney</p>
	<a href="https://www.qub.ac.uk"><img src="media/QUB Logo.jpg" style="max-width:8%;height:auto;"></a>
	
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

