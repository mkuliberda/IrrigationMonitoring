g++ -I/usr/include/python2.7 -I/usr/include -fPIC -c nrf24l01_python_wrapper.cpp nrf24l01.cpp communication_base.cpp
g++ -shared -Wl,--export-dynamic nrf24l01.o nrf24l01_python_wrapper.o communication_base.o -L/usr/lib -lboost_python -L/usr/lib/python2.7/config-arm-linux-gnueabihf -lpython2.7 -o nrf24l01_drv.so
mv nrf24l01_drv.so ../nrf24l01_drv.so
