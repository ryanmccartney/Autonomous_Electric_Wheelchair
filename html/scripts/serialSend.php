<?php
	
	//Error Reporting
	//echo"<p>";		
	//error_reporting(E_ALL);
	//ini_set('display_errors', '1');
	//echo"</p>";
		
	//Load the serial port class 	
	include 'PhpSerial.php';
	
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

	$data = $_GET['serialData'];

	//Write Data being Transmitted to a Log File
	$dateTime = date("Y/m/d H:i:s");
	$dataLog = $dateTime.",".$data."\n";
	$transmissionLog = fopen('transmittedData.txt', 'a');
	fwrite($transmissionLog, $dataLog);

	$serial->sendMessage($data);
			
	//echo"<p><b>Data sent to serial port: </b>";
	//echo $data;
	//echo"</p>";
	
	$read = $serial->readPort();
	
	if($read != ""){

		//echo"<p><b>Data received from serial line: </b> ";
		echo $read;

		//Write Data to Log File
		$data = $dateTime.",".$read;
		$receiveLog = fopen('receivedData.txt', 'a');
		fwrite($receiveLog, $data);
		
		//echo"</p>";
	}
	?>

