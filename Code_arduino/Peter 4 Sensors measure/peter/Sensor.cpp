#include "Sensor.h"

Sensor::Sensor() {}

// SensorBNO055 class
SensorBNO055::SensorBNO055() : Sensor() {}

void SensorBNO055::begin() {
    if (!bno.begin()) {
        // IMU1 (BNO055 0x28) not detected!
    }
    bno.setExtCrystalUse(true);
}

void SensorBNO055::measure() {
    sensors_event_t orientationData;
    bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
    Serial.print(orientationData.orientation.x);
    Serial.print(",");
    Serial.print(orientationData.orientation.y);
    Serial.print(",");
    Serial.print(orientationData.orientation.z);
    Serial.print(",");
    //delay(5); // Added delay IMPORTANT
}

SensorVL53L0X::SensorVL53L0X() : Sensor() {}

void SensorVL53L0X::begin() {
    if (!lox.begin()) {
        
    }
    lox.setAddress(0x30);
}

void SensorVL53L0X::measure() {
    VL53L0X_RangingMeasurementData_t measure;
    lox.rangingTest(&measure, false);
    if (measure.RangeStatus != 4) {
        Serial.print(measure.RangeMilliMeter);
    } else {
        Serial.print("-1");
    }
    Serial.print(",");
}

SensorBNO055_alt::SensorBNO055_alt() : Sensor() {}

void SensorBNO055_alt::begin() {
    if (!bno.begin()) {
        
    }
    bno.setExtCrystalUse(true);
}

void SensorBNO055_alt::measure() {
    sensors_event_t orientationData;
    bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
    Serial.print(orientationData.orientation.x);
    Serial.print(",");
    Serial.print(orientationData.orientation.y);
    Serial.print(",");
    Serial.print(orientationData.orientation.z);
    Serial.print(",");
}

SensorVL53L0X_alt::SensorVL53L0X_alt() : Sensor() {}

void SensorVL53L0X_alt::begin() {
    if (!lox.begin()) {
        
    }
    lox.setAddress(0x31);
}

void SensorVL53L0X_alt::measure() {
    VL53L0X_RangingMeasurementData_t measure;
    lox.rangingTest(&measure, false);
    if (measure.RangeStatus != 4) {
        Serial.print(measure.RangeMilliMeter);
    } else {
        Serial.print("-1");
    }
    Serial.print(",");
}
