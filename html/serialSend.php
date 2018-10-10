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
	