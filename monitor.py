import wireless_comm_lib as wireless
import time
import Scheduler
import threading


# RPi->STM32            |0xAA|Target|ID|Cmd|Dummy|CRC|
# bytes                 |1   |1     |1 |1  |27   | 1 |

# STM32->RPi            |0xBB|Target|ID|Value|String|CRC|
# bytes                 |1   | 1    |1 |4    |24    |1  |

RADIO1_CE_PIN = 26   # BCM pins numbering
RADIO1_IRQ_PIN = 13  # BCM pins numbering 
RADIO1_SPIDEV = 0
RADIO1_SPICS = 0
RADIO1_PAYLOAD_SIZE = 32
RADIO1_CHANNEL = 15
RADIO1_MY_ADDRESS = [231, 231, 231, 231, 231]  # 0xe7 is 231
RADIO1_TX_ADDRESS = [126, 126, 126, 126, 126]  # 0x7e is 126
commands_queue = []
answers_queue = []
command_to_irm = [wireless.dir.from_rpi_to_irm, wireless.tgt.Generic]

PLANTS_SCHEDULES = ["plants_group1_schedule.xml", "plants_group2_schedule.xml", "plants_group3_schedule.xml"]

lock = threading.RLock()
send_cmd_event = threading.Event()
confirmation_event = threading.Event()
rcv_msg_event = threading.Event()

class scheduleThread(threading.Thread):
        def __init__(self, schedules):
                self.schedules = schedules
                self._running = True
                threading.Thread.__init__(self)

        def terminate(self):
                self._running = False

        def is_running(self):
                return self._running

        def run(self):
                while self._running:
                        time.sleep(1)

class communicationsThread(threading.Thread):
        def __init__(self):
                self._running = True
                threading.Thread.__init__(self)

        def terminate(self):
                self._running = False

        def is_running(self):
                return self._running

        def run(self):
                while self._running:
                        time.sleep(1)



plants_schedule = Scheduler.Scheduler(PLANTS_SCHEDULES)
print(plants_schedule.is_active_by_tag("Plants_group1"))
print(plants_schedule.is_active_by_tag("Plants_group2"))
print(plants_schedule.is_active_by_tag("Plants_group3"))
print(plants_schedule.is_active_all())
print(plants_schedule.print_full_schedule())



radio1 = wireless.NRF24L01()
radio1.init(RADIO1_SPIDEV, RADIO1_SPICS, RADIO1_CE_PIN, RADIO1_IRQ_PIN)
config = radio1.config(RADIO1_PAYLOAD_SIZE, RADIO1_CHANNEL, wireless.NRF24L01_OutputPower.NRF24L01_OutputPower_0dBm, wireless.NRF24L01_DataRate.NRF24L01_DataRate_2M)
radio1.set_my_address(RADIO1_MY_ADDRESS)
radio1.set_tx_address(RADIO1_TX_ADDRESS)

tx_payload = [218] * RADIO1_PAYLOAD_SIZE
radio1.transmit_payload(tx_payload)
time.sleep(0.2)
print(wireless.NRF24L01_TransmitStatus.NRF24L01_Transmit_Status_Sending, radio1.get_transmission_status())
radio1.power_up_rx()

print(radio1.get_status())
print("done, exiting...")

