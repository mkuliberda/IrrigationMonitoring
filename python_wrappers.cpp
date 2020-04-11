#include <boost/python.hpp>
#include <boost/python/enum.hpp>
#include <boost/python/def.hpp>
#include <boost/python/module.hpp>
#include "WirelessComm/nrf24l01.h"
#include "WirelessComm/msg_definitions_irrigation.h"
  
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

list encodeCmdPy(IrrigationMessage & _irm_obj, cmd_s _cmd){
    list a;
    std::array<uint8_t, 32> buffer;

    buffer = _irm_obj.encode(_cmd);
    for(auto &byte : buffer){
        a.append(byte);
    }

    return a;
}


void setBufferPy(IrrigationMessage & _irm_obj, list _buf, uint8_t _size){
    uint8_t buffer[32];

    for (uint8_t i = 0; i < _size; ++i){
        buffer[i] = extract<uint8_t>(_buf[i]);
    }

    _irm_obj.setBuffer(buffer, _size);
}



BOOST_PYTHON_MODULE(wireless_comm_lib)
{       
        class_<NRF24L01>("NRF24L01")
              .def("init", &NRF24L01::Init)
              .def("config", ConfigPy)                                       //TODO: check if this wrapper works
              .def("set_my_address", SetMyAddressPy)
              .def("set_tx_address", SetTxAddressPy)
              .def("data_ready", &NRF24L01::DataReady)
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

        class_<IrrigationMessage>("IrrigationMessage", init<direction_t>())
              .def("validate_crc", &IrrigationMessage::validateCRC)
              .def("decode_tank_message", &IrrigationMessage::decodeTank)
              .def("decode_plant_message", &IrrigationMessage::decodePlant)
              .def("decode_pump_message", &IrrigationMessage::decodePump)
              .def("decode_sector_message", &IrrigationMessage::decodeSector)
              .def("decode_confirmation", &IrrigationMessage::decodeConfirmation)              
              .def("encode_cmd", encodeCmdPy)
              .def("set_buffer", setBufferPy)
              ;

        class_<tankstatus_s>("tank_status_s")
              .def_readwrite("id",&tankstatus_s::id)
              .def_readwrite("state",&tankstatus_s::state)
              ; 
        
        class_<pumpstatus_s>("pump_status_s")
              .def_readwrite("id",&pumpstatus_s::id)
              .def_readwrite("state",&pumpstatus_s::state)
              .def_readwrite("forced",&pumpstatus_s::forced)
              .def_readwrite("cmd_consumed",&pumpstatus_s::cmd_consumed)
              ; 

        class_<plant_s>("plant_status_s")
              .def_readwrite("id",&plant_s::id)
              .def_readwrite("health",&plant_s::health)
 //             .def_readwrite("name",&plant_s::name)
              ;  

        class_<sectorstatus_s>("sector_status_s")
              .def_readwrite("id",&sectorstatus_s::id)
              .def_readwrite("state",&sectorstatus_s::state)
              ;    

        class_<cmd_s>("cmd_s")
              .def_readwrite("target",&cmd_s::target)
              .def_readwrite("target_id",&cmd_s::target_id)
              .def_readwrite("cmd", &cmd_s::cmd)
              .def_readwrite("subcmd1", &cmd_s::subcmd1)
              .def_readwrite("subcmd2", &cmd_s::subcmd2)
              ;    

        class_<confirmation_s>("confirmation_s")
              .def_readwrite("target",&confirmation_s::target)
              .def_readwrite("target_id",&confirmation_s::target_id)
              .def_readwrite("cmd", &confirmation_s::cmd)
              .def_readwrite("subcmd1", &confirmation_s::subcmd1)
              .def_readwrite("subcmd2", &confirmation_s::subcmd2)
              .def_readwrite("consumed", &confirmation_s::consumed)
              ;    

        enum_<NRF24L01_Transmit_Status_t>("NRF24L01_TransmitStatus")
        .value("Lost", NRF24L01_Transmit_Status_Lost)
        .value("Ok", NRF24L01_Transmit_Status_Ok)
        .value("Sending", NRF24L01_Transmit_Status_Sending)
        .export_values()
        ;

       enum_<NRF24L01_DataRate_t>("NRF24L01_DataRate")
        .value("_2Mbps", NRF24L01_DataRate_2M)
        .value("_1Mbps", NRF24L01_DataRate_1M)
        .value("_250kbps", NRF24L01_DataRate_250k)
        .export_values()
        ;

       enum_<NRF24L01_OutputPower_t>("NRF24L01_OutputPower")
        .value("M18dBm", NRF24L01_OutputPower_M18dBm)
        .value("M12dBm", NRF24L01_OutputPower_M12dBm)
        .value("M6dBm", NRF24L01_OutputPower_M6dBm)
        .value("P0dBm", NRF24L01_OutputPower_0dBm)
        .export_values()
        ;

        enum_<target_t>("target")
        .value("Generic", Generic)
        .value("Pump", Pump)
        .value("Tank", Tank)
        .value("Plant", Plant)
        .value("Sector", Sector)
        .value("PowerSupply", Power)
        .value("System", System)
        .value("All", All)
        .export_values()
        ;

       enum_<direction_t>("direction")
        .value("from_rpi_to_irm", RPiToIRM)
        .value("from_irm_to_rpi", IRMToRPi)
        .export_values()
        ;

       enum_<command_t>("command")
        .value("None", None)
        .value("Start", Start)
        .value("Stop", Stop)
        .value("ForceStart", ForceStart)
        .value("ForceStop", ForceStop)
        .value("StartRev", StartRev)
        .value("ForceStartRev", ForceStartRev)
        .value("GetLiquidLevel", GetLiquidLevel)
        .value("GetTemperature", GetTemperature)
        .value("GetMoisture", GetMoisture)
        .value("GetVoltage", GetVoltage)
        .value("GetCurrent", GetCurrent)
        .value("GetChargeLevel", GetChargeLevel)
        .value("GetCycles", GetCycles)
        .value("GetDescription", GetDescription)
        .value("SetSleep", SetSleep)
        .value("SetStandby", SetStandby)
        .value("GetState", GetState)
        .value("GetStatus", GetStatus)
        .export_values()
        ; 

}
