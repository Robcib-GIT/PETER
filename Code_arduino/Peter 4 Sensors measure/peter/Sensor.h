// Sensor.h
#ifndef SENSOR_H
#define SENSOR_H

#include <Adafruit_BNO055.h>
#include <Adafruit_VL53L0X.h>
#include <Wire.h>

class Sensor {
public:
    Sensor();
    virtual void begin();
    virtual void measure();
};

class SensorBNO055 : public Sensor {
public:
    SensorBNO055();
    void begin();
    void measure();
private:
    Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28, &Wire);
};

class SensorVL53L0X : public Sensor {
public:
    SensorVL53L0X();
    void begin();
    void measure();
private:
    Adafruit_VL53L0X lox = Adafruit_VL53L0X();
};

class SensorBNO055_alt : public Sensor {
public:
    SensorBNO055_alt();
    void begin();
    void measure();
private:
    Adafruit_BNO055 bno = Adafruit_BNO055(56, 0x29, &Wire);
};

class SensorVL53L0X_alt : public Sensor {
public:
    SensorVL53L0X_alt();
    void begin();
    void measure();
private:
    Adafruit_VL53L0X lox = Adafruit_VL53L0X();
};

#endif
