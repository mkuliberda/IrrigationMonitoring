import nrf24l01_drv as nrf_radio
import time
import Scheduler


RADIO1_CE_PIN = 26   # BCM pins numbering
RADIO1_IRQ_PIN = 13  # BCM pins numbering 
RADIO1_SPIDEV = 0
RADIO1_SPICS = 0
RADIO1_PAYLOAD_SIZE = 32
RADIO1_CHANNEL = 15
RADIO1_MY_ADDRESS = [231, 231, 231, 231, 231]  # 0xe7 is 231
RADIO1_TX_ADDRESS = [126, 126, 126, 126, 126]  # 0x7e is 126

PLANTS_SCHEDULES = ["plants_group1_schedule.xml", "plants_group2_schedule.xml", "plants_group3_schedule.xml"]


plants_schedule = Scheduler.Scheduler(PLANTS_SCHEDULES)
print(plants_schedule.is_active_by_tag("Pelargonia"))
print(plants_schedule.is_active_by_tag("Surfinia"))
print(plants_schedule.is_active_all())
print(plants_schedule.print_full_schedule())



radio1 = nrf_radio.NRF24L01()
radio1.init(RADIO1_SPIDEV, RADIO1_SPICS, RADIO1_CE_PIN, RADIO1_IRQ_PIN)
config = radio1.config(RADIO1_PAYLOAD_SIZE, RADIO1_CHANNEL, nrf_radio.NRF24L01_OutputPower.NRF24L01_OutputPower_0dBm, nrf_radio.NRF24L01_DataRate.NRF24L01_DataRate_2M)
radio1.set_my_address(RADIO1_MY_ADDRESS)
radio1.set_tx_address(RADIO1_TX_ADDRESS)

tx_payload = [218] * RADIO1_PAYLOAD_SIZE
radio1.transmit_payload(tx_payload)
time.sleep(0.2)
print(nrf_radio.NRF24L01_TransmitStatus.NRF24L01_Transmit_Status_Sending, radio1.get_transmission_status())
radio1.power_up_rx()

print(radio1.get_status())
print("done, exiting...")

