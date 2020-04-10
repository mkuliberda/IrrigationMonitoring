import wireless_comm_lib as wireless
import time
import Scheduler
import threading
import re


RADIO1_CE_PIN = 26   # BCM pins numbering
RADIO1_IRQ_PIN = 13  # BCM pins numbering 
RADIO1_SPIDEV = 0
RADIO1_SPICS = 0
RADIO1_PAYLOAD_SIZE = 32
RADIO1_CHANNEL = 15
RADIO1_MY_ADDRESS = [231, 231, 231, 231, 231]  # 0xe7 is 231
RADIO1_TX_ADDRESS = [126, 126, 126, 126, 126]  # 0x7e is 126
messages_to_send_queue = []
messages_received_queue = []
command = [0] * RADIO1_PAYLOAD_SIZE


PLANTS_SCHEDULES = ["plants_group1_schedule.xml", "plants_group2_schedule.xml", "plants_group3_schedule.xml"]

lock = threading.RLock()

message_received_event = threading.Event()
get_status_event = threading.Event()
irrigation_time_event = threading.Event()


class schedulingThread(threading.Thread):
        def __init__(self, schedules):
                self._schedule = Scheduler.Scheduler(schedules)
                self._tags = self._schedule.get_tags()
                self._activity_previous = dict.fromkeys(self._tags, False)
                self._activity_current = dict.fromkeys(self._tags, False)
                self._activity_queue = []
                self._running = True
                self._activity_event = threading.Event()
                threading.Thread.__init__(self)

        def terminate(self):
                self._running = False

        def is_running(self):
                return self._running

        def run(self):
                while self._running:
                        if self._activity_changed() is True:
                                print("send_event")
                                self._activity_event.set()
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

        def configure_notification_event(self, event):
                self._activity_event = event



class communicationsThread(threading.Thread):
        def __init__(self, spi_dev, spi_cs, ce_pin, irq_pin, payload_size, channel, out_pwr, datarate, src_addr, dest_addr):
                self._radio1 = wireless.NRF24L01()
                self._radio1.init(spi_dev, spi_cs, ce_pin, irq_pin)
                self._radio1_configured = self._radio1.config(payload_size, channel, out_pwr, datarate)
                if self._radio1_configured is True: 
                        self._radio1.set_my_address(src_addr)
                        self._radio1.set_tx_address(dest_addr)
                        self._running = True
                else:
                        self._running = False
                        print("configuration of radio1 failed, terminating thread...")
                self._new_message_event = threading.Event()
                threading.Thread.__init__(self)

        def terminate(self):
                self._running = False

        def is_running(self):
                return self._running

        def run(self):
                while self._running:
                        while self._radio1.data_ready() == 1:
                                payload = self._radio1.get_payload()
                                print(payload)
                                if payload[0] == wireless.direction.from_irm_to_rpi:  #standard message
                                        inbound_msg = wireless.IrrigationMessage(wireless.direction.from_irm_to_rpi)
                                        inbound_msg.set_buffer(payload, RADIO1_PAYLOAD_SIZE)
                                        if inbound_msg.validate_crc():
                                                print("validated msg received, todo...")
                                                self._new_message_event.set()
                                        else:
                                                print("crc didn't pass, todo...")
                                        del inbound_msg

                                elif payload[0] == wireless.direction.from_rpi_to_irm:  #confirmation message
                                        confirmation_msg = wireless.IrrigationMessage(wireless.direction.from_rpi_to_irm)
                                        confirmation_msg.set_buffer(payload, RADIO1_PAYLOAD_SIZE)
                                        if confirmation_msg.validate_crc():
                                                print(confirmation_msg.decode_confirmation()) #returns class confirmation_s
                                                self._new_message_event.set()
                                        else:
                                                print("crc didn't pass, todo...")
                                        del confirmation_msg
                                else:
                                        print("unknown message")
                        time.sleep(0.05)

        def configure_notification_event(self, event):
                self._new_message_event = event
        
        def send_message(self, payload):
                self._radio1.transmit_payload(payload)
                while self._radio1.get_transmission_status() == wireless.NRF24L01_TransmitStatus.Sending:
                        pass     
                print("message sent", payload)
                self._radio1.power_up_rx()
                while self._radio1.get_status() != 14:
                        time.sleep(0.05)
                        self._radio1.power_up_rx()
                print("back to receiver mode")

        def retreive_received_messages(self):
                return "message"

def get_status(event):
        while True:
                event.set()
                time.sleep(30)      


# RPi->STM32            |0xAA|Target|ID|Cmd|Dummy|CRC|
# bytes                 |1   |1     |1 |1  |27   | 1 |

def encode_message(payload_size, direction, target, id, command):
        payload = [0] * payload_size
        payload[0] = int(direction)
        payload[1] = int(target)
        payload[2] = int(id)
        payload[3] = int(command)
        payload[-1] = 5         # crc in the future as last byte
        return payload

# STM32->RPi            |0xBB|Target|ID|Value|String|CRC|
# bytes                 |1   | 1    |1 |4    |24    |1  |
def decode_message(payload):  # TODO
        message = payload
        #wireless.target.values # returns enums as dictionary
        return message

if __name__ == "__main__":

        irrigation_scheduler = schedulingThread(PLANTS_SCHEDULES)
        irrigation_scheduler.configure_notification_event(irrigation_time_event)
        irrigation_scheduler.start()

        wireless_link = communicationsThread(RADIO1_SPIDEV, RADIO1_SPICS, RADIO1_CE_PIN, RADIO1_IRQ_PIN,
                                                RADIO1_PAYLOAD_SIZE, RADIO1_CHANNEL,
                                                wireless.NRF24L01_OutputPower.M6dBm,
                                                wireless.NRF24L01_DataRate._1Mbps,
                                                RADIO1_MY_ADDRESS, RADIO1_TX_ADDRESS)
        wireless_link.configure_notification_event(message_received_event)
        wireless_link.start()

        status_getter = threading.Thread(name='status getter', target=get_status, args=(get_status_event,))
        status_getter.daemon = True
        status_getter.start()

        tx_payload = [218] * RADIO1_PAYLOAD_SIZE


        try:
                while True:
                        irrigation_time_event.wait(0.5)
                        if irrigation_time_event.is_set():
                                irrigation_time_event.clear()
                                tasks = irrigation_scheduler.pick_tasks_from_queue()
                                for task in tasks:
                                        outbound_msg = wireless.IrrigationMessage(wireless.direction.from_rpi_to_irm)
                                        irrigation_cmd = wireless.cmd_s()
                                        irrigation_cmd.target = wireless.target.Sector
                                        irrigation_cmd.target_id = int(re.findall(r'\d+',task.keys()[0])[0])
                                        if task.values()[0]: 
                                                irrigation_cmd.cmd = wireless.command.Start
                                                tx_payload = outbound_msg.encode_cmd(irrigation_cmd)
                                        else:
                                                irrigation_cmd.cmd = wireless.command.Stop
                                                tx_payload = outbound_msg.encode_cmd(irrigation_cmd)
                                        wireless_link.send_message(tx_payload)
                                        del outbound_msg
                                        del irrigation_cmd
                        else:
                                print("there's no irrigation event")

                        get_status_event.wait(0.5)
                        if get_status_event.is_set():
                                get_status_event.clear()
                                outbound_msg = wireless.IrrigationMessage(wireless.direction.from_rpi_to_irm)
                                status_cmd = wireless.cmd_s()
                                status_cmd.target = wireless.target.All
                                status_cmd.target_id = 0
                                status_cmd.cmd = wireless.command.GetStatus
                                tx_payload = outbound_msg.encode_cmd(status_cmd)
                                wireless_link.send_message(tx_payload)
                                del outbound_msg
                                del status_cmd
                        else:
                                print("there's no new messages")

                        
        except KeyboardInterrupt:
                pass


        print("shutting down...")

        irrigation_scheduler.terminate()
        irrigation_scheduler.join(5)
        del irrigation_scheduler
        print("irrigation scheduler off!")

        wireless_link.terminate()
        wireless_link.join(2)
        del wireless_link
        print("wireless_link off!")

        del status_getter
        print("status_getter off!")

        print("done, exiting...")

