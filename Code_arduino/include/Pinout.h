//En este fichero estarán definidos todos los pines de E/S

#ifndef _PINOUT_H_
#define _PINOUT_H_

#include "Config.h"
#define NUM_VALVULAS 9

// ############# Valvulas #################

// valvulas 3/2

    const uint8_t PIN_32_ARRAY[NUM_VALVULAS] = 
    {
        25, // 1 
        34, // 2
        32, // 3
        24,  // 4
        26,  // 5
        30,  // 6
        36,  // 7
        22,  // 8
        28   // 9
    };

    

// valvulas 2/2

    const uint8_t PIN_22_ARRAY[NUM_VALVULAS] = 
    {
        23, // 0
        35, // 1
        41, // 2
        29, // 3  
        27, // 4
        39, // 5
        37, // 6
        33, // 7
        31 // 8
    };

    const uint8_t EMRGY_PIN = 9;
    const uint8_t LED_PIN = 0;

    const uint8_t PIN_LED_R = 2;
    const uint8_t PIN_LED_G = 3;
    const uint8_t PIN_LED_B = 4;
    



#endif // _PINOUT_H_