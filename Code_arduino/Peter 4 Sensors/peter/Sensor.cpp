#include "Sensor.h"

Sensor::Sensor() {}

// ==================== BNO055 (0x28) ====================
SensorBNO055::SensorBNO055() : Sensor() {}

void SensorBNO055::begin() {
    if (!bno.begin(0x28)) {
        Serial.println("Error BNO055 (0x28)");
    } else {
        bno.setExtCrystalUse(true);
    }
}

void SensorBNO055::measure() {
    sensors_event_t orientationData;
    bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
    Serial.print(orientationData.orientation.x); Serial.print(",");
    Serial.print(orientationData.orientation.y); Serial.print(",");
    Serial.print(orientationData.orientation.z); Serial.print(",");
    delay(5);
}

// ==================== VL53L0X_1 (0x30) ====================
SensorVL53L0X::SensorVL53L0X() : Sensor() {}

void SensorVL53L0X::begin() {
    // Intentamos iniciar en la dirección base 0x29 y cambiar a 0x30
    if (!lox.begin(0x30, false)) { 
        Serial.println("Error iniciando VL53L0X (0x30)");
    } else {
        Serial.println("VL53L0X (0x30) OK!");
    }
}

void SensorVL53L0X::measure() {
    VL53L0X_RangingMeasurementData_t measure;
    lox.rangingTest(&measure, false);
    if (measure.RangeStatus != 4) {
        Serial.print(measure.RangeMilliMeter);
    } else {
        Serial.print("8191");
    }
    Serial.print(",");
    delay(5);
}

// ==================== BNO055_alt (0x29) ====================
SensorBNO055_alt::SensorBNO055_alt() : Sensor() {}

void SensorBNO055_alt::begin() {
    if (!bno.begin(0x29)) {
        Serial.println("Error BNO055 Alt (0x29)");
    } else {
        bno.setExtCrystalUse(true);
    }
}

void SensorBNO055_alt::measure() {
    sensors_event_t orientationData;
    bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
    Serial.print(orientationData.orientation.x); Serial.print(",");
    Serial.print(orientationData.orientation.y); Serial.print(",");
    Serial.print(orientationData.orientation.z); Serial.print(",");
    delay(5);
}

// ==================== VL53L0X_2 (0x31) ====================
SensorVL53L0X_alt::SensorVL53L0X_alt() : Sensor() {}

void SensorVL53L0X_alt::begin() {
    if (!lox.begin(0x31, false)) {
        Serial.println("Error iniciando VL53L0X_alt (0x31)");
    } else {
        Serial.println("VL53L0X_alt (0x31) OK!");
    }
}

void SensorVL53L0X_alt::measure() {
    VL53L0X_RangingMeasurementData_t measure;
    lox.rangingTest(&measure, false);
    if (measure.RangeStatus != 4) {
        Serial.print(measure.RangeMilliMeter);
    } else {
        Serial.print("8191");
    }
    Serial.print(",");
    delay(5);
}