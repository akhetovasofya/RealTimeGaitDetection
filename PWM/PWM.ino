#include <Servo.h>

#include <Arduino.h>
#include <LSM6DS3.h>
#include "LSM6DS3.h"
#include "Wire.h"
 
//Create an instance of class LSM6DS3
LSM6DS3 myIMU(I2C_MODE, 0x6A);    //I2C device address 0x6A

const int imuPin = 10;  // Pin for the PWM output
 
void setup() {
    // put your setup code here, to run once:
    Serial.begin(9600);
    while (!Serial);
    //Call .begin() to configure the IMUs
    if (myIMU.begin() != 0) {
        Serial.println("Device error");
    } else {
        Serial.println("Device OK!");
    }

    pinMode(imuPin, OUTPUT);  // Set the pin for PWM output
}
 
void loop() {
  //Time
    //Serial.print("Time: ");
    unsigned long myTime = millis();
    //Serial.println(myTime); // prints time since program started
  
    //Accelerometer
    float accelx = myIMU.readFloatAccelX();  // Read IMU value from A0
    //Serial.print(" accel x = ");
    //Serial.println(imuValue);
    float accely = myIMU.readFloatAccelY();  // Read IMU value from A0
    //Serial.print(" accel y = ");
    //Serial.println(imuValue);
    float accelz = myIMU.readFloatAccelZ();  // Read IMU value from A0
    //Serial.print(" accel z = ");
    //Serial.println(imuValue);

//GYRO
    float gyrox = myIMU.readFloatGyroX();  // Read IMU value from A0
    //Serial.print(" gyro x = ");
    //Serial.println(imuValue);

    float gyroy = myIMU.readFloatGyroY();  // Read IMU value from A0
    //Serial.print(" gyro y = ");
    //Serial.println(imuValue);

    float gyroz = myIMU.readFloatGyroZ();  // Read IMU value from A0
    //Serial.print(" gyro z = ");
    //Serial.println(imuValue);
    
//FSR
    //int pwmValue = map(imuValue, 0, 1023, 0, 255);  // Map IMU value to PWM value
    int read_val0 = analogRead(A2);  // Generate PWM signal
    //Serial.print(" read 0 = ");
    //Serial.println(read_val);

    //analogWrite(imuPin, 255);

    int read_val1 = analogRead(A3);  // Generate PWM signal
    //Serial.print(" read 1 = ");
    //Serial.println(read_val);

    //Serial.println(accelx +", "+ accely +", "+accelz+", "+ gyrox +", "+gyroy +", "+gyroz +", "+read_val0 +", "+read_val1 +"\r");
    Serial.print(myTime);
    Serial.print(" ");
    Serial.print(accelx);
    Serial.print(" ");
    Serial.print(accely);
    Serial.print(" ");
    Serial.print(accelz);
    Serial.print(" ");
    Serial.print(gyrox);
    Serial.print(" ");
    Serial.print(gyroy);
    Serial.print(" ");
    Serial.print(gyroz);
    Serial.print(" ");
    Serial.print(read_val0);
    Serial.print(" ");
    Serial.print(read_val1);
    Serial.println();
    
    //delay(500);  // Delay for stability


}
