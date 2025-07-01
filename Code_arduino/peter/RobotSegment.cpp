#include "RobotSegment.h"

using namespace Robot;

stretchSensor::stretchSensor() {
  channel = INA3221_CH1;
  pin = 0;
  max_value = 0;
  min_value = 0;
  prev_time = 0;
  curr_value = 0;
  first_time_calibration = true;
  calibration_time = 5000;
}

stretchSensor::stretchSensor(uint8_t channelNum)
{
    switch (channelNum) {
      case 0: channel = INA3221_CH1; break;
      case 1: channel = INA3221_CH2; break;
      case 2: channel = INA3221_CH3; break;
    }
    pin = channelNum;
    calibration_time = 5000;
}


void stretchSensor::init()
{
    pinMode(pin, INPUT);
    max_value = 2000;
    min_value = 2000;
}

uint16_t stretchSensor::readRaw()
{
    return analogRead(pin);
}

void stretchSensor::calibrate()
{
    if(first_time_calibration)
    {
        max_value = analogRead(pin);
        min_value = analogRead(pin);
        first_time_calibration = false;
    }

    curr_value = analogRead(pin);

    if(curr_value > max_value)
    {
        max_value = curr_value;
    }

    if(curr_value < min_value)
    {
        min_value = curr_value;
    }
}

void stretchSensor::calibrateBloqueante()
{
    prev_time = millis();
    while(millis() - prev_time < calibration_time)
    {
        calibrate();
    }
}

uint16_t stretchSensor::readCalibratedValue()
{
    return map(readRaw(), min_value, max_value, 0, 1000);
}


/*********************************************************
  CLASE INA
*********************************************************/
myINA::myINA()
{
    INA3221 ina_temp(INA3221_ADDR40_GND);
    this -> ina = &ina_temp;
    this -> num_channels = 1;
    this -> sensor[0] = stretchSensor(0);
}

myINA::myINA(ina3221_addr_t address, uint8_t num_channels)
{
    INA3221 ina_temp(address);
    this -> ina = &ina_temp;
    this -> num_channels = num_channels;

    for (uint8_t i = 0; i < num_channels; i++) {
      this -> sensor[i] = stretchSensor(i);
    }

}

void myINA::measure() {
    for (uint8_t i = 0; i < num_channels; i++) {
      this -> measures[i] = this -> ina -> getVoltage(this->sensor[i].getChannel());
      Serial.print(this -> measures[i]);
      Serial.print(" ");
    }
}

