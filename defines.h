#ifndef DEFINES_H_
#define DEFINES_H_


#ifdef __cplusplus
extern "C" {
#endif

/**
*******Platform specific header with definitions
**/

//#include <string>
#include <cstdlib> //size_t


typedef unsigned char uint8_t;
typedef unsigned int uint32_t;

#pragma pack(push, 1)
struct pumpstatus_s {
	uint8_t id = 0;
	uint32_t state = 0;
	bool forced = false;
	bool cmd_consumed = false;
};

struct tankstatus_s {
	uint8_t id;
	uint32_t state;
};

struct plant_s{
	//std::string name;
	uint32_t id;
	float health;
};

struct sectorstatus_s {
	uint8_t id;
	uint32_t state;
	//std::string plants;
};
#pragma pack(pop)



#ifdef __cplusplus
}
#endif

#endif
