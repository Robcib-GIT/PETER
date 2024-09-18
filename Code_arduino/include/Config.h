//En este fichero se declararan todas las constantes del programa, definiciones de tipos
// etc.

#ifndef _CONFIG_H_
#define _CONFIG_H_



#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include "Pinout.h"
#include "Config.h"
#include "SerialCommunication.h"


#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define SCREEN_ADDRESS 0x3C // OLED I2C address
#define OLED_RESET -1 // Reset pin # (or -1 if sharing Arduino reset pin)

enum modos
{
    S_NORMAL,
    S_ERROR_STOPAUTO,
    S_ERROR_PARADA_EMERGENCIA
};

const uint8_t LED_MAXV_R = 180;
const uint8_t LED_MAXV_G = 255;
const uint8_t LED_MAXV_B = 180;


#endif // _CONFIG_H_