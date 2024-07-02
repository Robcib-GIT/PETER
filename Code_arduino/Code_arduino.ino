#include "Config.h"
#include "RobotSegment.h"
#include "Valvula.h"

#define P_V_RATIO (8.7 - 9) / 400

// ############### Objetos globales ################

// Numero de valvulas. Se considera valvula al conjunto de una 22 + una 23

// Sensor
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28, &Wire);

// Si se trabaja con robot real o con modelo (el dato lo manda Matlab, aunque por seguridad se dice que modelo)
uint8_t real_robot = 0;
const float length_constant = 0.05;

// Modo normal
modos State = S_NORMAL;

const uint32_t calibration_millis = 5000;

// Variable de estado
char cmode;
long int t = 0;
long int t1 = 0;
double datos[3];
int x = 0;

// Array de valvulas
Valvula *misValvulas[NUM_VALVULAS];


//Interrupcion emergencia
void emergency_stop_callback()
{
  State = S_ERROR_PARADA_EMERGENCIA;
  for(uint8_t i = 0; i < NUM_VALVULAS; i++)
  {
    misValvulas[i] -> alAire();
  }

}


/*void current_measure_init() {
    ina_0.begin(&Wire);
    ina_0.reset();
    ina_0.setShuntRes(100, 100, 100);
}*/

void setup()
{

  // Comunicacion con el PC
  Serial3.begin(115200);

  // Comunicacion con ESP32 (Interfaz wifi para desarollo)
  //Serial2.begin(9600);
  
  // Inicializamos los pines de la marca de la vision por omputador
  pinMode(PIN_LED_R, OUTPUT);
  pinMode(PIN_LED_G, OUTPUT);
  pinMode(PIN_LED_B, OUTPUT);


  //attachInterrupt(digitalPinToInterrupt( EMRGY_PIN), emergency_stop_callback, CHANGE);
  pinMode(EMRGY_PIN, INPUT_PULLUP);

  // Instanciamos las valvulas
  for (int i = 0; i < NUM_VALVULAS; i++)
  {
    misValvulas[i] = new Valvula(PIN_32_ARRAY[i], PIN_22_ARRAY[i]);
  }

  // Inicilaizamos las valvulas
  for (int i = 0; i < NUM_VALVULAS; i++)
  {
    misValvulas[i]->init();
  }


  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(2, OUTPUT);

  // Inicializamos los sensores
  digitalWrite(LED_BUILTIN, HIGH);
  while (!Serial) delay(10);  // wait for serial port to open!
  if (!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while (1);
  }
  
  Wire.begin();
  //current_measure_init();

  t = millis();

  /*
  // Calibracion de los sensores
  while(millis() - t < calibration_millis) {
    sensor1.calibrate();
    sensor2.calibrate();
    sensor3.calibrate();
  }
  */
  digitalWrite(LED_BUILTIN, LOW);

  // Se imprimen por Serial los valores calibrados de los sensores
  /*Serial3.print(sensor1.getMaxCalibratedValue());
  Serial3.print(" ");
  Serial3.println(sensor1.getMinCalibratedValue());
  Serial3.print(sensor2.getMaxCalibratedValue());
  Serial3.print(" ");
  Serial3.println(sensor2.getMinCalibratedValue());
  Serial3.print(sensor3.getMaxCalibratedValue());
  Serial3.print(" ");
  Serial3.println(sensor3.getMinCalibratedValue());*/
  Serial3.println("Calibration done");

  t = millis();

  // Modo normal
  State = S_NORMAL;
  // delay(1000);
}

void loop()
{
  if(State == S_NORMAL)
  {
  
  t1 = millis();

  if (Serial3.available() > 0)
  {
    static char op = ' ';
    op = Serial3.read();
    int num_valv;
    //int x;
    float p;
    int buffer[NUM_VALVULAS + 1];
    switch (op)
    {

    // decir si trabajamos con un robot real o ficticio
    case 'i':
      real_robot = Serial3.parseInt();
      Serial3.println("Working mode changed");
      break;

    // abrir valvula
    case 'a':
      num_valv = Serial3.parseInt();
      Serial3.println(num_valv);
      misValvulas[num_valv]->alAire();
      break;

    // cerrar valvula
    case 'b':
      num_valv = Serial3.parseInt();
      misValvulas[num_valv]->Cerrada();
      break;

    // a presion
    case 'c':
      num_valv = Serial3.parseInt();
      misValvulas[num_valv]->Presion();
      break;

    // llenar durante x ms
    case 'f':
      num_valv = Serial3.parseInt();
      x = Serial3.parseInt();
      misValvulas[num_valv]->fill_millis((uint16_t)x);
      break;

    // vaciar durante x ms
    case 'e':
      num_valv = Serial3.parseInt();
      x = Serial3.parseInt();
      misValvulas[num_valv]->emptyng_millis((uint16_t)x);
      break;

    // Medir los valores de los sensores
    case 'M':
      //Serial3.print("M ");
      if (real_robot) {
        // Read IMU data and send it back to Python
        sensors_event_t orientationData;
        bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
        Serial3.print(orientationData.orientation.x);
        Serial3.print(",");
        Serial3.print(orientationData.orientation.y);
        Serial3.print(",");
        Serial3.println(orientationData.orientation.z);
      } else {
        for (uint8_t i = 0; i < NUM_VALVULAS; i++) {
          int p = misValvulas[i]->get_actual_pressure();
          Serial3.print(9 + p * P_V_RATIO);
          Serial3.print(" ");
        }
      }
      Serial3.println(" ");
    break;

    // Para escribir un dato para todas las valvulas en modo absoluto
    case 'w':
    
      for (int i = 0; i < NUM_VALVULAS + 1; i++)
      {
        buffer[i] =  Serial3.parseInt();
      }

      for (int i = 1; i < NUM_VALVULAS + 1; i++)
      {
        if (buffer[0])
        {
          if (buffer[i] >= 0)
          {
            misValvulas[i - 1]->fill_millis(buffer[i]);
          }
          else
          {
            misValvulas[i - 1]->emptyng_millis(-buffer[i]);
          }
        }
        else
        {
          misValvulas[i - 1] -> relC(buffer[i]);
        }
      }

      break;

      // Para cambiar el brillo de las luces r,g,b de la marca de la vision por computador
      case 'v':
      case 'V':
        
        // rgb
        num_valv = Serial3.parseInt();
        x = Serial3.parseInt();
        switch(num_valv)
        {
          // r
          case 1:
            analogWrite(PIN_LED_R, x > 0? (x > LED_MAXV_R? LED_MAXV_R : x  ) : 0 );
          break;
          // g
          case 2:
            analogWrite(PIN_LED_G, x > 0? (x > LED_MAXV_G? LED_MAXV_G : x  ) : 0 );
          break;
          // b
          case 3:
            analogWrite(PIN_LED_B, x > 0? (x > LED_MAXV_B? LED_MAXV_B : x  ) : 0 );
          break;
        }

      break;

     

      // Para cambiar la presion maxima en modo relativo
      case 'l':
        p = Serial3.parseFloat();
        for (int i = 0; i < NUM_VALVULAS; i++)
        {
          misValvulas[i] ->  set_max_rel_pressure(p);
        }

      break;

      // Para cambiar ratio inflado/desinflado
      case 'm':
        p = Serial3.parseFloat();
        for (int i = 0; i < NUM_VALVULAS; i++)
        {
          misValvulas[i] ->  set_mult(p);
        }

      break;

    // Modo relativo en una sola valvula
    case 'x':
      num_valv = Serial3.parseInt();
      x = Serial3.parseInt();
      misValvulas[num_valv]->relC(x);
      break;

    case 'k':
      
      for(int i = 0; i < NUM_VALVULAS; i++)
      {
        int pres = Serial3.parseInt();
        misValvulas[i]->relC( pres);
        Serial3.print(i);
        Serial3.print(" ");
        Serial3.println(pres);

        delay(2);
      }
      
    break;

    
    }
  }


  // Callback de las valvulas   
  for (uint8_t i = 0; i < NUM_VALVULAS; i++)
  {
    misValvulas[i]->callback();
  }

  // Comunicacion con ESP32
  /*if (Serial2.available() > 0)
  {

    static char op = ' ';
    op = Serial3.read();
    Serial3.println(op);
    int num_valv;

    switch (op)
    {
    // abrir valvula
    case 'a':
      num_valv = Serial2.parseInt();
      Serial3.println(num_valv);
      misValvulas[num_valv]->alAire();
      break;

    // cerrar valvula
    case 'b':
      num_valv = Serial2.parseInt();
      misValvulas[num_valv]->Cerrada();
      break;

    // a presion
    case 'c':
      num_valv = Serial2.parseInt();
      misValvulas[num_valv]->Presion();
      break;
    }
  }*/

  
  // Comprobamos si alguna valvula ha entrado en modo de parada de emergencia
   for(uint8_t i = 0; i < NUM_VALVULAS; i++)
   {
    if(misValvulas[i]-> getEmergency() == true)
    {
      State = S_ERROR_STOPAUTO;
    }
    
   }
  
  
  }
 
  


  if(State == S_ERROR_STOPAUTO)
  {
    // Parpadea el led
    digitalWrite(13, !digitalRead(13));
    delay(100);

    if( Serial3.available() > 0)
    {
      char op = Serial3.read();

      // Rearmamos
      if(op == 'R')
      {
        for (int i = 0; i < NUM_VALVULAS; i++)
        {
          misValvulas[i] -> rearmar();
          State = S_NORMAL;
        }
      }

    }

  }

  
}
