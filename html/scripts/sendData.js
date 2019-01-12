function sendData(data){

    var url = "scripts/serialSend.php?serialData=";
	var payload = "scripts/serialSend.php?serialData="+ data;
	var receivedData = "TEST"
				
	$.ajax({
		type: "GET",
		url: payload,
		datatype: "text",
		success: function(result) {
			
			var dataRead = result.split("\r\n");
			receivedData = dataRead[0].split(",");
			
			//Print Data to console
			console.log(receivedData);

			//Print Status			
			outputStatus = document.getElementById('status');
			outputStatus.innerHTML = receivedData[3];

			//Print Voltage Percent
			var batteryPercent = ((receivedData[2] - 23.6)/2)*100;
			batteryPercent = Math.round(batteryPercent * 100) / 100;

			outputBatteryPercent = document.getElementById('batteryPercent');
			outputBatteryPercent.innerHTML = batteryPercent+'%';
			
			//Print Voltage
			outputBatteryVoltage = document.getElementById('batteryVoltage');
			outputBatteryVoltage.innerHTML = receivedData[2]+'V';

			//Print Currents
			var rCurrent = receivedData[1];
			var lCurrent = receivedData[0];

			outputRCurrent = document.getElementById('rCurrent');
			outputLCurrent = document.getElementById('lCurrent');	
			outputRCurrent.innerHTML = rCurrent+'A';
			outputLCurrent.innerHTML = lCurrent+'A';
    	}
	});
	return receivedData;
}