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
				<li><a href="about.php">About</a></li>
				<li><a class="active" href="stats.php">Logging</a></li>
			</ul>
		</div>
	</header>
	
	<h3>Command Buttons</h3>
	
	<p>
	<form  method="get" name="stop" action="scripts/serialSend.php">
    <input type="hidden" name="serialData" value="0,0,STOP" >
    <input type="submit" value="Stop Wheelchair" >
	</form>
	</p>
	
	<p>
	<form  method="get" name="update" action="scripts/serialSend.php">
    <input type="hidden" name="serialData" value="0,0,SEND" >
    <input type="submit" value="Update Variables" >
	</form>
	</p>
	
	<p>
	<form  method="get" name="reset" action="scripts/serialSend.php">
    <input type="hidden" name="serialData" value="0,0,RESET" >
    <input type="submit" value="Reset Controller" >
	</form>
	</p>
	
	<p>
	<form  method="get" name="brake" action="scripts/serialSend.php">
    <input type="hidden" name="serialData" value="0,0,BRAKEOFF" >
    <input type="submit" value="Release Brakes" >
	</form>
	</p>

	<hr>
		
	<h3>Logs of Recieved Data from Controller</h3>
	
	<p>
	Logged Operational Data from the Wheelchair controller appears below. Follow 
	<a href="scripts/receivedData.txt" download> this link</a> to download a copy of this data.</p>
	
	<p><div id="logfile">

  	<p><iframe src="scripts/receivedData.txt" frameborder="1" height="600" width="90%"></iframe></p>
	
	</div>
	</p>

	<hr>

	<h3>Logs of Data Transmitted to Controller</h3>
	
	<p>
	Logged control commands that have been sent to the Wheelchair controlloer appear below. Follow 
	<a href="scripts/transmittedData.txt" download> this link</a> to download a copy of this data. Note that this data is time
	stapmed in the same instance of the above logs.</p>
	
	<p><div id="logfile">

  	<p><iframe src="scripts/transmittedData.txt" frameborder="1" height="600" width="90%"></iframe></p>
	
	</div>
	</p>

	<hr>

	<h3>Debug Data</h3>
	
	<p><b>PHP executing as: </b><?php echo exec('whoami');?></p>
	
	<p><b>Joystick Output: </b><i id="result"></i></p>
	
	<p><b>Data sent to serial line: </b><i id="serialdata"></i></p>
		
	<p><b>Battery Voltage: </b><i id="batteryVoltage"></i></p>
	
	<p><b>Battery Percentage: </b><i id="batteryPercent"></i></p>
	
	<p><b>Right Motor Current: </b><i id="rCurrent"></i></p>
	
	<p><b>Left Motor Current: </b><i id="lCurrent"></i></p>
	
	<p><b>Status: </b><i id="status"></i></p>
		
	<hr>
				
	<footer>
	
	<br>
	<p>&copy; Copyright 2018, Queen's University Belfast | Ryan McCartney</p>
	<a href="https://www.qub.ac.uk">
	<img src="media/QUB Logo.jpg" style="max-width:8%;height:auto;">
	</a>
	
	</footer>
	
</body>
</html> 

