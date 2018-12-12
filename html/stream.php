<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, hieght=device-hieght user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">
		<title>Autonomous Wheelchair</title>
		<link rel="shortcut icon" href="media/favicon.ico" />	
		
	</head>

	<body>	
	
	<div class="grid-container">
  		<div class="grid-item">Microsoft Kinect RGB Image<p>
			
		  <img src="http://xavier.local:8080/?action=stream" width="30%" alt="Image not found" onerror="this.onerror=null;this.src='media/nostream.jpg';" />
		  </p></div>

  		<div class="grid-item">Microsoft Kinect Depth Image<p>
			
		  <img src="http://xavier.local:8081/?action=stream" width="30%" alt="Image not found" onerror="this.onerror=null;this.src='media/nostream.jpg';" />
		  </p></div>

  		<div class="grid-item">Webcam Floor Image <p>
			  
		   <img src="http://xavier.local:8082/?action=stream" width="30%" alt="Image not found" onerror="this.onerror=null;this.src='media/nostream.jpg';" />
		   </p></div>

	</div>
	</body>

</html> 

