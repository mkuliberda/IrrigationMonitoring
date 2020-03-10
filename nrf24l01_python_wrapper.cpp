#include <boost/python.hpp>
#include <boost/python/enum.hpp>
#include <boost/python/def.hpp>
#include <boost/python/module.hpp>
#include "WirelessComm/nrf24l01.h"
  
using namespace boost::python;

object ConfigPy(NRF24L01 & _nrf_obj, const uint8_t & _payloadsize, const uint8_t & _channel, const NRF24L01_OutputPower_t & _outpwr, const NRF24L01_DataRate_t & _datarate){
    return object(_nrf_obj.Config(_payloadsize, _channel, _outpwr, _datarate));
}


list GetPayloadPy(NRF24L01 & _nrf_obj){
    list a;
    uint8_t buffer[32]; //max payload is 32

    _nrf_obj.GetPayload(buffer);
    uint8_t payload_size = _nrf_obj.GetPayloadSize();
    for (uint8_t i = 0; i < payload_size; ++i){
        a.append(buffer[i]);
    }

    return a;
}

void TransmitPayloadPy(NRF24L01 & _nrf_obj, list _payload){
    uint8_t buffer[32]; //max payload is 32

    for (uint8_t i = 0; i < _nrf_obj.GetPayloadSize(); ++i){
        buffer[i] = extract<uint8_t>(_payload[i]);
    }

    _nrf_obj.TransmitPayload(buffer);
}

void SetMyAddressPy(NRF24L01 & _nrf_obj, list _addr){
    uint8_t address[5];

    for (uint8_t i = 0; i < 5; ++i){
        address[i] = extract<uint8_t>(_addr[i]);
    }

    _nrf_obj.SetMyAddress(address);
}

void SetTxAddressPy(NRF24L01 & _nrf_obj, list _addr){
    uint8_t address[5];

    for (uint8_t i = 0; i < 5; ++i){
        address[i] = extract<uint8_t>(_addr[i]);
    }

    _nrf_obj.SetTxAddress(address);
}


BOOST_PYTHON_MODULE(nrf24l01_drv)
{
       
        class_<NRF24L01>("NRF24L01")
              .def("init", &NRF24L01::Init)
              .def("config", ConfigPy)                                       //TODO: check if this wrapper works
              .def("set_my_address", SetMyAddressPy)
              .def("set_tx_address", SetTxAddressPy)
              .def("is_data_ready", &NRF24L01::DataReady)
              .def("get_payload", GetPayloadPy)                               
              .def("transmit_payload", TransmitPayloadPy)                     
              .def("get_retransmissions_count", &NRF24L01::GetRetransmissionsCount)
              .def("get_transmission_status", &NRF24L01::GetTransmissionStatus)
              .def("power_up_tx", &NRF24L01::PowerUpTx)
              .def("power_up_rx", &NRF24L01::PowerUpRx)
              .def("get_status", &NRF24L01::GetStatus)
              .def("power_down", &NRF24L01::PowerDown)
              .def("read_register_test", &NRF24L01::ReadRegisterTest)
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
