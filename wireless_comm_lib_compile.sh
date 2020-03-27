g++ -DRPI -I/usr/include/python2.7 -I/usr/include -fPIC -c python_wrappers.cpp WirelessComm/nrf24l01.cpp WirelessComm/communication_base.cpp
g++ -DRPI -shared -Wl,--export-dynamic nrf24l01.o python_wrappers.o communication_base.o -L/usr/lib -lboost_python -lwiringPi -L/usr/lib/python2.7/config-arm-linux-gnueabihf -lpython2.7 -o wireless_comm_lib.so
