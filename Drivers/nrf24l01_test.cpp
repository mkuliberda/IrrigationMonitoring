char const* greet()
{
       return "hello, world";
}


#include <boost/python.hpp>
  
BOOST_PYTHON_MODULE(nrf24l01_ext)
{
       using namespace boost::python;
          def("greet", greet);
}

