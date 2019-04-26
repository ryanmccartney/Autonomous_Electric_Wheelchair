//------------------------------------------------------------------------------------------------------------------
// NAME: Encoder Testing
// AUTH: Ryan McCartney
// DATE: 25th April 2019
// DESC: Left, Right Motor Encoders for distance measurement and angle
// NOTE: All Rights Reserved, 2018, Queen's University Belfast
//------------------------------------------------------------------------------------------------------------------

#define PI 3.1415926535897932384626433832795

//Receive Data Variables
String inputString = "";
bool stringComplete = false;

//Encoder Info
#define rightEncoderA 2
#define rightEncoderB 3
#define leftEncoderA 18
#define leftEncoderB 19

float xPos = 0.0;
float yPos = 0.0;
float bearing = 0.0;
float xPosDelta = 0.0;
float yPosDelta = 0.0;
float bearingDelta = 0.0;

//ISRs
void rightEncoderAPulse(){
  xPos = xPos + xPosDelta; 
  yPos = yPos + yPosDelta; 
  bearing = bearing + bearingDelta;
}

void rightEncoderBPulse(){
  xPos = xPos - xPosDelta; 
  yPos = yPos - yPosDelta; 
  bearing = bearing - bearingDelta;
}

void leftEncoderAPulse(){
  xPos = xPos + xPosDelta; 
  yPos = yPos + yPosDelta; 
  bearing = bearing + bearingDelta;
}

void leftEncoderBPulse(){
  xPos = xPos - xPosDelta; 
  yPos = yPos - yPosDelta; 
  bearing = bearing - bearingDelta;
}


//Turn Bearing from Reference in Radians
float calcBearing(float leftDistance, float rightDsitance){
  float wheelbase = 0.4;
  float angleRotation = atan((leftDistance-rightDsitance)/wheelbase);
  bearing = bearing + angleRotation;
  }

//Calculate Distance
float distanceTravelled(int pulses){
  float gearRatio = 27.0;
  float pulsesPerRev = 600.0;
  float wheelDiameter = 0.2;
  float wheelMovement = pulses*((PI*wheelDiameter)/(gearRatio*pulsesPerRev));
  return wheelMovement;
  }

//Determine X,Y, Position
float calcPos(float leftDistance, float rightDsitance){
  
  float travelDistance = (leftDistance+rightDsitance)/2;
  xPosDelta = travelDistance*sin(bearing);
  yPosDelta = travelDistance*cos(bearing);
  xPos = xPos + xPosDelta;
  yPos = yPos + yPosDelta;
  }

void storePos(){
  EEPROM.update(0, xPos);
  EEPROM.update(1, yPos);
  EEPROM.update(2, bearing);
}
void caclConstants(){
  
  float wheelbase = 0.4;
  float gearRatio = 27.0;
  float pulsesPerRev = 600.0;
  float wheelDiameter = 0.2;
   
  float distanceDelta = 1*((PI*wheelDiameter)/(gearRatio*pulsesPerRev));
  bearingDelta = atan(distanceDelta/wheelbase);    
  xPosDelta = (distanceDelta/2)*sin(bearingDelta);
  yPosDelta = (distanceDelta/2)*cos(bearingDelta);
  
}

void setup() {

  //Determine Constants for Tracking 
  caclConstants();

  //Load from Memory
  xPos = EEPROM.read(0);
  yPos = EEPROM.read(1);
  bearing = EEPROM.read(2);
  
  //Attach Interupts
  attachInterrupt(digitalPinToInterrupt(rightEncoderA), rightEncoderAPulse, RISING);
  attachInterrupt(digitalPinToInterrupt(rightEncoderB), rightEncoderBPulse, RISING);
  attachInterrupt(digitalPinToInterrupt(leftEncoderA), leftEncoderAPulse, RISING);
  attachInterrupt(digitalPinToInterrupt(leftEncoderB), leftEncoderBPulse, RISING);

  //Serial Communications Setup
  Serial.begin(115200);

  //Print Indicators
  Serial.println("Encoder Testing");
}

void loop() {

  //Convert Bearing to Degrees
  float bearingDegrees = (bearing/(2*PI))*360;
  
  Serial.print("Current Bearing from base is ");
  Serial.print(bearingDegrees,2);
  Serial.print(" degrees. Grid position is (");
  Serial.print(xPos,2);
  Serial.print(",");
  Serial.print(yPos,2);
  Serial.println(") in the X,Y grid.");

  storePos();
  delayMicroseconds(1E9);

  if(stringComplete == true){
    if(inputString == "SETHOME"){
      xPos = 0;
      yPos = 0;
      bearing = 0;
    }
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
