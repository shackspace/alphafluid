/*
 * AVRGCC3.c
 *
 * Created: 06.03.2012 20:29:49
 *  Author: armageddon
 */


#include "main.h"


int main(void)
{
	
	uint8_t delay1 = 0, delay2 = 0, delay3 = 0;
	
	seg_init();
	mat_init();
	uart_init();
	sei();
	
	uart_puts("\n\n");
	uart_puts("/o/i/booting\r\n");
	
    while(1)
    {	
		
		for(uint8_t i=0; i<3;i++) uart_process();
		
		
		delay2++;
		if(delay2 == 200){
			delay2 = 0;
			mat_check();		
			
			
			delay1++;
			if(delay1 == 200){
				delay1 = 0;
				mat_debug();
				test();
				uart_puts("d\r\n");
				
				if(delay3 == 10){
					delay3 = 0;
					uart_puts("\n");
				}
				connect(); //checks hastoconnect variable
			}
		}			
		_delay_us(5);
    }
}

