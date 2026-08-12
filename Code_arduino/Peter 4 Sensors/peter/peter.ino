#include <Arduino.h>
#include "Config.h"
#include "Sensor.h"

#define XSHUT_PIN_1 6
#define XSHUT_PIN_2 7

modes State = S_NORMAL;
uint8_t real_robot = 1;
SensorBNO055 sensor1;
SensorVL53L0X sensor2;
SensorBNO055_alt sensor3;
SensorVL53L0X_alt sensor4;
Sensor* misSensores[] =
{
    &sensor1,
    &sensor2,
    &sensor3,
    &sensor4
};

void setup() {
  Serial.begin(115200);
  delay(100); // Dar tiempo al puerto Serie para estabilizarse

  // 1. PRIMERO: Iniciar bus I2C antes de configurar cualquier sensor
  Wire.begin();
  Serial.print("asdfadsf");

  pinMode(EMRGY_PIN, INPUT_PULLUP);
  pinMode(XSHUT_PIN_1, OUTPUT);
  pinMode(XSHUT_PIN_2, OUTPUT);
  
  // Apagamos los VL53L0X para reiniciar sus direcciones I2C
  digitalWrite(XSHUT_PIN_1, LOW);
  digitalWrite(XSHUT_PIN_2, LOW);
  delay(100);

  Serial.println("Hola");

  Serial.println("Adiós");

  // Encender primer VL53L0X y darle tiempo a arrancar
  digitalWrite(XSHUT_PIN_1, HIGH);
  delay(300); 
  ((SensorVL53L0X*)misSensores[1])->begin();

  // Encender segundo VL53L0X
  digitalWrite(XSHUT_PIN_2, HIGH);
  delay(300);
  ((SensorVL53L0X_alt*)misSensores[3])->begin();

  // Iniciar BNO055
  misSensores[0]->begin();
  misSensores[2]->begin();

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(2, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  State = S_NORMAL;
  Serial.println("PETER está listo");
}

void loop() {
  
  if (real_robot) {
    Serial.print("S ");
    for (uint8_t i = 0; i < NUM_SENSORES; i++) {
      if (misSensores[i] != nullptr) misSensores[i]->measure();
    }
    Serial.println();
  }

  if (Serial.available() > 0) {
    char op = Serial.read();
    uint8_t num_valv;
    uint16_t x;

    switch (op) {
      case 'i':
        real_robot = Serial.parseInt();
        Serial.println("Working mode changed");
        break;

      case 'M': {
        String input = Serial.readStringUntil('\n');
        input.trim();

        if (real_robot) {
          Serial.print("S ");
          for (uint8_t i = 0; i < NUM_SENSORES; i++) {
            if (misSensores[i] != nullptr) misSensores[i]->measure();
          }
          Serial.println();
        }
        break;
      }
    }
  }

  delay(5);
}