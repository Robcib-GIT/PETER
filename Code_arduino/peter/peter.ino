/*
  Control for modular pneumatic robots

  Jorge F. García-Samartín
  www.gsamartin.es
  2024-11-18
*/

#include <Arduino.h>
#include "Config.h"
#include "Valvula.h"
#include "Sensor.h"

// Global Variables
modes State = S_NORMAL; // State of the robot (for managiing emergency stops)
uint8_t real_robot = 1; // 1 if the robot is real, 0 if it is a simulation

// Valve array
Valvula *misValvulas[NUM_VALVULAS];

// Sensor array and definition
Sensor *misSensores[NUM_SENSORES];

//Interrupcion emergencia
void emergency_stop_callback() {
  State = S_ERROR_EMERGENCY_STOP;
  for(uint8_t i = 0; i < NUM_VALVULAS; i++) {
    misValvulas[i] -> alAire();
  }

}

void setup() {
  Serial.begin(115200);

  pinMode(EMRGY_PIN, INPUT_PULLUP);

  // Instanciamos las valvulas
  for (int i = 0; i < NUM_VALVULAS; i++) {
    misValvulas[i] = new Valvula(PIN_32_ARRAY[i], PIN_22_ARRAY[i]);
    misValvulas[i]->init();
  }

  // Sensor initialization  
  misSensores[0] = new SensorBNO055();
  misSensores[1] = new SensorVL53L0X();

  for (uint8_t i = 0; i < NUM_SENSORES; i++) {
    misSensores[i]->begin();
  }

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(2, OUTPUT);
  
  Wire.begin();

  uint16_t t = millis();

  digitalWrite(LED_BUILTIN, LOW);

  // Normal mode
  State = S_NORMAL;

}

void loop() {

  /********************************************************
    Normal State
  ********************************************************/

  if(State == S_NORMAL) {

    uint16_t t1 = millis();

    if (Serial.available() > 0) {
      static char op = ' ';
      op = Serial.read();
      uint8_t num_valv;
      uint16_t x;
      float p;
      int buffer[NUM_VALVULAS + 1];
      
      switch (op) {

        // Real or simulation mode
        case 'i':
          real_robot = Serial.parseInt();
          if (DEBUG) {
            Serial.println("Working mode changed");
          }
          break;

        // Fill valve x milliseconds
        case 'f':
          num_valv = Serial.parseInt();
          x = Serial.parseInt();
          misValvulas[num_valv]->fill_millis((uint16_t)x);
          if (DEBUG) {
            Serial.print(x);
            Serial.println(num_valv);
          }
          break;

        // Empty valve x milliseconds
        case 'e':
          num_valv = Serial.parseInt();
          x = Serial.parseInt();
          misValvulas[num_valv]->emptyng_millis((uint16_t)x);
          break;
        
        case 'c':
        num_valv = Serial.parseInt();
        misValvulas[num_valv]->Cerrada();
        break;

        // Measure value of the sensors
        case 'M':
          if (real_robot) {
            Serial.print("S ");
            for (uint8_t i = 0; i < NUM_SENSORES; i++) {
              misSensores[i]->measure(); 
            }
            
          } else {
            for (uint8_t i = 0; i < NUM_VALVULAS; i++) {
                int p = misValvulas[i]->get_actual_pressure();
                Serial.print(9 + p * P_V_RATIO);
                Serial.println(" ");
            }
          }

          break;
    }
  }


  // Callback de las valvulas   
  for (uint8_t i = 0; i < NUM_VALVULAS; i++) {
    misValvulas[i]->callback();
  }
  
  // Comprobamos si alguna valvula ha entrado en modo de parada de emergencia
  for (uint8_t i = 0; i < NUM_VALVULAS; i++) {
    if(misValvulas[i]-> getEmergency() == true) {
      State = S_ERROR_STOPAUTO;
    }
   }  

  }

  /********************************************************
    Error State
  ********************************************************/
  if(State == S_ERROR_STOPAUTO) {
    // Parpadea el led
    digitalWrite(13, !digitalRead(13));
    delay(100);

    if( Serial.available() > 0) {
      char op = Serial.read();

      // Rearmamos
      if(op == 'R') {
        for (int i = 0; i < NUM_VALVULAS; i++) {
          misValvulas[i] -> rearmar();
          State = S_NORMAL;
        }
      }
    }

  }
}