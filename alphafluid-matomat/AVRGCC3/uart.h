/*
 * uart.h
 *
 * Created: 10.03.2012 01:09:49
 *  Author: armageddon
 */ 


#ifndef UART_H_
#define UART_H_

#include <avr/interrupt.h>
#include <avr/io.h>
#include <util/delay.h>
#include <string.h>

#include "7seg.h"
#include "automat.h"


#define UART_MAXSTRLEN 160

#define BAUD 115200UL      // Baudrate

// Berechnungen
#define UBRR_VAL ((F_CPU+BAUD*8)/(BAUD*16)-1)   // clever runden
#define BAUD_REAL (F_CPU/(16*(UBRR_VAL+1)))     // Reale Baudrate
#define BAUD_ERROR ((BAUD_REAL*1000)/BAUD) // Fehler in Promille, 1000 = kein Fehler.
 
#if ((BAUD_ERROR<990) || (BAUD_ERROR>1010))
  #error Systematischer Fehler der Baudrate grösser 1% und damit zu hoch! 
#endif 

int uart_putc(unsigned char c);
void uart_puts (char *s);
void uart_init(void);
void parse(char *msg);
uint8_t uart_process();
uint8_t connect();
uint8_t isConnected();
char* con_getText();
#endif /* UART_H_ */