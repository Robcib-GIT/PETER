/*
  Class for controlling the sensors

  Jorge F. García-Samartín
  www.gsamartin.es
  2024-12-17
*/

#include "Sensor.h"

/********************************************************
    Sensor class
********************************************************/

// Constructor for Sensor class
Sensor::Sensor() {
    // Initialization code here
}

/********************************************************
    Sensor BNO055 class
********************************************************/
// Constructor for SensorBNO055 class
SensorBNO055::SensorBNO055() : Sensor() {
    // Initialization code specific to BNO055
}

// Method to initialize the BNO055 sensor
void SensorBNO055::begin() {
    // Code to initialize the BNO055 sensor
    if(!bno.begin()) {
        /* There was a problem detecting the BNO055 ... check your connections */
        //Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
        //while(1);
    }
    bno.setExtCrystalUse(true);
}

// Method to read data from the BNO055 sensor
void SensorBNO055::measure() {
    sensors_event_t orientationData;
    bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
    Serial.print(orientationData.orientation.x);
    Serial.print(",");
    Serial.print(orientationData.orientation.y);
    Serial.print(",");
    Serial.print(orientationData.orientation.z);
}

/********************************************************
    Sensor INU3221 class
********************************************************/
// Constructor for SensorINA3221 class
SensorINA3221::SensorINA3221(uint8_t channel) {
    // Initialization code specific to INA3221
    this->channel = channel;
}

// Method to initialize the INA3221 sensor
void SensorINA3221::begin() {
    // Code to initialize the INA3221 sensor
}

// Method to read data from the INA3221 sensor
void SensorINA3221::measure() {
    float busVoltage = ina3221.getBusVoltage(this->channel); // Example: reading voltage from channel 1
    Serial.print(busVoltage);
}
