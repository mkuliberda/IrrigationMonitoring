import sys
from typing import TypeVar, List, Union
import wireless_comm_lib as wireless

WirelessTarget = TypeVar(wireless.target_t)

class Watertank():
    def __init__(self, id: int):
        self.__type = wireless.target_t.Tank
        self.__id = id
        self.__water_lvl = "unknown"
        self.__water_temp = "unknown"

    def get_id(self) -> int:
        return self.__id

    def get_type(self) -> WirelessTarget:
        return self.__type

    def update(self, water_lvl: str, water_temp: str="ok") -> None:
        self.__water_lvl = water_lvl
        self.__water_temp = water_temp

    def is_valid(self) -> bool:
        if self.__water_lvl == "ok" and self.__water_temp == "ok":
            return True
        else:
            return False

class Sector():
    def __init__(self, id: int):
        self.__type = wireless.target_t.Sector
        self.__id = id
        self.__watering_active = False
        self.__plants = ""
        self.__errors = ""

    def get_id(self) -> int:
        return self.__id

    def get_type(self) -> WirelessTarget:
        return self.__type

    def is_watering(self) -> bool:
        return self.__watering_active

    def list_plants(self) -> List[str]:
        return self.__plants[:-1].split(",")

    def list_errors(self) -> List[str]:
        return self.__errors[:-1].split(",")

    def update(self, watering_active: bool, plants: str, errors: str) -> None:
        self.__watering_active = watering_active
        self.__plants = plants
        self.__errors = errors

class Plant():
    def __init__(self, id: int):
        self.__type = wireless.target_t.Plant
        self.__id = id
        self.__name = "noname"
        self.__health = 0

    def get_id(self) -> int:
        return self.__id

    def get_type(self) -> WirelessTarget:
        return self.__type

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def update(self, health: float, name: str=None) -> None:
        if name is not None:
            self.__name = name
        self.__health = health
    
    def get_health(self) -> float:
        return self.__health

class Battery():
    def __init__(self, id: int):
        self.__type = wireless.target_t.Power
        self.__id = id
        self.__percentage = 0
        self.__time_remaining_min = 0
        self.__state = "undetermined"
        self.__errors = ""

    def get_id(self) -> int:
        return self.__id

    def get_type(self) -> WirelessTarget:
        return self.__type

    def update(self, percentage: int=None, time_remaining_min: int=None, state: str=None, errors: str=None) -> None:
        if percentage is not None:
            self.__percentage = percentage
        if time_remaining_min is not None:
            self.__time_remaining_min = time_remaining_min
        if state is not None:
            self.__state = state
        if errors is not None:
            self.__errors = errors
    
    def get_percentage(self) -> int:
        return self.__percentage

    def get_time_remaining_min(self) -> int:
        return self.__time_remaining_min

    def get_state(self) -> str:
        return self.__state
    
    def list_errors(self) -> List[str]:
        return self.__errors[:-1].split(",")


SectorType = TypeVar(Sector)
WatertankType = TypeVar(Watertank)
PlantType = TypeVar(Plant)
BatteryType = TypeVar(Battery)


class Builder:

    def produce_sector(self) -> None:
        pass

    def produce_watertank(self) -> None:
        pass

    def produce_plant(self) -> None:
        pass
    
    def produce_battery(self) -> None:
        pass


BuilderType = TypeVar(Builder)


class IrrigationSystemBuilder(Builder):

    __s_i = 0
    __w_i = 0
    __p_i = 0
    __b_i = 0

    def produce_sector(self) -> SectorType:
        sector = Sector(self.__s_i)
        self.__s_i += 1
        return sector

    def produce_watertank(self) -> WatertankType:
        watertank = Watertank(self.__w_i)
        self.__w_i += 1
        return watertank

    def produce_plant(self) -> PlantType:
        plant = Plant(self.__p_i)
        self.__p_i += 1
        return plant

    def produce_battery(self) -> BatteryType:
        battery = Battery(self.__b_i)
        self.__b_i += 1
        return battery


class IrrigationSystem():
    """
    It makes sense to use the Builder pattern only when your products are quite
    complex and require extensive configuration.

    Unlike in other creational patterns, different concrete builders can produce
    unrelated products. In other words, results of various builders may not
    always follow the same interface.
    """

    def __init__(self):
        self.__watertanks = []
        self.__sectors = []
        self.__plants = []
        self.__batteries = []

    def add(self, entity: Union[SectorType, WatertankType, BatteryType, PlantType]) -> None:
        if entity.get_type() == wireless.target_t.Sector:
            self.__sectors.append(entity)
        if entity.get_type() == wireless.target_t.Tank:
            self.__watertanks.append(entity)
        if entity.get_type() == wireless.target_t.Power:
            self.__batteries.append(entity)
        if entity.get_type() == wireless.target_t.Plant:
            self.__plants.append(entity)

    def list_sectors(self) -> list:
        return self.__sectors

    def list_watertanks(self) -> list:
        return self.__watertanks

    def list_plants(self) -> list:
        return self.__plants

    def list_batteries(self) -> list:
        return self.__batteries
    
    def update_sector(self, sector_id: int, watering_active: bool, plants: str, errors: str) -> bool:
        if sector_id >= 0 and sector_id < len(self.__sectors):
            self.__sectors[sector_id].update(watering_active, plants, errors)
            return True
        else:
            return False

    def update_watertank(self, tank_id: int, water_level: str, water_temp: str="unknown") -> bool:
        if tank_id >= 0 and tank_id < len(self.__watertanks):
            if water_temp == "unknown":
                self.__watertanks[tank_id].update(water_level)
            else:
                self.__watertanks[tank_id].update(water_level, water_temp)
            return True
        else:
            return False
    
    def update_plant(self, plant_id: int, health: float, name: str="unknown") -> bool:
        if plant_id >= 0 and plant_id < len(self.__plants):
            if name == "unknown":
                self.__plants[plant_id].update(health)
            else:
                self.__plants[plant_id].update(health, name)
            return True
        else:
            return False
    
    def update_battery(self, battery_id: int, percentage: int=None, time_remaining_min: int=None, state: str=None, errors: str=None) -> bool:
        if battery_id >= 0 and battery_id < len(self.__batteries):
            self.__batteries[battery_id].update(percentage, time_remaining_min, state, errors)
            return True
        else:
            return False

    def list_plants_by_sector(self, sector_id: int) -> List[str]:
        return self.__sectors[sector_id].list_plants()
        
    def is_watertank_valid(self, tank_id: int) -> bool:
        if tank_id >= 0 and tank_id < len(self.__watertanks):
            return self.__watertanks[tank_id].is_valid()

    def print_entities(self) -> None:
        print("System consists of:\n" + \
          "watertanks: " + str(len(self.__watertanks)) + "\n" +\
          "sectors: " + str(len(self.__sectors)) + "\n" +\
          "plants: " + str(len(self.__plants)) + "\n" +\
          "batteries: " + str(len(self.__batteries)))

    def list_all_entities(self) -> list:
        alist = []
        for sector in self.__sectors:
            alist.append(sector)
        for plant in self.__plants:
            alist.append(plant)
        for watertank in self.__watertanks:
            alist.append(watertank)
        for battery in self.__batteries:
            alist.append(battery)
        return alist


IrrigationSystemType = TypeVar(IrrigationSystem)


class Director():
    __builder = None
  
    def setBuilder(self, builder: BuilderType) -> None:
        self.__builder = builder

    def build_basic_irrigation_system(self) -> IrrigationSystemType:

        basic_system = IrrigationSystem()
        basic_system.add(self.__builder.produce_watertank())
        basic_system.add(self.__builder.produce_battery())
        basic_system.add(self.__builder.produce_sector())

        return basic_system

    def build_full_irrigation_system(self) -> IrrigationSystemType:

        full_system = IrrigationSystem()
        full_system.add(self.__builder.produce_watertank())
        full_system.add(self.__builder.produce_battery())
        for i in range(4):
            full_system.add(self.__builder.produce_sector())
        for i in range(8):
            full_system.add(self.__builder.produce_plant())
        
        return full_system

    def build_custom_irrigation_system(self) -> IrrigationSystemType:

        custom_system = IrrigationSystem()
        custom_system.add(self.__builder.produce_watertank())
        custom_system.add(self.__builder.produce_battery())
        for i in range(3):
            custom_system.add(self.__builder.produce_sector())
        for i in range(7):
            custom_system.add(self.__builder.produce_plant())
        
        return custom_system


if __name__ == "__main__":

    print(sys.version)
    
    """
    The client code creates a builder object, passes it to the director and then
    initiates the construction process. The end result is retrieved from the
    builder object.
    Example below
    """

    director = Director()
    system_builder = IrrigationSystemBuilder()
    director.setBuilder(system_builder)

    print("Custom system: ")
    system1 = director.build_custom_irrigation_system()
    system1.print_entities()
    print(system1.get_sector_plants(0))
    entity_list = system1.list_entities()
    for entity in entity_list:
        if entity.get_type() == wireless.target_t.Sector:
            print("Sector found")

