/*
 * CProgram1.c
 *
 * Created: 06.03.2012 20:38:20
 *  Author: armageddon
 */ 

#include "7seg.h"

char *str;
uint8_t strpos;

uint8_t outbuf[4] ={0,0,0,0};
	

uint8_t map[][2] = {	
	{'0', 0b01111011},
	{'1', 0b00001010},
	{'2', 0b01101101},
	{'3', 0b01001111},
	{'4', 0b00011110},
	{'5', 0b01010111},
	{'6', 0b01110111},
	{'7', 0b01001010},
	{'8', 0b01111111},
	{'9', 0b01011111},
		
	{'-', 0b00000100},
	{' ', 0b00000000},
	{'a', 0b01111110},
	{'b', 0b00110111},
	{'c', 0b00100101},
	{'d', 0b00101111},
	{'e', 0b01110101},
	{'f', 0b01110100},
	{'g', 0b01110011},
	{'h', 0b00110110},
	{'i', 0b00100000},
	{'j', 0b00001011},
	{'k', 0b00110100},
	{'l', 0b00110001},
	{'m', 0b01100010},
	{'n', 0b00100110},
	{'o', 0b00100111},
	{'p', 0b01111100},
	{'q', 0b01011110},
	{'r', 0b00100100},
	{'s', 0b01010111},
	{'t', 0b01110000},
	{'u', 0b00111011},
	{'v', 0b00100011},
	{'w', 0b00011001},
	{'x', 0b00111110},
	{'y', 0b00111100},
	{'z', 0b01101101},
	{'@', 0b01111101}		
};

#define SIZEOF(x) (sizeof(x)/sizeof(*x))

void seg_init(){
	
	SEG_DATA_DDR |= (1<<SEG_DATA);
	SEG_SCK_DDR |= (1<<SEG_SCK);
	SEG_STORE_DDR |= (1<<SEG_STORE);
	SEG_EN_DDR |= (1<<SEG_EN);
	
	SEG_EN_PORT &= !(1<<SEG_EN);
	
	str = (char*)malloc(140+4*6+4);
	
	//strcpy(str, " alpha fluid counter -\0");
	str[0] = 'a';
	strpos = 0;
}

void seg_setstring(char *s){
	str = s;
}

char *seg_getstring(){
	return str;
}

void push(uint8_t data){
	
	for(uint8_t j=0; j<8; j++){
		SEG_DATA_PORT &= ~(1<<SEG_DATA);
		SEG_DATA_PORT |= (((~data & (1<<j))>0)<<SEG_DATA);
		_delay_us(20);
		SEG_SCK_PORT |= (1<<SEG_SCK);
		_delay_us(20);
		SEG_SCK_PORT &= ~(1<<SEG_SCK);
		_delay_us(20);
	}
}

void latch(){
	SEG_STORE_PORT |= (1<<SEG_STORE);
	_delay_us(20);
	SEG_STORE_PORT &= ~(1<<SEG_STORE);
}

uint8_t convert (char ch){
	
	for(uint8_t i=0;i<SIZEOF(map);i++){
		if(map[i][0] == tolower(ch)) return map[i][1];
	}
	
	return 0b00000001;
}

void update(){
	
	for(int i=3;i>=0;i--){
		push(outbuf[i]);
	}
	latch();
	
}

void addch(uint8_t ch){
	
	for(uint8_t i=0;i<3;i++){
		outbuf[i] = outbuf[i+1];
	}
	outbuf[3] = ch;
	
}

void test(){
	
	if(strlen(str) <= 4){
		uint8_t blank = 0;
		for (uint8_t i=0; i<4; i++){
			if(!str[i]) blank = 1;
			addch(convert((!blank)?str[i]:' '));
		}
		
	}
	else{
		if(!str[strpos]){
			strpos = 0;
			//addch(convert(' '));
		}
		addch(convert(str[strpos]));
		strpos++;
	}		
	
	update();
	
	
	
	
	
}



void point(){
	
	outbuf[3] |= 0b10000000;
	
	
}