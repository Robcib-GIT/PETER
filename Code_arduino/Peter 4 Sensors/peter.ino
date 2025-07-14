#include <Arduino.h>
#include "Config.h"
#include "Valvula.h"
#include "Sensor.h"

#define XSHUT_PIN_1 7
#define XSHUT_PIN_2 6

modes State = S_NORMAL;
uint8_t real_robot = 1;
Valvula *misValvulas[NUM_VALVULAS];
Sensor *misSensores[NUM_SENSORES];

void emergency_stop_callback() {
  State = S_ERROR_EMERGENCY_STOP;
  for (uint8_t i = 0; i < NUM_VALVULAS; i++) {
    misValvulas[i]->alAire();
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(EMRGY_PIN, INPUT_PULLUP);
  pinMode(XSHUT_PIN_1, OUTPUT);
  pinMode(XSHUT_PIN_2, OUTPUT);
  digitalWrite(XSHUT_PIN_1, LOW);
  digitalWrite(XSHUT_PIN_2, LOW);
  delay(10);

  for (int i = 0; i < NUM_VALVULAS; i++) {
    misValvulas[i] = new Valvula(PIN_32_ARRAY[i], PIN_22_ARRAY[i]);
    misValvulas[i]->init();
  }

  misSensores[0] = new SensorBNO055();
  delay(500);
  misSensores[1] = new SensorVL53L0X();
  misSensores[2] = new SensorBNO055_alt();
  delay(500);
  misSensores[3] = new SensorVL53L0X_alt();

  digitalWrite(XSHUT_PIN_1, HIGH);
  delay(10);
  ((SensorVL53L0X*)misSensores[1])->begin();

  digitalWrite(XSHUT_PIN_2, HIGH);
  delay(10);
  ((SensorVL53L0X_alt*)misSensores[3])->begin();

  misSensores[0]->begin();
  misSensores[2]->begin();

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(2, OUTPUT);

  Wire.begin();
  digitalWrite(LED_BUILTIN, LOW);
  State = S_NORMAL;
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');  // Read full line until newline
    input.trim(); // Remove whitespace or carriage return if any

    if (input.length() > 0) {
      char op = input.charAt(0);
      uint8_t num_valv;
      uint16_t x;

      switch (op) {
        case 'i':
          real_robot = input.substring(1).toInt();
          Serial.println("Working mode changed");
          break;

        case 'f':
          sscanf(input.c_str() + 1, "%hhu %hu", &num_valv, &x);
          misValvulas[num_valv]->fill_millis(x);
          Serial.print("Filling valve ");
          Serial.print(num_valv);
          Serial.print(" for ");
          Serial.print(x);
          Serial.println(" ms");
          break;

        case 'e':
          sscanf(input.c_str() + 1, "%hhu %hu", &num_valv, &x);
          misValvulas[num_valv]->emptyng_millis(x);
          Serial.print("Emptying valve ");
          Serial.print(num_valv);
          Serial.print(" for ");
          Serial.print(x);
          Serial.println(" ms");
          break;

        case 'c':
          num_valv = input.substring(1).toInt();
          misValvulas[num_valv]->Cerrada();
          Serial.print("Valve ");
          Serial.print(num_valv);
          Serial.println(" closed");
          break;

        case 'M':
          if (real_robot) {
            Serial.print("S ");
            for (uint8_t i = 0; i < NUM_SENSORES; i++) {
              misSensores[i]->measure();
            }
            Serial.println();
          }
          break;
      }
    }
  }

  for (uint8_t i = 0; i < NUM_VALVULAS; i++) {
    misValvulas[i]->callback();
    if (misValvulas[i]->getEmergency()) {
      State = S_ERROR_STOPAUTO;
    }
  }

  if (State == S_ERROR_STOPAUTO) {
    digitalWrite(13, !digitalRead(13));
    delay(100);
  }
}
