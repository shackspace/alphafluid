/*
 * IncFile1.h
 *
 * Created: 06.03.2012 20:38:41
 *  Author: armageddon
 */ 


#ifndef INCFILE2_H_
#define INCFILE2_H_

#include <avr/io.h>
#include <util/delay.h>
#include <string.h>
#include <stdlib.h>

#define SEG_DATA_DDR	DDRD
#define SEG_DATA_PORT	PORTD
#define SEG_DATA		PD7
#define SEG_SCK_DDR		DDRD
#define SEG_SCK_PORT	PORTD
#define SEG_SCK			PD6
#define SEG_STORE_DDR	DDRD
#define SEG_STORE_PORT	PORTD
#define SEG_STORE		PD5
#define SEG_EN_DDR		DDRD
#define SEG_EN_PORT		PORTD
#define SEG_EN			PD4


void seg_init();
void test();
void seg_setstring(char s[]);
void push(uint8_t data);
void latch();
uint8_t convert (char ch); //convert char to encoded char
void update(); //push the buffer array
void addch(uint8_t ch); //add encoded char to the right (push left)
char *seg_getstring();
void point();

#endif /* INCFILE2_H_ */