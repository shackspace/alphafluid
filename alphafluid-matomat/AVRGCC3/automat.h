/*
 * IncFile1.h
 *
 * Created: 07.03.2012 19:33:02
 *  Author: armageddon
 */ 


#ifndef INCFILE1_H_
#define INCFILE1_H_

#include <avr/io.h>
#include <stdlib.h>
#include <string.h>
#include <avr/eeprom.h>

#include "7seg.h"
#include "uart.h"

#define MAT_1_PIN	PINA
#define MAT_1		PA0
#define MAT_2_PIN	PINA
#define MAT_2		PA1
#define MAT_3_PIN	PINA
#define MAT_3		PA2
#define MAT_4_PIN	PINA
#define MAT_4		PA3
#define MAT_5_PIN	PINA
#define MAT_5		PA4
#define MAT_6_PIN	PINA
#define MAT_6		PA5
#define MAT_12_PIN	PINA
#define MAT_12		PA6
#define MAT_11_PIN	PINA
#define MAT_11		PA7
#define MAT_10_PIN	PINB
#define MAT_10		PB0
#define MAT_9_PIN	PINB
#define MAT_9		PB1
#define MAT_8_PIN	PINB
#define MAT_8		PB2
#define MAT_7_PIN	PINB
#define MAT_7		PB3

#define MAT_DOOR_PIN	PINC
#define MAT_DOOR_PORT	PORTC
#define MAT_DOOR		PC0



#define MAT_COUNTER_ADDRESS 0

void mat_init();
void mat_read();
void mat_check();
void mat_debug();
void mat_set(uint8_t slot, uint8_t val);
uint16_t* mat_getOfflineValues();


#endif /* INCFILE1_H_ */