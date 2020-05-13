import sys
#from abc import ABCMeta, abstractmethod, abstractproperty

class Watertank():
    def __init__(self, id):
        self.__name__ = "Watertank"
        self.__id = id
        self.__water_lvl = "unknown"
        self.__water_temp = "unknown"

    def get_id(self):
        return self.__id

    def is_valid(self, water_lvl, water_temp="ok"):
        self.__water_lvl = water_lvl
        self.__water_temp = water_temp
        if self.__water_lvl == "ok" and self.__water_temp == "ok":
            return True
        else:
            return False

class Sector():
    def __init__(self, id):
        self.__name__ = "Sector"
        self.__id = id
        self.__watering_active = False
        self.__plants = ""
        self.__errors = ""

    def get_id(self):
        return self.__id

    def is_watering(self):
        return self.__watering_active

    def list_plants(self):
        return self.__plants[:-1].split(",")

    def list_errors(self):
        return self.__errors[:-1].split(",")

    def update(self, watering_active, plants, errors):
        self.__watering_active = watering_active
        self.__plants = plants
        self.__errors = errors

class Plant():
    def __init__(self, id):
        self.__name__ = "Plant"
        self.__id = id
        self.__name = "noname"
        self.__health = 0

    def get_id(self):
        return self.__id

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def update(self, health, name=None):
        if name is not None:
            self.__name = name
        self.__health = health
    
    def get_health(self):
        return self.__health

class Battery():
    def __init__(self, id):
        self.__name__ = "Battery"
        self.__id = id
        self.__percentage = 0
        self.__time_remaining_min = 0
        self.__state = "undetermined"
        self.__errors = ""

    def get_id(self):
        return self.__id

    def update(self, percentage=None, time_remaining_min=None, state=None, errors=None):
        if percentage is not None:
            self.__percentage = percentage
        if time_remaining_min is not None:
            self.__time_remaining_min = time_remaining_min
        if state is not None:
            self.__state = state
        if errors is not None:
            self.__errors = errors
    
    def get_percentage(self):
        return self.__percentage

    def get_time_remaining_min(self):
        return self.__time_remaining_min

    def get_state(self):
        return self.__state
    
    def list_errors(self):
        return self.__errors[:-1].split(",")


#class Abstract:
    '''
    In Python 2.7 ABC class is not available 
    so we need to create new Abstract class from ABCMeta(py 2.7)
    '''
#    __metaclass__ = ABCMeta

class Builder:

    def produce_sector(self):
        pass

    def produce_watertank(self):
        pass

    #def produce_plant(self):
    #    pass
    
    #def produce_battery(self):
    #    pass

class IrrigationSystemBuilder(Builder):

    __s_i = 0
    __w_i = 0

    def produce_sector(self):
        sector = Sector(self.__s_i)
        self.__s_i += 1
        return sector

    def produce_watertank(self):
        watertank = Watertank(self.__w_i)
        self.__w_i += 1
        return watertank

    #def produce_plant(self):
    #    self._product.add(plant)

    #def produce_battery(self):
    #    self._product.add(battery)

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

    def add(self, entity):
        if entity.__name__ == "Sector":
            self.__sectors.append(entity)

        if entity.__name__ == "Watertank":
            self.__watertanks.append(entity)

        if entity.__name__ == "Battery":
            self.__batteries.append(entity)

        if entity.__name__ == "Plant":
            self.__plants.append(entity)

    def get_sector_plants(self, id):
        return self.__sectors[id].list_plants()

    def list_entities(self):
        print("System consists of:\n" + str(len(self.__watertanks)) + " watertanks\n" +\
         str(len(self.__sectors)) + " sectors\n" +\
         str(len(self.__plants)) + " plants\n" +\
         str(len(self.__batteries)) + " batteries")


class Director:
    __builder = None
  
    def setBuilder(self, builder):
        self.__builder = builder

    def build_basic_irrigation_system(self):
        basic_system = IrrigationSystem()
        sector = self.__builder.produce_sector()
        basic_system.add(sector)
        sector = self.__builder.produce_sector()
        basic_system.add(sector)

        return basic_system

    def build_full_irrigation_system(self):
        pass
        #self.builder.produce_watertank()
        #self.builder.produce_sector()
        #self.builder.produce_battery()
        #self.builder.produce_plant()

if __name__ == "__main__":

    print(sys.version)
    
    """
    The client code creates a builder object, passes it to the director and then
    initiates the construction process. The end result is retrieved from the
    builder object.
    """

    director = Director()
    system_builder = IrrigationSystemBuilder()
    director.setBuilder(system_builder)

    print("Standard basic product: ")
    system1 = director.build_basic_irrigation_system()
    system1.list_entities()
    print(system1.get_sector_plants(1))

    #print("Standard full featured product: ")
    #director.build_full_irrigation_system()
    #builder.product.list_parts()
