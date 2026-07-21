#include <Arduino.h>
#include "Config.h"
#include "Sensor.h"

#define XSHUT_PIN_1 6
#define XSHUT_PIN_2 7

modes State = S_NORMAL;
uint8_t real_robot = 1;
Sensor *misSensores[NUM_SENSORES];

bool autoSerial = false;

void setup() {
  Serial.begin(115200);

  Wire.begin();
  Wire.setClock(100000);

  pinMode(EMRGY_PIN, INPUT_PULLUP);
  pinMode(XSHUT_PIN_1, OUTPUT);
  pinMode(XSHUT_PIN_2, OUTPUT);
  digitalWrite(XSHUT_PIN_1, LOW);
  digitalWrite(XSHUT_PIN_2, LOW);
  delay(10);

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
  digitalWrite(LED_BUILTIN, LOW);
  
  State = S_NORMAL;

  // --- HANDSHAKE: Avisamos a MATLAB de que los sensores están listos ---
  delay(500);
  Serial.println("READY_PETER");
}

void loop() {
  // 1. LEER COMANDOS SIEMPRE (Sin "else if")
  if (Serial.available() > 0) {
    char op = Serial.read();

    switch (op) {
      case 'T': 
        Serial.println(millis());
        break;
      
      case 'M': {
        String input = Serial.readStringUntil('\n');
        input.trim();
        if (real_robot) {
          Serial.print("S ");
          for (uint8_t i = 0; i < NUM_SENSORES; i++) {
            misSensores[i]->measure();
          }
          Serial.println();
        }
        break;
      }

      case 'S': 
        autoSerial = 1; // Encender transmisión
        break;
        
      case 'Q':
        autoSerial = 0; // Apagar transmisión (Callar)
        break;
    }
  }

  // 2. ENVIAR DATOS (De forma independiente)
  if (autoSerial) {
    Serial.print("S ");
    Serial.print(",");
    for (uint8_t i = 0; i < NUM_SENSORES; i++) {
      misSensores[i]->measure();
    }
    Serial.println();
  }

  if (State == S_ERROR_STOPAUTO) {
    digitalWrite(13, !digitalRead(13));
    delay(100);
  }
  delay(5);
}
