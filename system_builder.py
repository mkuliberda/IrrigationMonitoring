import sys
from abc import ABCMeta, abstractmethod, abstractproperty


class Abstract:
    '''
    In Python 2.7 ABC class is not available 
    so we need to create new Abstract class from ABCMeta(py 2.7)
    '''
    __metaclass__ = ABCMeta

class Builder(Abstract):
    """
    The Builder interface specifies methods for creating the different parts of
    the Product objects.
    """

    @abstractproperty
    def product(self):
        pass

    @abstractmethod
    def produce_sector(self):
        pass

    @abstractmethod
    def produce_watertank(self):
        pass

    @abstractmethod
    def produce_plant(self):
        pass
    
    @abstractmethod
    def produce_battery(self):
        pass

class IrrigationSystemBuilder(Builder):
    """
    The Concrete Builder classes follow the Builder interface and provide
    specific implementations of the building steps. Your program may have
    several variations of Builders, implemented differently.
    """

    def __init__(self):
        """
        A fresh builder instance should contain a blank product object, which is
        used in further assembly.
        """
        self.reset()

    def reset(self):
        self._product = IrrigationSystem1()

    @property
    def product(self):
        """
        Concrete Builders are supposed to provide their own methods for
        retrieving results. That's because various types of builders may create
        entirely different products that don't follow the same interface.
        Therefore, such methods cannot be declared in the base Builder interface
        (at least in a statically typed programming language).

        Usually, after returning the end result to the client, a builder
        instance is expected to be ready to start producing another product.
        That's why it's a usual practice to call the reset method at the end of
        the `getProduct` method body. However, this behavior is not mandatory,
        and you can make your builders wait for an explicit reset call from the
        client code before disposing of the previous result.
        """
        product = self._product
        self.reset()
        return product

    def produce_sector(self):
        self._product.add("Sector")

    def produce_watertank(self):
        self._product.add("Watertank")

    def produce_plant(self):
        self._product.add("Plant")

    def produce_battery(self):
        self._product.add("Battery")

class IrrigationSystem1():
    """
    It makes sense to use the Builder pattern only when your products are quite
    complex and require extensive configuration.

    Unlike in other creational patterns, different concrete builders can produce
    unrelated products. In other words, results of various builders may not
    always follow the same interface.
    """

    def __init__(self):
        self.parts = []

    def add(self, part):
        self.parts.append(part)

    def list_parts(self):
        print("Product parts: " + ', '.join(self.parts))

class Director:
    """
    The Director is only responsible for executing the building steps in a
    particular sequence. It is helpful when producing products according to a
    specific order or configuration. Strictly speaking, the Director class is
    optional, since the client can control builders directly.
    """

    def __init__(self) :
        self._builder = None

    @property
    def builder(self):
        return self._builder

    @builder.setter
    def builder(self, builder):
        """
        The Director works with any builder instance that the client code passes
        to it. This way, the client code may alter the final type of the newly
        assembled product.
        """
        self._builder = builder

    """
    The Director can construct several product variations using the same
    building steps.
    """

    def build_basic_irrigation_system(self):
        self.builder.produce_watertank()
        self.builder.produce_sector()
        self.builder.produce_battery()

    def build_full_irrigation_system(self):
        self.builder.produce_watertank()
        self.builder.produce_sector()
        self.builder.produce_battery()
        self.builder.produce_plant()

if __name__ == "__main__":

    print(sys.version)
    
    """
    The client code creates a builder object, passes it to the director and then
    initiates the construction process. The end result is retrieved from the
    builder object.
    """

    director = Director()
    builder = IrrigationSystemBuilder()
    director.builder = builder

    print("Standard basic product: ")
    director.build_basic_irrigation_system()
    builder.product.list_parts()

    print("Standard full featured product: ")
    director.build_full_irrigation_system()
    builder.product.list_parts()
