#ifndef _SERIALCOMMUNICATION_H_
#define _SERIALCOMMUNICATION_H_

#include "Config.h"

void SerialCommunication_publish_int(int* data, uint8_t nArg);

void SerialCommunication_receive_int(int* data, uint8_t nArg);
char SerialCommunication_getMode();




#endif // _SERIALCOMMUNICATION_H_