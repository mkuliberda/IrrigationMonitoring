/**
 * @brief  Project specific communication protocol defines and enums
 */

/**
 * @brief  Targets
 */
typedef enum _Target_t {
	Generic 	= 0x00,
	Pump 		= 0x01,   
	Tank 		= 0x02,     
	Plant 		= 0x03,
	Power		= 0x0D,
	System		= 0x0E,
	All			= 0xFF
} Target_t;

/**
 * @brief  Directions
 */
typedef enum _Direction_t {
	RPiToIRM 	= 0xAA,
	IRMToRPi 	= 0xBB
} Direction_t;

/**
 * @brief  Commands, 0x1X - Pump, 0x2X - Tank, 0x3X - Plant, 0xDX - Power Supply, 0xEX - System 
 */
typedef enum _Command_t {
	None			= 0x00,
	Start 			= 0x10,
	Stop 			= 0x11,
	ForceStart		= 0x12,
	ForceStop		= 0x13,
	StartRev		= 0x14,
	ForceStartRev	= 0x15,
	GetLiquidLevel	= 0x20,
	GetTemperature	= 0x21,
	GetMoisture		= 0x30,
	GetVoltage		= 0xD0,
	GetCurrent		= 0xD1,
	GetChargeLevel	= 0xD2,
	GetCycles		= 0xD3,
	GetDescription	= 0xFB,
	SetSleep		= 0xFC,
	SetStandby		= 0xFD,
	GetState		= 0xFE,
	GetStatus		= 0xFF
} Command_t;