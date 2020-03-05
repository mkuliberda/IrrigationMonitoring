#import nrf24l01_drv
import nrf24l01_test

radio = nrf24l01_test.nrf24l01()

radio.no_greet()
print(radio.greet())

