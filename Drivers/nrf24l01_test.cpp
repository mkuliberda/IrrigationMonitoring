

class nrf24l01{
public:
       char const* greet(){ return "hello, world";}
};


#include <boost/python.hpp>
  
BOOST_PYTHON_MODULE(nrf24l01_ext)
{
       using namespace boost::python;
       class_<nrf24l01>("nrf24l01")
              .def("greet", &nrf24l01::greet);
}

