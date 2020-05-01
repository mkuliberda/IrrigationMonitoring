import wireless_comm_lib as wireless
import time
import Scheduler
import threading
import re
import collections


RADIO1_CE_PIN = 26   # BCM pins numbering
RADIO1_IRQ_PIN = 13  # BCM pins numbering 
RADIO1_SPIDEV = 0
RADIO1_SPICS = 0
RADIO1_PAYLOAD_SIZE = 32
RADIO1_CHANNEL = 15
RADIO1_MY_ADDRESS = [231, 231, 231, 231, 231]  # 0xe7 is 231
RADIO1_TX_ADDRESS = [126, 126, 126, 126, 126]  # 0x7e is 126
COMMS_REFRESH_RATE_MS = 50

PLANTS_SCHEDULES = ["plants_group1_schedule.xml", "plants_group2_schedule.xml", "plants_group3_schedule.xml"]
SCHEDULE_REFRESH_RATE_MS = 1000

MONITOR_REFRESH_RATE_MS = 1000

lock = threading.RLock()

message_received_event = threading.Event()
get_status_event = threading.Event()
irrigation_time_event = threading.Event()



class schedulingThread(threading.Thread):
        def __init__(self, schedules, refresh_rate_ms=1000):
                self._schedule = Scheduler.Scheduler(schedules)
                self._tags = self._schedule.get_tags()
                self._activity_previous = dict.fromkeys(self._tags, False)
                self._activity_current = dict.fromkeys(self._tags, False)
                self._activity_queue = []
                self._running = True
                self._activity_event = threading.Event()
                self._refresh_rate_s = refresh_rate_ms/1000.0
                threading.Thread.__init__(self)

        def terminate(self):
                self._running = False

        def is_running(self):
                return self._running

        def run(self):
                while self._running:
                        if self._activity_changed() is True:
                                print("irrigation activity change")
                                self._activity_event.set()
                        time.sleep(self._refresh_rate_s)
        
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
        def __init__(self, spi_dev, spi_cs, ce_pin, irq_pin, payload_size, channel, out_pwr, datarate, src_addr, dest_addr, refresh_rate_ms=20):
                self._radio1 = wireless.NRF24L01()
                self._radio1.init(spi_dev, spi_cs, ce_pin, irq_pin)
                self._radio1_configured = self._radio1.config(payload_size, channel, out_pwr, datarate)
                self._outbound_msg_queue = collections.deque() 
                self._inbound_msg_queue = collections.deque()
                self._awaiting_confirmation_msg_queue = collections.deque()
                self._refresh_rate_s = refresh_rate_ms/1000.0
                self._cmd_retry_counter_s = 0
                if self._radio1_configured is True: 
                        self._radio1.set_my_address(src_addr)
                        self._radio1.set_tx_address(dest_addr)
                        self._running = True
                else:
                        self._running = False
                        print("configuration of radio1 failed, terminating thread...")
                self._comm_lost_event = threading.Event()
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
                                #print("payload ", payload)
                                if payload[0] == wireless.direction_t.from_irm_to_rpi:  #standard message
                                        msg = wireless.IrrigationMessage(wireless.direction_t.from_irm_to_rpi)
                                        msg.set_buffer(payload, RADIO1_PAYLOAD_SIZE)
                                        if msg.validate_crc():
                                                message_dict = msg.decode_message()
                                                self._inbound_msg_queue.append(message_dict)
                                                self._new_message_event.set()
                                                #print("valid msg received:", message_dict)
                                        else:
                                                print("crc error")
                                        del msg

                                elif payload[0] == wireless.direction_t.from_rpi_to_irm:  #confirmation message
                                        msg = wireless.IrrigationMessage(wireless.direction_t.from_irm_to_rpi)
                                        msg.set_buffer(payload, RADIO1_PAYLOAD_SIZE)
                                        if msg.validate_crc():
                                                confirmation_dict = msg.decode_confirmation()
                                                if confirmation_dict['consumed'] == True:
                                                        del confirmation_dict['consumed']
                                                        for aw_confirmation_dict in list(self._awaiting_confirmation_msg_queue):
                                                                if aw_confirmation_dict == confirmation_dict:
                                                                        print("command: ",confirmation_dict['cmd'],"to ",confirmation_dict['target'],confirmation_dict['target_id']," confirmed")
                                                                        self._awaiting_confirmation_msg_queue.remove(aw_confirmation_dict)
                                        else:
                                                print("crc error")
                                        del msg
                                else:
                                        print("unknown message")

                        self._command_retry()
                        self._send_avbl_messages()
                        time.sleep(self._refresh_rate_s)

        def configure_comm_lost_event(self, event):
                self._comm_lost_event = event

        def configure_new_message_event(self, event):
                self._new_message_event = event
        
        def get_awaiting_confirmation_msg_queue(self):
                return self._awaiting_confirmation_msg_queue

        def _convert_cmd_to_dict(self, _cmd):
                return {'target': _cmd[1], 'target_id': _cmd[2], 'cmd': _cmd[3], 'subcmd1': 0, 'subcmd2': 0}

        def add_msg_to_queue(self, payload):
                self._outbound_msg_queue.append(payload)

        def _command_retry(self):  #WIP
        
                if self._cmd_retry_counter_s <= 5:
                        self._cmd_retry_counter_s += self._refresh_rate_s
                else:
                        self._cmd_retry_counter_s = 0  
                        while len(self._awaiting_confirmation_msg_queue) > 0:
                                msg_dict = self._awaiting_confirmation_msg_queue.pop()
                                outbound_msg = wireless.IrrigationMessage(wireless.direction_t.from_rpi_to_irm)
                                irrigation_cmd = wireless.cmd_s()
                                irrigation_cmd.target = wireless.target_t(msg_dict['target'])
                                irrigation_cmd.target_id = msg_dict['target_id']
                                irrigation_cmd.cmd = wireless.command_t(msg_dict['cmd'])
                                payload = outbound_msg.encode_cmd(irrigation_cmd)
                                self._outbound_msg_queue.append(payload)
                                print("command retry:", payload)
                                del outbound_msg
                                del irrigation_cmd

        def _send_avbl_messages(self):
                while len(self._outbound_msg_queue) > 0:
                        msg = self._outbound_msg_queue.pop()
                        if msg[3] == wireless.command_t.Start or msg[3] == wireless.command_t.Stop:  #only Start and Stop commmands are now enabled
                                self._awaiting_confirmation_msg_queue.append(self._convert_cmd_to_dict(msg))
                        self._radio1.transmit_payload(msg)
                        while self._radio1.get_transmission_status() == wireless.NRF24L01_TransmitStatus.Sending:
                                pass     
                        print("command sent:", self._convert_cmd_to_dict(msg))
                        time.sleep(0.05)
                self._radio1.power_up_rx()
                while self._radio1.get_status() != 14:
                        time.sleep(0.005)
                        self._radio1.power_up_rx()
        
        def get_new_message_count(self):
                return len(self._inbound_msg_queue)

        def retreive_new_message(self):
                return self._inbound_msg_queue.pop()

def get_status(event):
        while True:
                event.set()
                time.sleep(10)      


if __name__ == "__main__":

        irrigation_scheduler = schedulingThread(PLANTS_SCHEDULES, SCHEDULE_REFRESH_RATE_MS)
        irrigation_scheduler.configure_notification_event(irrigation_time_event)
        irrigation_scheduler.start()

        wireless_link = communicationsThread(RADIO1_SPIDEV, RADIO1_SPICS, RADIO1_CE_PIN, RADIO1_IRQ_PIN,
                                                RADIO1_PAYLOAD_SIZE, RADIO1_CHANNEL,
                                                wireless.NRF24L01_OutputPower.P0dBm,
                                                wireless.NRF24L01_DataRate._1Mbps,
                                                RADIO1_MY_ADDRESS, RADIO1_TX_ADDRESS,
                                                COMMS_REFRESH_RATE_MS)
        wireless_link.configure_new_message_event(message_received_event)
        wireless_link.start()

        status_checker = threading.Thread(name='status getter', target=get_status, args=(get_status_event,))
        status_checker.daemon = True
        status_checker.start()

        try:
                while True:
                        if message_received_event.is_set():
                                message_received_event.clear()
                                while wireless_link.get_new_message_count() > 0:
                                        print(wireless_link.retreive_new_message())

                        if irrigation_time_event.is_set():
                                irrigation_time_event.clear()
                                tasks = irrigation_scheduler.pick_tasks_from_queue()
                                for task in tasks:
                                        outbound_msg = wireless.IrrigationMessage(wireless.direction_t.from_rpi_to_irm)
                                        irrigation_cmd = wireless.cmd_s()
                                        irrigation_cmd.target = wireless.target_t.Sector
                                        irrigation_cmd.target_id = int(re.findall(r'\d+',task.keys()[0])[0])
                                        if task.values()[0]: 
                                                irrigation_cmd.cmd = wireless.command_t.Start
                                                tx_payload = outbound_msg.encode_cmd(irrigation_cmd)
                                        else:
                                                irrigation_cmd.cmd = wireless.command_t.Stop
                                                tx_payload = outbound_msg.encode_cmd(irrigation_cmd)
                                        wireless_link.add_msg_to_queue(tx_payload)
                                        del outbound_msg
                                        del irrigation_cmd
                        else:
                                print("there's no irrigation event")

                        if get_status_event.is_set():
                                get_status_event.clear()
                                outbound_msg = wireless.IrrigationMessage(wireless.direction_t.from_rpi_to_irm)
                                status_cmd = wireless.cmd_s()
                                status_cmd.target = wireless.target_t.All
                                status_cmd.target_id = 0
                                status_cmd.cmd = wireless.command_t.GetStatus
                                tx_payload = outbound_msg.encode_cmd(status_cmd)
                                wireless_link.add_msg_to_queue(tx_payload)
                                del outbound_msg
                                del status_cmd
                        else:
                                print("there's no new messages")
                        time.sleep(MONITOR_REFRESH_RATE_MS/1000)

                        
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

        del status_checker
        print("status_checker off!")

        print("done, exiting...")

