/*
  Class for controlling the sensors

  Jorge F. García-Samartín
  www.gsamartin.es
  2024-12-17
*/

#ifndef SENSOR_H
#define SENSOR_H

#include <Adafruit_BNO055.h>
#include <Adafruit_INA3221.h>
#include <Adafruit_VL53L0X.h>
#include <Wire.h>

// Class Sensor should work both with Adafruit BNO055 and with a INA3221. Function measure should return the value of the sensor
class Sensor {
public:
    Sensor();
    virtual void begin();
    virtual void measure();
};

// Class SensorBNO055 should inherit from Sensor and should implement the measure function
class SensorBNO055 : public Sensor {
public:
    SensorBNO055();
    void begin();
    void measure();
private:
    Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28, &Wire);
};

// Class SensorINA3221 should inherit from Sensor and should implement the measure function
class SensorINA3221 : public Sensor {
public:
    SensorINA3221(uint8_t channel);
    void begin();
    void measure();
private:
    Adafruit_INA3221 ina3221 = Adafruit_INA3221();
    uint8_t channel;
};

// Class SensorVL53L0X should inherit from Sensor and should implement the measure function
class SensorVL53L0X : public Sensor {
public:
    SensorVL53L0X();
    void begin();
    void measure();
private:
    Adafruit_VL53L0X lox = Adafruit_VL53L0X();
};

#endif

