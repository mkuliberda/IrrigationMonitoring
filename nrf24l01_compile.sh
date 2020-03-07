g++ -DRPI -I/usr/include/python2.7 -I/usr/include -fPIC -c nrf24l01_python_wrapper.cpp WirelessComm/nrf24l01.cpp WirelessComm/communication_base.cpp
g++ -DRPI -shared -Wl,--export-dynamic nrf24l01.o nrf24l01_python_wrapper.o communication_base.o -L/usr/lib -lboost_python -lwiringPi -L/usr/lib/python2.7/config-arm-linux-gnueabihf -lpython2.7 -o nrf24l01_drv.so
# mv nrf24l01_drv.so ../nrf24l01_drv.so
