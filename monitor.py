import nrf24l01_drv as nrf
#import nrf24l01_test

RADIO1_CE_PIN = 25
RADIO1_IRQ_PIN = 23 
RADIO1_SPIDEV = 0
RADIO1_SPICS = 0
RADIO1_PAYLOAD_SIZE = 32
RADIO1_CHANNEL = 15
RADIO1_MY_ADDRESS = [231, 231, 231, 231, 231]  # 0xe7 is 231
RADIO1_TX_ADDRESS = [126, 126, 126, 126, 126]  # 0x7e is 126



radio1 = nrf.NRF24L01()
radio1.init(RADIO1_SPIDEV, RADIO1_SPICS, RADIO1_CE_PIN, RADIO1_IRQ_PIN)
radio1.config(RADIO1_PAYLOAD_SIZE, RADIO1_CHANNEL, nrf.NRF24L01_OutputPower.NRF24L01_OutputPower_M18dBm, nrf.NRF24L01_DataRate.NRF24L01_DataRate_2M)
radio1.set_my_address(RADIO1_MY_ADDRESS)
radio1.set_tx_address(RADIO1_TX_ADDRESS)
data_ready = radio1.is_data_ready()
rcv_payload = radio1.get_payload()
tx_payload = [219] * RADIO1_PAYLOAD_SIZE
radio1.transmit_payload(tx_payload)


print(data_ready, rcv_payload, "done, exiting...")

