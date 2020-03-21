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
DUMMY = [0] * 27
MSG_STRING = "That's only an empty msg"
commands_queue = []
messages_queue = []
command = [wireless.dir.from_rpi_to_irm, wireless.tgt.Generic, 0, wireless.cmd.None, DUMMY, 0]


PLANTS_SCHEDULES = ["plants_group1_schedule.xml", "plants_group2_schedule.xml", "plants_group3_schedule.xml"]

lock = threading.RLock()
send_cmd_event = threading.Event()
confirmation_event = threading.Event()
rcv_msg_event = threading.Event()
get_plants_health_event = threading.Event()
irrigation_time_event = threading.Event()


class schedulingThread(threading.Thread):
        def __init__(self, schedules):
                self._schedule = Scheduler.Scheduler(schedules)
                self._tags = self._schedule.get_tags()
                self._activity_previous = dict.fromkeys(self._tags, False)
                self._activity_current = dict.fromkeys(self._tags, False)
                self._activity_queue = []
                self._running = True
                threading.Thread.__init__(self)

        def terminate(self):
                self._running = False

        def is_running(self):
                return self._running

        def run(self):
                while self._running:
                        if self._activity_changed() is True:
                                print("send_event")
                        time.sleep(1)
        
        def _activity_changed(self):
                event_flag = False
                self._activity_current = self._schedule.is_active_all()
                for key in self._activity_current:
                        if self._activity_current[key] != self._activity_previous[key]:
                                self._activity_queue.append({key: self._activity_current[key]})
                                self._activity_previous[key] = self._activity_current[key] 
                                event_flag = True
                return event_flag

        def pick_tasks_from_queue(self):
                temp_queue = self._activity_queue
                self._activity_queue = []
                return temp_queue

        def clear_tasks_queue(self):
                self._activity_queue = []

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
                        time.sleep(0.2)

class monitoringThread(threading.Thread):
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

irrigation_scheduler = schedulingThread(PLANTS_SCHEDULES)
irrigation_scheduler.start()


radio1 = wireless.NRF24L01()
radio1.init(RADIO1_SPIDEV, RADIO1_SPICS, RADIO1_CE_PIN, RADIO1_IRQ_PIN)
config = radio1.config(RADIO1_PAYLOAD_SIZE, RADIO1_CHANNEL, wireless.NRF24L01_OutputPower.NRF24L01_OutputPower_0dBm, wireless.NRF24L01_DataRate.NRF24L01_DataRate_2M)
radio1.set_my_address(RADIO1_MY_ADDRESS)
radio1.set_tx_address(RADIO1_TX_ADDRESS)

tx_payload = [218] * RADIO1_PAYLOAD_SIZE
radio1.transmit_payload(tx_payload)
while radio1.get_transmission_status() == wireless.NRF24L01_TransmitStatus.NRF24L01_Transmit_Status_Sending:
        print ("Sending...")
        time.sleep(0.05)
print(radio1.get_transmission_status())
radio1.power_up_rx()
time.sleep(0.5)
print(radio1.get_status())
print(irrigation_scheduler.pick_tasks_from_queue())
#irrigation_scheduler.mark_tasks_consumed()



irrigation_scheduler.terminate()
irrigation_scheduler.join(5)
del irrigation_scheduler
print("done, exiting...")

