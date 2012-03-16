/*
 * uart.c
 *
 * Created: 10.03.2012 01:09:57
 *  Author: armageddon
 */ 

#include "uart.h"
 
volatile uint8_t uart_str_complete = 0;     // 1 .. String komplett empfangen
volatile uint8_t uart_str_count = 0;
volatile char uart_string[UART_MAXSTRLEN + 1] = "";
volatile char uart_string_tmp[UART_MAXSTRLEN + 1] = "";

char text[160];

uint8_t hastoconnect = 0;

ISR(USART_RXC_vect)
{
  unsigned char nextChar;
 
  // Daten aus dem Puffer lesen
  nextChar = UDR;
  
  /*uart_string[0] = nextChar;
  uart_string[1] = 0;
  uart_str_complete = 1;
  uart_putc(nextChar);
  return;*/
  
	 
	  
    // Daten werden erst in uart_string geschrieben, wenn nicht String-Ende/max Zeichenlänge erreicht ist/string gerade verarbeitet wird
    if( nextChar != '\n' &&
        nextChar != '\r' &&
        uart_str_count < UART_MAXSTRLEN - 1 ) {
      uart_string_tmp[uart_str_count] = nextChar;
      uart_str_count++;
    }
    else {
      uart_string_tmp[uart_str_count] = '\0';
      uart_str_count = 0;
	  
	  if(uart_str_complete == 0 && uart_string_tmp[0] == '/'){
		  uint8_t i=0;
		  while(uart_string_tmp[i]){
			  uart_string[i] = uart_string_tmp[i];
			  i++;
		  }
		  uart_string[i] = 0;
		  
		  uart_str_complete = 1;
	  }
	  else{
		  //uart_str_complete = 0;
	  }
	  
  }
}


int uart_putc(unsigned char c)
{
    while (!(UCSRA & (1<<UDRE)));  /* warten bis Senden moeglich */                             
    UDR = c;                      /* sende Zeichen */
    return 0;
}
 
 
/* puts ist unabhaengig vom Controllertyp */
void uart_puts (char *s)
{
    while (*s)
    {   /* so lange *s != '\0' also ungleich dem "String-Endezeichen(Terminator)" */
        uart_putc(*s);
        s++;
    }
}

void uart_init(void)
{
  UBRRH = UBRR_VAL >> 8;
  UBRRL = UBRR_VAL & 0xFF;
  UCSRC = (1<<URSEL)|(1<<UCSZ1)|(1<<UCSZ0); // Asynchron 8N1 
  UCSRB |= (1<<RXEN)|(1<<TXEN)|(1<<RXCIE);  // UART RX, TX und RX Interrupt einschalten
  
  text[0] = 0;
}

uint8_t connect(){
	
	if(hastoconnect){
		_delay_ms(2);
		uart_puts("\r\ntelnet alphafluid.shack 1337\r\n");
		_delay_ms(30);
		uart_puts("/o/i/booting\r\n");
	}		
	
	return 0;
}

void parse(char *msg){
	if(msg[1] != '/') return;
	char *str = seg_getstring();
	
	switch(msg[0]){
		case 'w':	//Welcome reply
			hastoconnect = 0;
			strcpy(str, "connected   ");
			/*for(uint8_t i=0;i<12;i++){
				test();
				_delay_ms(300);
			}*/
			uint16_t *ov = mat_getOfflineValues();
			for(uint8_t i=0;i<6;i++){
				while((ov[i]) > 0){
					ov[i]--;
					char tmp[20];
					strcpy(tmp, "/o/o/");	//out,empty
					itoa(i,tmp+strlen(tmp),10);
					strcpy(tmp+strlen(tmp), "\r\n");
					uart_puts(tmp);
					_delay_ms(10);
				}
				
			}
			break;
		case 't':	//set text to be displayed (twitter?)
			strcpy(text, msg+2);
			break;
		case 's':
			if(strlen(msg+2) >= 3 && msg[3] == ' '){
				//strcpy(text, msg+2);
				uart_puts(msg);
				msg[3] = 0;
				uint8_t index = strtoul(msg+2,0,10);
				uint16_t val = strtoul(msg+4,0,10);
				if(index<6)
					mat_set(index, val);
			}
			else{
				uart_puts("/o/a/wrong format\r\n");
			}
			
			break;
	}	
	
}

char* con_getText(){
	return text;
}

uint8_t isConnected(){
	return (hastoconnect)?0:1;
}

uint8_t uart_process(){
		
		if(!uart_str_complete) return 1;
		
		point(); 
		
		if(uart_string[0] == '/' &&
				uart_string[1] == 'i' &&
				uart_string[2] == '/'){
					parse(uart_string+3);
					uart_str_complete = 0;
					return 0;
				}
		
		char *str = uart_string;
		
		while(str[2]){
			if(str[0] == '/' &&
			str[1] == ' ' &&
			str[2] == '#'){
				
				uart_str_complete = 0;
				hastoconnect = 1; //makes to connect call pass
				return 0;
			}
			str++;
		}
		
		uart_str_complete=0;
		
	
	return 0;
}