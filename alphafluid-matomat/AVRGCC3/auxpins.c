/*
 * auxpins.c
 *
 * Created: 17.03.2012 21:50:56
 *  Author: armageddon
 */ 



void aux_init(){
	
	AUX_DDR &= !(1<<AUX_DOOR);
	AUX_PORT |= (1<<AUX_DOOR);
	
	
	
}


uint8_t aux_door(){
	
	return (AUX_PIN | (1<<AUX_DOOR))>0;
	
}