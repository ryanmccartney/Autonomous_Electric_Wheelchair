//------------------------------------------------------------------------------------------------------------------
// NAME: Electric Wheelchair Motor Control Alogtrithm
// AUTH: Ryan McCartney
// DATE: 14th January 2019
// DESC: Recieves serial communications containing control commands for an electric wheelchair
// NOTE: All Rights Reserved, 2018, Queen's University Belfast
//------------------------------------------------------------------------------------------------------------------

//Pin Definitions
#define RightMotorDirection 24 //DIR Input on Board
#define LeftMotorDirection 22 //DIR Input on Board

#define RightMotorSleep 28 //SLP Input on Board
#define LeftMotorSleep 26  //SLP Input on Board

#define RightMotorFault 32 //FLT Pin on Board
#define LeftMotorFault 30  //FLT Pin on Board

#define RightMotorEnergise 36 //Relay Isolating Supply to Right Motor
#define LeftMotorEnergise 34  //Relay Isolating Supply to Left Motor

#define RightMotorSpeed 3 //PWM Input on Board
#define LeftMotorSpeed 2 //PWM Input on Board

#define RightMotorCurrent 1 //CS Pin on Board
#define LeftMotorCurrent 0  //CS Pin on Board

#define MotorBrakes 40 //Relay to apply mechanical brake
#define WarningLight 38 //Relay to apply mechanical brake
#define Reset 42 //Pin attached to reset for instrinsic program reset
#define BatteryIndication 2 //Voltage Sensor

//Receive Data Variables
float maxCurrent = 30.00;
int maxSpeed = 100;

//Accuracy adustment for current readings
int currentOffset = 0;

//Receive Data Variables
String inputString = "";
String command = ""; //Override commands to STOP, indicate ERRORs, etc.
int setSpeed = 0; // -100 to +100 (Reverse to Forward)
int setAngle = 0; // -100 to +100 (Left to Right)
int serialInputs = 1; //Commands Recieved for Processing
bool stringComplete = false;

//Transmittable Data
float batteryVoltage = 0.00;
float rightMotorCurrent = 0.00;
float leftMotorCurrent = 0.00;
int rightMotorFault = 0;
int leftMotorFault = 0;
String statusMessage = "";

//Motor Driver Output Variables
int leftMotorSpeed = 0; // 0 to 255
int rightMotorSpeed = 0; // 0 to 255
int leftDirection = 1;
int rightDirection = 1;

//------------------------------------------------------------------------------------------------------------------
//Setup runs on Powerup
//------------------------------------------------------------------------------------------------------------------
void setup() {
  //Deal with RESET Pin
  digitalWrite(Reset, HIGH);

  //Change PWM Frequency to 31.25KHz
  TCCR3B = TCCR3B & 0b11111000 | 0x01;
  
  //Initialise Ourput Pins
  pinMode(RightMotorDirection, OUTPUT);
  pinMode(LeftMotorDirection, OUTPUT);
  pinMode(RightMotorSpeed, OUTPUT);
  pinMode(LeftMotorSpeed, OUTPUT);
  pinMode(RightMotorEnergise, OUTPUT);
  pinMode(LeftMotorEnergise, OUTPUT);   
  pinMode(MotorBrakes, OUTPUT);
  pinMode(WarningLight, OUTPUT);
  pinMode(Reset, OUTPUT);

  //Set Initial State
  digitalWrite(RightMotorDirection, 1);
  digitalWrite(LeftMotorDirection, 1);
  digitalWrite(RightMotorEnergise, 1);
  digitalWrite(LeftMotorEnergise, 1);
  digitalWrite(RightMotorSpeed, 0);
  digitalWrite(LeftMotorSpeed, 0);
  digitalWrite(MotorBrakes, 0);
  digitalWrite(WarningLight, 0);
  
  //Setup Input Pins
  pinMode(BatteryIndication, INPUT_PULLUP);
  pinMode(RightMotorCurrent, INPUT_PULLUP);
  pinMode(LeftMotorCurrent, INPUT_PULLUP);
  pinMode(RightMotorFault, INPUT_PULLUP);
  pinMode(LeftMotorFault, INPUT_PULLUP);

  //Serial Communications Setup
  Serial.begin(115200);
  //Reserve Memory Sapce for Incomming Bytes
  inputString.reserve(200);
  statusMessage = "STATUS = System restarting.";

  //Calibrate the current value on startup
  currentOffset = (analogRead(RightMotorCurrent)+analogRead(LeftMotorCurrent))/2;
  
  sendData();
  delay(250);
}

//------------------------------------------------------------------------------------------------------------------
//Maps Speed and Direction for Output to Motor Driver
//------------------------------------------------------------------------------------------------------------------
bool mapOutputs() {

  bool status = false;

  //Check the range of speed data
  if((setSpeed <= 100 && setSpeed >= -100)){

     //Check the range of angle data
    if((setAngle <= 100 && setAngle >= -100)){
    
      if(setSpeed < 0){
        setSpeed = -setSpeed;
        leftDirection = 0;
        rightDirection = 0;
      }
      else{
        leftDirection = 1;
        rightDirection = 1;
      }
 
      //Map Inputs to motor PWM
      leftMotorSpeed = map(setSpeed, 0, 100, 0, 255);
      rightMotorSpeed = map(setSpeed, 0, 100, 0, 255);
      
      if (setAngle < 0) {
        setAngle = -setAngle;
        if(setAngle <= 50){
          rightMotorSpeed = map(setAngle,50,0,0,rightMotorSpeed);
          rightMotorSpeed = (int)rightMotorSpeed;
        }
        else if(setAngle > 50){
          rightMotorSpeed = map(setAngle,50,100,0,rightMotorSpeed);
          rightMotorSpeed = (int)rightMotorSpeed;
          if(rightDirection == 0){
            rightDirection = 1;
          }
          else if(rightDirection == 1){
            rightDirection = 0;
          }
        }
        status = true;
      }
      else if (setAngle > 0){
        if(setAngle <= 50){
          leftMotorSpeed = map(setAngle,50,0,0,leftMotorSpeed);
          leftMotorSpeed = (int)leftMotorSpeed;
        }
        else if(setAngle > 50){
          leftMotorSpeed = map(setAngle,50,100,0,leftMotorSpeed);
          leftMotorSpeed = (int)leftMotorSpeed;
          if(leftDirection == 0){
            leftDirection = 1;
          }
          else if(leftDirection == 1){
            leftDirection = 0;
          }
        }
        status = true;
        }
      else if (setAngle == 0){
         status = true; 
        }
      else{
        status = false;
      }
    }
  }
  
    if(status == true){
      statusMessage = "STATUS = Data Mapped Succesfully";
    }
    else{
      statusMessage = "ERROR = Failed to map sent data to output. Check range of sent data.";
    }
    
    return status;
  }

//------------------------------------------------------------------------------------------------------------------
//When Serial input is made this function parses the contents
//------------------------------------------------------------------------------------------------------------------
bool proccessInput() {

  bool status = false;
  char delimiter = ',';
  char newline = '\r';
  int variableNumber = 1;
  String variable = "";

  // Length (with one extra character for the null terminator)
  int stringLength = inputString.length() + 1;

  if(stringLength > 100){
    stringLength = 100;
    }

  // Prepare the character array (the buffer) 
  char charArray[stringLength];

  // Copy it over 
  inputString.toCharArray(charArray, stringLength);

  //Parse char array derved from input string from serial line
  for(int i = 0; i < stringLength; i++){

   // if the incoming character is a comma then it must indicate the end of a variable
   if (charArray[i] == delimiter) {

      if (variableNumber == 1){
         setSpeed = variable.toInt();
         }
      else if (variableNumber == 2){
         setAngle = variable.toInt();
         }
      else{
        command = "ERROR";   
      }
      variableNumber++;
      variable = "";
    }

  else if(charArray[i] == newline){
    
   if((command == "STOP") && (variable == "RESET")){
      //Assign Command Variable
      command = variable; 
      }
    else if(command != "STOP"){
      //Assign Command Variable
      command = variable; 
    }
    else{
      //Assign Command Variable
      command = "STOP"; 
    }     
    
    //Function performed correctly if here, set status
    if(variableNumber == 3){
      status = true;
      break;
      }
    else{
      status = false;
      command = "ERROR";
      }
    }
  else{
  
  //Input Sterilisation 
  String currentChar = "";
  currentChar =+ charArray[i];
  int inputSterilise = currentChar.toInt();
     
    if(variableNumber == 1 || variableNumber == 2){
      if((inputSterilise == 45) || ((inputSterilise >= 45) && (inputSterilise <= 57))){
          variable += charArray[i];
          }
      else{
          status = false;
          command = "ERROR";
          break;
          }
      }
    else if(variableNumber == 3){
      if((inputSterilise >= 65) && (inputSterilise <= 90)){
          variable += charArray[i];
      }
      else{
          status = false;
          command = "ERROR";
          break;
          }
      }
    }
  }

  //Debug Indicators
  /*Serial.print("Data Sequence = ");
  Serial.println(serialInputs); 
  Serial.print("Raw Input = ");
  Serial.print(inputString);
  
  if(status == true){
      Serial.print("Speed Read from Serial Port = ");
      Serial.println(setSpeed);
      Serial.print("Angle Read from Serial Port = ");
      Serial.println(setAngle);
      }
      
  Serial.print("Command Read from Serial Port = ");
  Serial.println(command);
  Serial.println("");
  */
 
  //Reset Serial
  inputString = "";
  stringComplete = false;
  
  //Increment Commmands Processed
  serialInputs++;

  if(status == true){
      statusMessage = "STATUS = Data succesfully received.";
    }
  else{
      statusMessage = "ERROR = Data not received. Check the format of your data.";
    }
    
  return status;
}

//------------------------------------------------------------------------------------------------------------------
//When Serial input is made this function parses the contents
//------------------------------------------------------------------------------------------------------------------
bool executeCommands() {

  //Function error variable
  bool status = false;

  if(command == "ERROR"){
    stopWheelchair();
    sendData();
    status = true; 
  }
  else if(command == "STOP"){
    statusMessage =  "WARNING = Wheelchair is performing an Emergency Stop.";
    stopWheelchair();
    sendData();
    status = true;
  }
  else if(command == "SEND"){
    sendData();
    status = true;
  }
  else if(command == "RUN"){
    status = true;    
  }
  else if(command == "BRAKEOFF"){

    //Allow wheelchair to be stopped
    setSpeed = 0;
    setAngle = 0;
  
    //Speed to Zero
    analogWrite(RightMotorSpeed, 0);
    analogWrite(LeftMotorSpeed, 0);
 
    //Turn Off Brakes
    digitalWrite(MotorBrakes, 1);
    
    //Enable Wheelchair Coasting
    digitalWrite(RightMotorSleep, 0);
    digitalWrite(LeftMotorSleep, 0);

    //Isolate the motor power supply
    digitalWrite(RightMotorEnergise, 1);
    digitalWrite(LeftMotorEnergise, 1);
       
    statusMessage =  "WARNING = Brakes Not Engaged, beware of vechile movement.";
    sendData();

    status = true;
  }
  else if(command == "RESET"){
    statusMessage =  "WARNING = Controller is resseting. Expect abnormal behaviour.";
    sendData();
    delay(250);
    digitalWrite(Reset, 0);
    status = true;
  }
  else{
     status = false;
     statusMessage = "ERROR = No valid command to execute. Declaring Error.";
     command = "ERROR";
     sendData();
     stopWheelchair();
  }
  return status; 
}

//------------------------------------------------------------------------------------------------------------------
//Stop the Wheelchair
//------------------------------------------------------------------------------------------------------------------
void stopWheelchair() {

   //Set Variables to Appropriate Values to stop chair further moving.
   setSpeed = 0;
   setAngle = 0;
     
   //Speed to Zero
   analogWrite(RightMotorSpeed, 0);
   analogWrite(LeftMotorSpeed, 0);
 
   //Isolate the motor power supply
   digitalWrite(RightMotorEnergise, 1);
   digitalWrite(LeftMotorEnergise, 1);
    
   //Stop Wheelchair Coasting
   digitalWrite(RightMotorSleep, 0);
   digitalWrite(LeftMotorSleep, 0);

   //Apply Brakes
   digitalWrite(MotorBrakes, 0);

   //Turn Off Warning Light
   digitalWrite(WarningLight, 0);
   return;
}

//------------------------------------------------------------------------------------------------------------------
//Reads senor inputs and computes metrics
//------------------------------------------------------------------------------------------------------------------
void readInputs() {

   //Constants for sensor readings conversion
   float voltageFactor = 0.02932551; //Voltage in Volts
   float voltageOffset = 1.65;
   float currentFactor = 0.244379; //Current in Amps
 
   //Read sensor data to update variables 
   batteryVoltage = (analogRead(BatteryIndication)*voltageFactor)-voltageOffset;
   rightMotorCurrent = (analogRead(RightMotorCurrent)-currentOffset)*currentFactor;
   leftMotorCurrent = (analogRead(LeftMotorCurrent)-currentOffset)*currentFactor;
   
   rightMotorFault = digitalRead(RightMotorFault);
   leftMotorFault = digitalRead(LeftMotorFault);

   return;
}

//------------------------------------------------------------------------------------------------------------------
//Send input variables and stauts over serial
//------------------------------------------------------------------------------------------------------------------
void sendData() {

   readInputs();
   
   if(rightMotorFault == 0){
      statusMessage = "ERROR = Right motor has developed a fault.";
      stopWheelchair();
      
   }
   else if(leftMotorFault == 0){
      statusMessage = "ERROR = Left motor has developed a fault.";
      stopWheelchair();
   }

   //Send Serial Information
   Serial.print(leftMotorCurrent,2);
   Serial.print(",");
   Serial.print(rightMotorCurrent,2);
   Serial.print(",");
   Serial.print(batteryVoltage,2);
   Serial.print(",");
   Serial.print(statusMessage);    
   Serial.println("");

   //Ensure Data is Sent
   Serial.flush();

   return; 
}

//------------------------------------------------------------------------------------------------------------------
//Main Programme operating loop
//------------------------------------------------------------------------------------------------------------------
void loop() {

  //Function Variables
  bool status = true;
   
  //When new Serial Data Arrives
  if (stringComplete == true) {

      if (proccessInput() == true){

        if (mapOutputs() == true){
        
          if (executeCommands() == true){

            if (setSpeed != 0){
              //Set the Motor Direction
              digitalWrite(RightMotorDirection, rightDirection);
              digitalWrite(LeftMotorDirection, leftDirection);
  
              //Disable Electrical Brake
              digitalWrite(RightMotorSleep, 1);
              digitalWrite(LeftMotorSleep, 1);
   
              //Connect motor power supply
              digitalWrite(RightMotorEnergise, 0);
              digitalWrite(LeftMotorEnergise, 0);
                 
              //Disable Brakes
              digitalWrite(MotorBrakes, 1);

              //Activate Warning Light
              digitalWrite(WarningLight, 1);

              analogWrite(RightMotorSpeed, rightMotorSpeed);
              analogWrite(LeftMotorSpeed, leftMotorSpeed);
            
              status = true;
            }
            else if(command == "BRAKEOFF"){
              status = true;
              }
            else{
              stopWheelchair();
              status = true;
            }
          }
          else{
            stopWheelchair();
            sendData();
            }
        }
        else{
          stopWheelchair();
          sendData();
          }
      }
      else{
        sendData();
        }
    }

  readInputs();
  //Current Limiting Algorithm
  
  if(rightMotorCurrent > maxCurrent || leftMotorCurrent > maxCurrent){

    float maxMotorCurrent = leftMotorCurrent;
    
    if(rightMotorCurrent > maxMotorCurrent){
      maxMotorCurrent = rightMotorCurrent;
    }

    //maxSpeed = (int)(100/(maxMotorCurrent/maxCurrent));
    
    inputString = setSpeed;
    inputString += ",";
    inputString += setAngle;
    inputString += ",RUN";
    stringComplete = true;
    status = true;

    //Send Warning Message
    statusMessage = "WARNING = Overcurrent Warning. Max Speed now set to " + maxSpeed;
    sendData();
  }
  
  if(status == false){
  
    inputString = "0,0,ERROR";
    statusMessage = "ERROR = Main Loop program error.";
    stopWheelchair();
    sendData();
  }
}

//------------------------------------------------------------------------------------------------------------------
//Rertieve Serial Data
//------------------------------------------------------------------------------------------------------------------
void serialEvent() {

  while (Serial.available()){

    //Gets the next byte
    char inputChar = (char)Serial.read();
    
    //Add latest char to string
    inputString += inputChar;
      
    if (inputChar == '\n') {
      stringComplete = true;
    }
  }
}
