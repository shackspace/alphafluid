/*
 * CProgram1.c
 *
 * Created: 07.03.2012 19:32:49
 *  Author: armageddon
 */ 

#include "automat.h"

uint8_t mat_status[12];

uint16_t mat_counter[6];
uint16_t mat_offline_counter[6];



void mat_init(){
	
	
	/* und nun mit 16-Bit Array */
	//eeprom_read_block (mat_counter, MAT_COUNTER_ADDRESS, sizeof(mat_counter));
	
	for(uint8_t i=0; i<6;i++){
		//if(mat_counter[i] == 0xffff) mat_counter[i] = 0;
		mat_counter[i] = 0;
	}
	
	/* Datenblock in EEPROM schreiben */
	//eeprom_write_block (mat_counter, MAT_COUNTER_ADDRESS, sizeof(mat_counter));
	
}

void mat_read(){
	
	DDRA = 0;
	mat_status[0] += (MAT_1_PIN & (1<<MAT_1))?((mat_status[0]==255)?0:1):-mat_status[0];
	mat_status[1] += (MAT_2_PIN & (1<<MAT_2))?((mat_status[1]==255)?0:1):-mat_status[1];
	mat_status[2] += (MAT_3_PIN & (1<<MAT_3))?((mat_status[2]==255)?0:1):-mat_status[2];
	mat_status[3] += (MAT_4_PIN & (1<<MAT_4))?((mat_status[3]==255)?0:1):-mat_status[3];
	mat_status[4] += (MAT_5_PIN & (1<<MAT_5))?((mat_status[4]==255)?0:1):-mat_status[4];
	mat_status[5] += (MAT_6_PIN & (1<<MAT_6))?((mat_status[5]==255)?0:1):-mat_status[5];
	mat_status[6] += (MAT_7_PIN & (1<<MAT_7))?((mat_status[6]==255)?0:1):-mat_status[6];
	mat_status[7] += (MAT_8_PIN & (1<<MAT_8))?((mat_status[7]==255)?0:1):-mat_status[7];
	mat_status[8] += (MAT_9_PIN & (1<<MAT_9))?((mat_status[8]==255)?0:1):-mat_status[8];
	mat_status[9] += (MAT_10_PIN & (1<<MAT_10))?((mat_status[9]==255)?0:1):-mat_status[9];
	mat_status[10] += (MAT_11_PIN & (1<<MAT_11))?((mat_status[10]==255)?0:1):-mat_status[10];
	mat_status[11] += (MAT_12_PIN & (1<<MAT_12))?((mat_status[11]==255)?0:1):-mat_status[11];
	
}



void mat_check(){
	
	mat_read();
	
	for(uint8_t i=0; i<6;i++){
		
		if(mat_status[i]==254){
			if(mat_counter >0)
				mat_counter[i]--;
			if(isConnected()){
				char tmp[20];
				strcpy(tmp, "/o/b/");	//out,empty
				itoa(i,tmp+strlen(tmp),10);
				strcpy(tmp+strlen(tmp), "\r\n");
				uart_puts(tmp);
			}
			else{
				mat_offline_counter[i]++;
			}
			
			/* Datenblock in EEPROM schreiben */
			//eeprom_write_block (mat_counter, MAT_COUNTER_ADDRESS, sizeof(mat_counter));
			
		}
		
	}
	
	for(uint8_t i=6; i<12;i++){
		
		if(mat_status[i]==254){
			mat_counter[i]=0;
			if(isConnected()){
				char tmp[20];
				strcpy(tmp, "/o/e/");	//out,empty
				itoa(i-6,tmp+strlen(tmp),10);
				strcpy(tmp+strlen(tmp), "\r\n");
				uart_puts(tmp);
			}
			
			/* Datenblock in EEPROM schreiben */
			//eeprom_write_block (mat_counter, MAT_COUNTER_ADDRESS, sizeof(mat_counter));
			
		}
		
	}
	
	
}

void mat_set(uint8_t slot, uint8_t val){
	mat_counter[slot] = val;
}

uint16_t* mat_getOfflineValues(){
	return mat_offline_counter;
}

void mat_debug(){
	
	char *str = (char*)seg_getstring();
	
	//mat_read();
	if (!isConnected()){
		strcpy(str, " no connection");
	}
	else{
		strcpy(str, " ");
		strcpy(str+1, con_getText());
		if(strlen(str+1) == 0)
			strcpy(str+1, " hier hackerbrause");
	}		
			//itoa(MAT_1_PIN,seg_getstring(),10);
			
	for(uint8_t i=0; i<6;i++){
		strcpy(str+strlen(str)," ");
		itoa(i+1,str+strlen(str),10);
		str[strlen(str)+1] = '\0';
		str[strlen(str)] = '-';
		itoa(mat_counter[i],str+strlen(str),10);
	}
	
	
		//display wenn verkauf stattfindet
	for(uint8_t i=0; i<6;i++){
		
		if(mat_status[i]){
			itoa(i+1,str,10);
			str[1] = '-';
			itoa(mat_counter[i],str+2,10); break;
		}
		
	}
	
	
	
}