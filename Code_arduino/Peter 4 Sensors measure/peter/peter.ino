#include <Arduino.h>
#include "Config.h"
#include "Sensor.h"

#define XSHUT_PIN_1 6
#define XSHUT_PIN_2 7

modes State = S_NORMAL;
uint8_t real_robot = 1;
Sensor *misSensores[NUM_SENSORES];

bool autoSerial = true;

void setup() {
  Serial.begin(115200);

  Wire.begin();
  Wire.setClock(100000);
  Wire.setWireTimeout(3000, true); // <-- AÑADIR: Resetea el bus si se cuelga más de 3ms

  pinMode(EMRGY_PIN, INPUT_PULLUP);
  // 1. Apagar AMBOS ToF
  pinMode(XSHUT_PIN_1, OUTPUT);
  pinMode(XSHUT_PIN_2, OUTPUT);
  digitalWrite(XSHUT_PIN_1, LOW);
  digitalWrite(XSHUT_PIN_2, LOW);
  delay(100); // Pausa para asegurar que se reinicien del todo

  // Instanciar objetos
  misSensores[0] = new SensorBNO055();
  misSensores[1] = new SensorVL53L0X();
  misSensores[2] = new SensorBNO055_alt();
  misSensores[3] = new SensorVL53L0X_alt();

  // 2. Encender e inicializar el PRIMER ToF (0x30)
  digitalWrite(XSHUT_PIN_1, HIGH);
  delay(200);
  ((SensorVL53L0X*)misSensores[1])->begin();

  // 3. Encender e inicializar el SEGUNDO ToF (0x31)
  digitalWrite(XSHUT_PIN_2, HIGH);
  delay(200);
  ((SensorVL53L0X_alt*)misSensores[3])->begin();

  // 4. Inicializar IMUs
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
  delay(50);
}
