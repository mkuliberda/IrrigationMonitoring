#include <boost/python.hpp>
#include <boost/python/enum.hpp>
#include <boost/python/def.hpp>
#include <boost/python/module.hpp>
#include "nrf24l01.h"
  
using namespace boost::python;

BOOST_PYTHON_MODULE(nrf24l01_drv)
{
       
        class_<NRF24L01>("nrf24l01_drv")
              .def("Init", &NRF24L01::Init)
              //.def("Config", &NRF24L01::Config)                                       //Compilation error bool as return type
              //.def("SetMyAddress", &NRF24L01::SetMyAddress)                           //Compilation error bool as return type
              //.def("SetTxAddress", &NRF24L01::SetTxAddress)                           //Compilation error bool as return type
              .def("DataReady", &NRF24L01::DataReady)
              .def("GetPayload", &NRF24L01::GetPayload)                               
              .def("TransmitPayload", &NRF24L01::TransmitPayload)                     
              .def("GetRetransmissionsCount", &NRF24L01::GetRetransmissionsCount)
              .def("GetTransmissionStatus", &NRF24L01::GetTransmissionStatus)
              .def("PowerUpTx", &NRF24L01::PowerUpTx)
              .def("PowerUpRx", &NRF24L01::PowerUpRx)
              .def("GetStatus", &NRF24L01::GetStatus)
              .def("PowerDown", &NRF24L01::PowerDown)
              ;

        enum_<NRF24L01_Transmit_Status_t>("transmit_status")
        .value("NRF24L01_Transmit_Status_Lost", NRF24L01_Transmit_Status_Lost)
        .value("NRF24L01_Transmit_Status_Ok", NRF24L01_Transmit_Status_Ok)
        .value("NRF24L01_Transmit_Status_Sending", NRF24L01_Transmit_Status_Sending)
        .export_values()
        ;

       enum_<NRF24L01_DataRate_t>("datarate")
        .value("NRF24L01_DataRate_2M", NRF24L01_DataRate_2M)
        .value("NRF24L01_DataRate_1M", NRF24L01_DataRate_1M)
        .value("NRF24L01_DataRate_250k", NRF24L01_DataRate_250k)
        .export_values()
        ;

       enum_<NRF24L01_OutputPower_t>("output_power")
        .value("NRF24L01_OutputPower_M18dBm", NRF24L01_OutputPower_M18dBm)
        .value("NRF24L01_OutputPower_M12dBm", NRF24L01_OutputPower_M12dBm)
        .value("NRF24L01_OutputPower_M6dBm", NRF24L01_OutputPower_M6dBm)
        .value("NRF24L01_OutputPower_0dBm", NRF24L01_OutputPower_0dBm)
        .export_values()
        ;

       
}
