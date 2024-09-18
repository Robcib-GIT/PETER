#include "Valvula.h"



void Valvula::init()
{
    pinMode(pin_32, OUTPUT);
    pinMode(pin_22, OUTPUT);

    state = S_CLOSED;
    modof = M_LIB;
    actual_pressure_percent = 0;
    max_rel_pressure = 100;
    timing_active = false;
    emergency_halted = false;
    actual_pressure = 0;
}

void Valvula::alAire()
{
    state = S_EMPTYING;
    

    digitalWrite(pin_32, LOW);
    digitalWrite(pin_22, HIGH);
}

void Valvula::Presion()
{
    state = S_FILLING;
    
    if(state != S_EMERGENCY_STOP)
    {
    digitalWrite(pin_32, HIGH);
    digitalWrite(pin_22, HIGH);
    }
}

void Valvula::Cerrada()
{
    state = S_CLOSED;
    
    if(state != S_EMERGENCY_STOP)
    {
    digitalWrite(pin_32, LOW);
    digitalWrite(pin_22, LOW);
    }
}

void Valvula::fill_millis_private(uint32_t time)
{
    if(state == S_EMERGENCY_STOP) return;

    // Se  pone en modo llenar
    this->Presion();

    // Activamos la temporizacion
    timing_active = true;

    // Se guarda tiempo de comienzo
    first_time = millis();

    // MS que se quieren alcanzar
    final_time = time;

    control_time = millis();

    state = S_FILLING;
    

}

void Valvula::emptyng_millis_private(uint32_t time)
{
    if(state == S_EMERGENCY_STOP) return;

    this->alAire();
    timing_active = true;
    first_time = millis();
    final_time = time;
    control_time = millis();

    state = S_EMPTYING;
    
}

void Valvula::callback()
{
    if(timing_active)
    {
        
        if(millis() - first_time > final_time)
        {
            this -> Cerrada();
            timing_active = false;
        }
    }

    // Para el control de seguridad
    //static int first = millis();

    // Controlamos el estado de la presion actual.
    // Si se esta llenando o vaciando, se va actualizando cada 10ms
    if(state == S_FILLING || state == S_EMPTYING)
    {
        // Si esta en un estado distinto de cerrado durante mas de 10ms
        if(millis() - control_time >= 10)
        {
            if(state == S_FILLING)
            {
                actual_pressure += 10;
            }
            else if(state == S_EMPTYING)
            {
                actual_pressure -= 10;
                if(actual_pressure < 0) actual_pressure = 0;
            }
            
            control_time = millis();
        }
    }

    // Si la presion actual en algun momento supera la maxima, se entra en modo de emergencia
    if(actual_pressure > MAX_PRESSURE)
    {
        this ->alAire();
        state = S_EMERGENCY_STOP;
        emergency_halted = true;
    }
    

    
}

uint32_t Valvula::comp_eq_empt_millis(uint32_t ms)
{
    float eqms_f = (float)  (transf_mult *  ms);
    return (uint32_t) eqms_f;
}



void Valvula::relC(int data)
{
    if(state == S_EMERGENCY_STOP) return;

    if(modof == M_ABS)
    {
        // Habria que hacer el vaciado de porseacaso
        actual_pressure_percent = 0;
    }


    // Ponemos mood porcentual
    modof = M_REL;

    // Tiene que ser un dato mayor que 0 y menor que 100
    if(data > 100 || data < 0) return;

    // Primero comparamos con lo que esta 
    int porcentaje_cambiar = data - actual_pressure_percent;

    Serial.print("a cambiar: ");
    Serial.println(porcentaje_cambiar);

    // Si es mayor que 0, hay que llenar
    if(porcentaje_cambiar > 0)
    {
        uint32_t presion_a_enviar = (uint32_t)((max_rel_pressure/100) * porcentaje_cambiar);
        Serial.print("a enviar: ");
        Serial.println(porcentaje_cambiar);
        // Hinchamos lo necesario
        this -> fill_millis_private(presion_a_enviar);
        actual_pressure_percent = data;
    }
    else
    {
        porcentaje_cambiar = - porcentaje_cambiar;
        uint32_t presion_a_enviar = (uint32_t)((max_rel_pressure/100) * porcentaje_cambiar);
        presion_a_enviar = this->comp_eq_empt_millis(presion_a_enviar);
        this -> emptyng_millis_private(presion_a_enviar);
        actual_pressure_percent = data;
    }

    Serial.print("porcentaje actual: ");
    Serial.println(actual_pressure_percent);
}

void Valvula::security_emptyng()
{
    // TODO
}

void Valvula::rearmar()
{
    if(state == S_EMERGENCY_STOP)
    {
        
        state = S_EMPTYING;
        this -> emptyng_millis_private(3000);
        emergency_halted = false;

        actual_pressure = 0;
        actual_pressure_percent = 0;


    }
}
