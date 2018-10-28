<?php
	
	//Error Reporting
	//echo"<p>";		
	//error_reporting(E_ALL);
	//ini_set('display_errors', '1');
	//echo"</p>";
		
	//Load the serial port class 	
	include 'PhpSerial.php';
			
	$data = $_GET['serialData']; 
	$serial->sendMessage($data);	
			
	//echo"<p><b>Data sent to serial port: </b>";
	//echo $data;
	//echo"</p>";
	
	$read = $serial->readPort();
	//echo"<p><b>Data received from serial line: </b> ";
	echo $read;
	//echo"</p>";

