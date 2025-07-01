#include "SerialCommunication.h"

void SerialCommunication_publish_int(int* data, uint8_t nArg)
{
    if(Serial.available() > 0)
    {
        for (int i = 0; i < nArg; i++)
        {
            Serial.println(data[i]);
        } 
    }
}

char SerialCommunication_getMode()
{
    if(Serial.available() > 0)
    {
        return Serial.read();
    }
    else
    {
        return 'f';
    }
}

void SerialCommunication_receive_int(int* data, uint8_t nArg)
{
    if(Serial.available() > 0)
    {
        for (int i = 0; i < nArg; i++)
        {
            data[i] = Serial.parseInt(SKIP_WHITESPACE);
        } 
    }
}