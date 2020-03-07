#include <boost/python.hpp>
#include <boost/python/enum.hpp>
#include <boost/python/def.hpp>
#include <boost/python/module.hpp>
#include "nrf24l01.h"
  
using namespace boost::python;

object ConfigPy(NRF24L01 & _nrf_obj, const uint8_t & _payloadsize, const uint8_t & _channel, const NRF24L01_OutputPower_t & _outpwr, const NRF24L01_DataRate_t & _datarate){
    return object(_nrf_obj.Config(_payloadsize, _channel, _outpwr, _datarate));
}

BOOST_PYTHON_MODULE(nrf24l01_drv)
{
       
        class_<NRF24L01>("NRF24L01")
              .def("Init", &NRF24L01::Init)
              .def("Config", ConfigPy)                                       //TODO: check if this wrapper works
              .def("SetMyAddress", &NRF24L01::SetMyAddress)
              .def("SetTxAddress", &NRF24L01::SetTxAddress)
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

        enum_<NRF24L01_Transmit_Status_t>("NRF24L01_TransmitStatus")
        .value("NRF24L01_Transmit_Status_Lost", NRF24L01_Transmit_Status_Lost)
        .value("NRF24L01_Transmit_Status_Ok", NRF24L01_Transmit_Status_Ok)
        .value("NRF24L01_Transmit_Status_Sending", NRF24L01_Transmit_Status_Sending)
        .export_values()
        ;

       enum_<NRF24L01_DataRate_t>("NRF24L01_DataRate")
        .value("NRF24L01_DataRate_2M", NRF24L01_DataRate_2M)
        .value("NRF24L01_DataRate_1M", NRF24L01_DataRate_1M)
        .value("NRF24L01_DataRate_250k", NRF24L01_DataRate_250k)
        .export_values()
        ;

       enum_<NRF24L01_OutputPower_t>("NRF24L01_OutputPower")
        .value("NRF24L01_OutputPower_M18dBm", NRF24L01_OutputPower_M18dBm)
        .value("NRF24L01_OutputPower_M12dBm", NRF24L01_OutputPower_M12dBm)
        .value("NRF24L01_OutputPower_M6dBm", NRF24L01_OutputPower_M6dBm)
        .value("NRF24L01_OutputPower_0dBm", NRF24L01_OutputPower_0dBm)
        .export_values()
        ;

       
}
