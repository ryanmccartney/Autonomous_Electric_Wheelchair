//------------------------------------------------------------------------------------------------------------------
// NAME: Encoder Testing
// AUTH: Ryan McCartney
// DATE: 25th April 2019
// DESC: Left, Right Motor Encoders for distance measurement and angle
// NOTE: All Rights Reserved, 2018, Queen's University Belfast
//------------------------------------------------------------------------------------------------------------------

#define PI 3.1415926535897932384626433832795

//Encoder Info
#define rightEncoderA 2
#define rightEncoderB 3
#define leftEncoderA 18
#define leftEncoderB 19
int rightPulses = 0;
int leftPulses = 0;

//ISRs
void rightEncoderAPulse(){
  rightPulses = rightPulses + 1; 
}

void rightEncoderBPulse(){
  rightPulses = rightPulses - 1; 
}

void leftEncoderAPulse(){
  leftPulses = leftPulses + 1; 
}

void leftEncoderBPulse(){
  leftPulses = leftPulses - 1; 
}


//Turn Angle
float angle(float leftDistance, float rightDsitance){

  float wheelbase = 0.4;
  float angleRotation = atan((leftDistance-rightDistance)/wheelbase);

  //Convert to Degrees
  angleRotation = (angleRotation/(2*PI))*360;
  
  return angleRotation;
  }

//Calculate Distance
float distanceTravelled(int pulses){

  float gearRatio = 27.0;
  float pulsesPerRev = 600.0;
  float wheelDiameter = 0.2;
  float wheelMovement = pulses*((PI*wheelDiameter)/(gearRatio*pulsesPerRev));
 
  return wheelMovement;
  }

void setup() {
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

  float rightWheelTravel = distanceTravelled(rightPulses);
  float leftWheelTravel = distanceTravelled(leftPulses);

  float currentAngle = angle(leftWheelTravel,rightWheelTravel);

  //Print Indicators
  Serial.print("Right wheel has travelled ");
  Serial.print(rightWheelTravel,2);
  Serial.print("m and the left ");
  Serial.print(leftWheelTravel,2);
  Serial.println("m.");

  delayMicroseconds(1E9);
}
