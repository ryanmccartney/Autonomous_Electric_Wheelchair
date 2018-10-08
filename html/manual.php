<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8" />
		<title>Autonomous Wheelchair</title>
		<link rel="shortcut icon" href="media/favicon.ico" />	
		<link rel="stylesheet" href="style/style.css">
				
	</head>

<body>
	
	<header>
		<br>
		<h1>Autonomous Electric Wheelchair</h1>
	<div class="header" id="myHeader">
		<h2>Manual Control Interface</h2>
		
		<ul>
			<li><a href="index.php">Home</a></li>
			<li><a href="auto.php">Autonomous</a></li>
			<li><a class="active" href="manual.php">Manual</a></li>
			<li><a href="about.php">About</a></li>
		</ul>
	</div>
	</header>
	
	<div class="content">
	
	<h3>Command Buttons</h3>
	
		<p>
		<form align="center" method="post">

				<input type="submit" value="Stop Wheelchair" name="Stop">
				
				<input type="submit" value="Update Values" name="Update">

		</form>
		<p>
	
	<h3>Control Gamepad</h3>
	
	<p>Take manual control of the electric wheelchair by using the gamepad below.</p>
			
		<div id="joystick">
        
			<script src="scripts/virtualjoystick.js"></script>
			<script>
			console.log("touchscreen is", VirtualJoystick.touchScreenAvailable() ? "available" : "not available");
	
			var joystick	= new VirtualJoystick({
				container	: document.getElementById('joystick'),
				mouseSupport	: true,
				stationaryBase: true,
                      baseX: 200,
                      baseY: 200,
				limitStickTravel: true,
				stickRadius	: 100
				
			});
			
			joystick.addEventListener('touchStart', function(){
				console.log('down')
			})
			
			joystick.addEventListener('onTouchMove', function(){
				// Prevent the browser from doing its default thing (scroll, zoom)
				event.preventDefault()
			})
			
			joystick.addEventListener('touchEnd', function(){
				console.log('up')
			})

			setInterval(function(){
				var outputEl	= document.getElementById('result');
				outputEl.innerHTML	= '<b>Joystick Output:</b> '
					+ ' dx:'+joystick.deltaX()
					+ ' dy:'+joystick.deltaY()	
			}, 1/30 * 1000);
		</script>
				
        </div>
	
	<h3>Debug Data</h3>
	
	<p><b>PHP executing as: </b>
	<?php
		echo exec('whoami');
	?>
	</p>
	
	<p id="result"></p>
		
	<p id="output"></p>
	
	<?php
		
		echo"<p>";		
		error_reporting(E_ALL);
		ini_set('display_errors', '1');
		echo"</p>";
		
		//Load the serial port class 	
		include 'scripts/PhpSerial.php';
		
		// New instance of class
		$serial = new PhpSerial;
				
		// First we must specify the device. This works on both linux and windows (if
		// your linux serial device is /dev/ttyS0 for COM1, etc)
		$serial->deviceSet("/dev/ttyACM0");

		// We can change the baud rate, parity, length, stop bits, flow control
		$serial->confBaudRate(115200);
		$serial->confParity("none");
		$serial->confCharacterLength(8);
		$serial->confStopBits(1);
		$serial->confFlowControl("none");

		// Then we need to open it
		$serial->deviceOpen();
		
		//Delay before writing data
		sleep(0.2);
		
		// To write into
		$data = "0,0,SEND";
		$serial->sendMessage($data);
		
		$read = $serial->readPort();
				
	?>
	
	<?php
	
	$data = "0,0,STOP";
						
		if (isset($_POST['Stop']))
			{
			$data = "0,0,STOP";
			$serial->sendMessage($data);	
			}
		if (isset($_POST['Update']))
			{
			$data = "0,0,SEND";
			$serial->sendMessage($data);	
			}
			
	echo"<p><b>Data sent to serial port: </b>";
	echo $data;
	echo"</p>";
			
	$read = $serial->readPort();
	echo"<p><b>Data received from serial line: </b> ";
	echo $read;
	echo"</p>";
			
	?>
	
	
	<?php
	
	$speed = "0";
	$angle = "0";
	
	//Combine Strings
	$data = $speed . ',' . $angle.',RUN';
	
	//Send Data
	$serial->sendMessage($data);

	echo"<p><b>Realtime Data Sent: </b> ";
	echo $data;
	echo"</p>";
				
					
	?>
	
	<br>
	
	<h3>Emergency Stop</h3>
	
	<script>
		function changeImage() {
		var Off = "media/Emergency Stop Off.png",
			On = "media/Emergency Stop On.png";
		var imgElement = document.getElementById('emergency');
   
		imgElement.src = (imgElement.src === Off)? On : Off;
		}
	</script>
	
	<img alt="" src="media/Emergency Stop Off.png" style="max-width:80%;height:auto;align:center;" id="emergency" onclick="changeImage();"/>
		
	</div>
	<br>
	
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

