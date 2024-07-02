#ifndef VALVULA_H
#define VALVULA_H

// Clase que maneja cada una de las valvulas

#include "Arduino.h"

// Constante para compensar la velocidad de vaciado, menor que la de llenado
const float io_multiplier = 1.2;

// Maximos ms que debe estar abierta la valvula
//const int MAX_PRESSURE = 2500;
const int MAX_PRESSURE = 1e6;

// Posibles estados de la valvula
enum mode
{
    S_FILLING,
    S_EMPTYING,
    S_CLOSED,
    S_EMERGENCY_STOP,
    S_SECURITY_EMPTYNG
};

// Posibles modos de funcionamiento
//      -> M_ABS: Cuando se pide llenar/ vaciar durante una cantidad de ms no determinada
//      -> M_REL: Modo relativo, cuando se le indica a la valvula que hinche entre el 0 y 100%
//  	-> M_LIB: Modo libre, simplemente se controla el estado de la valvula
enum modef
{
    M_ABS,
    M_REL,
    M_LIB
};

class Valvula
    {
        private:

            // Pines a los que esta conectada la electrovalvula 3/2 y 2/2 respectivamente
            uint8_t pin_32;
            uint8_t pin_22;

            // Estado de la valvula
            mode state;

            // Modo de funcionamiento
            modef modof;        

            bool timing_active;
            bool filling;

            
            uint32_t first_time;
            uint32_t final_time;
            uint32_t control_time;


            bool emergency_halted;
            int actual_pressure;

            // Metodo que transforma los millisegundos a millisegundos de vaciado equivalente
            uint32_t comp_eq_empt_millis(uint32_t);
            float transf_mult = io_multiplier;

            // Porcentaje de llenado en control porcentual
            int actual_pressure_percent;
            float max_rel_pressure;

            // Desinflado de seguridad
            void security_emptyng();
            
            void fill_millis_private(uint32_t);
            void emptyng_millis_private(uint32_t);

        public:
            // Constructor
            Valvula(uint8_t pin_32, uint8_t pin_22)
            {
                this->pin_32 = pin_32;
                this->pin_22 = pin_22;
            }

            // Inicializa los pines
            void init();

            // Para vaciar
            void alAire();

            // Para llenar
            void Presion();

            // Mantener la presion
            void Cerrada();

            // Llenar durante x millis
            void fill_millis(uint32_t d)
            {
                modof = M_ABS;
                this ->fill_millis_private(d);
            };

            // Vaciar durante x millis
            void emptyng_millis(uint32_t d)
            {
                modof = M_ABS;
                this ->emptyng_millis_private(d);
            };

            // Control porcentual
            void relC(int);

            

            // Funcion callback que tiene que llamarse de forma ciclica. Sumamente importante
            void callback();



            bool getEmergency()
            {
                return emergency_halted;
            }

            int get_actual_pressure()
            {
                return actual_pressure;
            }

            void set_mult(float a)
            {
                transf_mult = a;
            }

            void set_max_rel_pressure(float a)
            {
                max_rel_pressure = a > MAX_PRESSURE? MAX_PRESSURE : a;
            }

            void rearmar();

    };



#endif
