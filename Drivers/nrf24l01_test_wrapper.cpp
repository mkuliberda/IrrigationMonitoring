#include <boost/python.hpp>
#include "nrf24l01_test.h"
  
BOOST_PYTHON_MODULE(nrf24l01_ext)
{
       using namespace boost::python;
       class_<nrf24l01>("nrf24l01")
              .def("greet", &nrf24l01::greet);
}