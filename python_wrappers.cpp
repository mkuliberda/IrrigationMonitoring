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


object setBufferPy(IrrigationMessage & _irm_obj, list _buf, uint8_t _size){
    uint8_t buffer[32];

    for (uint8_t i = 0; i < _size; ++i){
        buffer[i] = extract<uint8_t>(_buf[i]);
    }

    return object(_irm_obj.setBuffer(buffer, _size));    
}

list getBufferPy(IrrigationMessage & _irm_obj){
    list buffer;
    std::array<uint8_t, PAYLOAD_SIZE> arr = _irm_obj.getBuffer();

    for (auto &byte : arr){
        buffer.append(byte);
    }

    return buffer;   
}

dict decodeConfirmationPy(IrrigationMessage & _irm_obj){

    struct confirmation_s confirmation = _irm_obj.decodeConfirmation();

    dict confirmation_dict;
    confirmation_dict["target"] = static_cast<uint8_t>(confirmation.target);
    confirmation_dict["target_id"] = static_cast<uint8_t>(confirmation.target_id);
    confirmation_dict["cmd"] = static_cast<uint8_t>(confirmation.cmd);
    confirmation_dict["subcmd1"] = static_cast<uint8_t>(confirmation.subcmd1);
    confirmation_dict["subcmd2"] = static_cast<uint8_t>(confirmation.subcmd2);
    confirmation_dict["consumed"] = object(confirmation.consumed ? true : false);

    return confirmation_dict;
}

dict decodeSectorPy(IrrigationMessage & _irm_obj){

    struct sectorstatus_s sector = _irm_obj.decodeSector();

    dict sector_dict;
    sector_dict["object"] = target_t::Sector;
	sector_dict["id"] = sector.id;
	sector_dict["plants"] = sector.plants;
	sector_dict["state"] = sector.state;

    return sector_dict;
}

dict decodePumpPy(IrrigationMessage & _irm_obj){

    struct pumpstatus_s pump = _irm_obj.decodePump();

    dict pump_dict;
    pump_dict["object"] = target_t::Pump;
	pump_dict["id"] = pump.id;
	pump_dict["state"] = pump.state;                //TODO: decode zipped state
	pump_dict["forced"] = pump.forced;
	pump_dict["cmd_consumed"] = pump.cmd_consumed;

    return pump_dict;
}

dict decodePlantPy(IrrigationMessage & _irm_obj){

    struct plant_s plant = _irm_obj.decodePlant();
    std::string name(plant.name);

    dict plant_dict;
    plant_dict["object"] = target_t::Plant;
	plant_dict["id"] = plant.id;
	plant_dict["name"] = name;
	plant_dict["health"] = plant.health;

    return plant_dict;
}

dict decodeTankPy(IrrigationMessage & _irm_obj){

    struct tankstatus_s tank = _irm_obj.decodeTank();

    dict tank_dict;
    tank_dict["object"] = target_t::Tank;
	tank_dict["id"] = tank.id;
	tank_dict["state"] = tank.state; //TODO: decode state

    	/******************************errcodeBitmask****************************************
	 * *Upper 16 bits										Lower 16 bits
	 * 00000000 00000000 									00000000 00000000
	 * |||||||| ||||||||->water temperature too low	 (16)	|||||||| ||||||||->(0)
	 * |||||||| |||||||-->water temperature too high (17)	|||||||| |||||||-->(1)
	 * |||||||| ||||||--->water level too low		 (18)	|||||||| ||||||--->(2)
	 * |||||||| |||||---->							 (19)	|||||||| |||||---->(3)
	 * |||||||| ||||----->temperature sensor1 invalid(20)	|||||||| ||||----->(4)
	 * |||||||| |||------>temperature sensor2 invalid(21)	|||||||| |||------>(5)
	 * |||||||| ||------->wl sensor1 invalid         (22)	|||||||| ||------->(6)
	 * |||||||| |-------->wl sensor2 invalid         (23)	|||||||| |-------->(7)
	 * ||||||||---------->wl sensor3 invalid         (24)	||||||||---------->(8)
	 * |||||||----------->wl sensor4 invalid         (25)	|||||||----------->(9)
	 * ||||||------------>wl sensor5 invalid         (26)	||||||------------>(10)
	 * |||||------------->wl sensor6 invalid         (27)	|||||------------->(11)
	 * ||||-------------->wl sensor7 invalid         (28)	||||-------------->(12)
	 * |||--------------->wl sensor8 invalid         (29)	|||--------------->(13)
	 * ||---------------->wl sensor9 invalid         (30)	||---------------->(14)
	 * |----------------->wl sensor10 invalid        (31)	|----------------->(15)
	 */

    return tank_dict;
}

dict decodeMsgPy(IrrigationMessage & _irm_obj){

    dict empty;
    std::array<uint8_t, PAYLOAD_SIZE> buffer = _irm_obj.getBuffer();

    switch (static_cast<target_t>(buffer[1])){

        case target_t::Sector:
        return decodeSectorPy(_irm_obj);
        break;


        case target_t::Pump:
        return decodePumpPy(_irm_obj);
        break;

        case target_t::Tank:
        return decodeTankPy(_irm_obj);
        break;

        case target_t::Plant:
        return decodePlantPy(_irm_obj);
        break;

        default:
        return empty;
        break;

    }
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
              .def("decode_confirmation", decodeConfirmationPy)
              .def("decode_message", decodeMsgPy)            
              .def("encode_cmd", encodeCmdPy)
              .def("set_buffer", setBufferPy)
              .def("get_buffer", getBufferPy)
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

        enum_<target_t>("target_t")
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

       enum_<direction_t>("direction_t")
        .value("from_rpi_to_irm", RPiToIRM)
        .value("from_irm_to_rpi", IRMToRPi)
        .export_values()
        ;

       enum_<command_t>("command_t")
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
