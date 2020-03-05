#g++ -O3 nrf24l01_test.cpp -shared -I/usr/include/python3.5m/ -lpython3.5m -lboost_python -o nrf24l01_test.so
g++ -I/usr/include/python2.7 -I/usr/include -fPIC -c nrf24l01_test_wrapper.cpp nrf24l01_test.cpp
g++ -shared -Wl,--export-dynamic nrf24l01_test.o nrf24l01_test_wrapper.o -L/usr/lib -lboost_python -L/usr/lib/python2.7/config-arm-linux-gnueabihf -lpython2.7 -o nrf24l01_test.so
mv nrf24l01_test.so ../nrf24l01_test.so
