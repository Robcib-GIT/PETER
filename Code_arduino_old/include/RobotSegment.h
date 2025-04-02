#ifndef ROBOTSEGMENT_H
#define ROBOTSEGMENT_H

#include <Arduino.h>
#include <Wire.h>
#include <INA3221.h>
#include "Valvula.h"

namespace Robot { 

    const uint8_t __NUM_VALVULAS__ = 9;

    struct v_pinout {
      uint8_t pin_32;
      uint8_t pin_22;
    };

    

    class stretchSensor {
        private:
          ina3221_ch_t channel;

          uint8_t pin;

          uint16_t max_value, min_value;
          int prev_time;
          uint16_t  curr_value;
          bool first_time_calibration = true;
          
            uint32_t calibration_time = 5000;

        public:
          // Constructores
          stretchSensor();
          stretchSensor(uint8_t channel);

          // Para inicializar el sensor
          void init();

          // Se devuelve el valor leido (entre 0 y 4096)
          uint16_t readRaw();

          // Se devuelve el valor leido y procesado (entre 0 y 1000)
          uint16_t readCalibratedValue();

          // Se calibra la medicion maxima y minima durante un periodo de tiempo
          void calibrate();

          // Se calibra la medicion maxima y minima durante un periodo de tiempo
          void calibrateBloqueante();

          uint16_t getMaxCalibratedValue() {
            return max_value;
          };

          uint16_t getMinCalibratedValue() {
            return min_value;
          };

          ina3221_ch_t getChannel() {
            return channel;
          };
    };

    class myINA {
      private:
          INA3221 *ina;
          uint8_t num_channels;
          Robot::stretchSensor sensor[3];
          double measures[3];

      public:
          // Constructores
          myINA();
          myINA(ina3221_addr_t address, uint8_t num_channels);

          // Inicialización
          void current_measure_init() {
            this -> ina -> begin(&Wire);
            this -> ina -> reset();
            this -> ina -> setShuntRes(100, 100, 100);
          }

          // Asignar sensores
          void setSensor(stretchSensor sensor, int num) {
            this -> sensor[num] = sensor;
          }

          // Nümero de canalaes
          uint8_t getNumChannels () {
            return num_channels;
          }

          // Medir
          void measure();
    };



};





#endif 