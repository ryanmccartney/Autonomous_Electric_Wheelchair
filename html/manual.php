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
			
			<h2>Manual Navigation</h2>
		
			<ul>
				<li><a href="index.php">Home</a></li>
				<li><a href="stream.php">Stream</a></li>
				<li><a href="auto.php">Auto Navigation</a></li>
				<li><a class="active" href="manual.php">Manual Navigation</a></li>
				<li><a href="about.php">About</a></li>
				<li><a href="stats.php">Logging</a></li>
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

	<h3>Control Gamepad</h3>
	
	<p>Take manual control of the electric wheelchair by using the gamepad below.</p>

	<div class="stream" id="joystick">
	
	<img src="http://xavier.local:8080/?action=stream" alt="media/nostream.jpg">

		<script src="scripts/jquery.min.js"></script>
			<script src="scripts/virtualjoystick.js"></script>
			
			<script>
			console.log("touchscreen is", VirtualJoystick.touchScreenAvailable() ? "available" : "not available");
			
			var serialDataPrevious = '0,0,SEND';
			var receivedData = '0,0,0,STATUS';
									
			var joystick	= new VirtualJoystick({
				container	: document.getElementById('joystick'),
				mouseSupport	: true,
				//stationaryBase: true,
                //    baseX: 300,
                //    baseY: 300,
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
				outputEl.innerHTML	= ' dx:'
					+ joystick.deltaX()
					+ ' dy:'
					+ joystick.deltaY()
				
				var setSpeed = Math.round( joystick.deltaY() );
				var setAngle = Math.round( joystick.deltaX() );
									
				var serialData = setSpeed
					+ ','
					+ setAngle;		
												
				if(serialData != serialDataPrevious){
					
					serialDataPrevious = serialData;
					serialData += ',SEND';
					
					//Output Serial data to webpage
					outputSerial = document.getElementById('serialdata');
					outputSerial.innerHTML	= serialData;
					document.manualEntry.serialData.value = serialData;
				
					var sendData = "scripts/serialSend.php?serialData="+ serialData;
				
					$.ajax({
						type: "GET",
						url: sendData,
						datatype: "text",
						success: function(result) {
							
							//If there was data read...
							if(result != ""){
							
							//Parse Data
							var dataRead = result.split("\r\n");
							receivedData = dataRead[0].split(",");
							
							//Print Data to console
							console.log(receivedData);
							
							var batteryVoltage = receivedData[2];
							var batteryPercent = ((batteryVoltage - 23.6)/2)*100;
							batteryPercent = Math.round(batteryPercent * 100) / 100
							var rCurrent = receivedData[1];
							var lCurrent = receivedData[0];
							var status = receivedData[3];
							
							outputBatteryVoltage = document.getElementById('batteryVoltage');
							outputBatteryPercent = document.getElementById('batteryPercent');
							outputRCurrent = document.getElementById('rCurrent');
							outputLCurrent = document.getElementById('lCurrent');
							outputStatus = document.getElementById('status');
							
							outputBatteryVoltage.innerHTML = batteryVoltage+'V';
							outputBatteryPercent.innerHTML = batteryPercent+'%';
							outputRCurrent.innerHTML = rCurrent+'A';
							outputLCurrent.innerHTML = lCurrent+'A';
							outputStatus.innerHTML = status;
							
							}
						}
					});
				}	
			}, 1/5 * 1000);
		</script>
	
	</div>

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

	<h3>Manual Data Input</h3>
	
	<form  method="get" name="manualEntry" action="scripts/serialSend.php">
    <input type="text" name="serialData" value="0,0,STOP" >
	<br>
    <input type="submit" value="Submit" >
	</form>

	<hr>
			
	<h3>Emergency Stop</h3>
	
	<script>
		var off = "media/Emergency Stop Off.png";
		var	on = "media/Emergency Stop On.png";
		var serialData = "0,0,STOP"
		var sendData = "scripts/serialSend.php?serialData="+ serialData;

		function changeImage() {
		{
			alert(window.document.emergency.src);

			if(document.emergency.src==off){
				document.emergency.src=on;
		
				$.ajax({
					type: "GET",
					url: sendData,
					datatype: "text"
				})

			}

			else if(document.emergency.src==on){
				document.emergency.src=off;
			}
		}
	</script>
	
	<img src="media/Emergency Stop Off.png" style="max-width:80%;height:auto;align:center;" alt="" id="emergency" onclick="changeImage();"/>
		
	<br>
	
	<footer>
	
	<br>
	<p>&copy; Copyright 2018, Queen's University Belfast | Ryan McCartney</p>
	<a href="https://www.qub.ac.uk">
	<img src="media/QUB Logo.jpg" style="max-width:8%;height:auto;">
	</a>
	
	</footer>
	
</body>
</html> 

