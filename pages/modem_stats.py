import json
import time

import requests
import streamlit as st
from pydantic import BaseModel

import config
import init
from Save.Save import save
from models.anomaly_task import AnomalyTask
from models.client_pcs import ClientPC
from models.modbus_task import ModbusTask, ModbusAddr
from models.virtual_task import VirtualTask, VirtualRegister


character_list = ["Mittelwert", "Standardabweichung", "Schiefe", "Kurtosis","Shapiro-Wilk Test","Kolmogorov-Smirnov Test"]



init.init_clients(st)
client_device_list:list[ClientPC]
if "client_pcs" in st.session_state.keys():
    client_device_list = st.session_state["client_pcs"]



# class Task(BaseModel):
#     name: str
#     func: str
#     interval: int
#     send_interface: str = "5G"
#     send_via: str = "eth"
#     next_run: float = None
#     canceled: bool = False
#     isRunning: bool = False
#     isError: bool = False
#     type: str = ""
#
#     def __init__(self, **data):
#         super().__init__(**data)
#         if self.next_run is None:
#             self.next_run = time.time()
        # self.next_run = data.get('next_run', time.time())



# init.init_virtual_register(st)
# virtual_register_list:list[VirtualRegister] = []
# if "virtual_register" in st.session_state.keys():
#     virtual_register_list = st.session_state["virtual_register"]

client:ClientPC = st.selectbox("Client auswählen", client_device_list)
response = ""

# if "client" in locals() and client:

try:
    response = requests.get(f'http://192.168.100.104:29000/monitor_data_transfer/getRunningTasks/', timeout=2)
    response_client = requests.get(f'http://{client.url}/virtual/getRunningTasks/', timeout=2)
except Exception as e:
    st.write(f"Client localhost nicht erreichbar")

if response:
    tasks = json.loads(response_client.text)
    tasks_stats = json.loads(response.text)
    task_list = []

    with st.expander("Laufende Tasks anzeigen"):
        # st.write(f"Die folgenden Tasks sind auf {client.name}/ {client.url} aktiv")
        if response:
            # tasks = json.loads(response.text)
            # task_list = []
            st.write(tasks_stats)


        # errors = []
        # # for task in tasks:
        # #     if task["isError"]:
        # #         errors.append(task)
        # if errors:
        #     st.write("Task with errors")
        #     st.write(errors)
        # else:
        #     st.write("no errors in tasks")

    # with st.expander("Task entfernen "):
    #     if response:
    #         tasks = json.loads(response.text)
    #         task_list = []
    #         result ={}
    #         for item in tasks:
    #             # result[item["name"]] = st.checkbox(item["name"])
    #
    #         click = st.button("remove")
    #
    #         if click:
    #             for key, item in result.items():
    #                 if item:
    #                     response = requests.delete(f'http://{client.url}/removeTask/',params={"task_name":key},  timeout=2)
    #                     print(response)
    #                     print(key)
    #             st.rerun()

    # with st.expander("Neues Register anlegen"):
    #     register_name = st.text_input("Register Namen festlegen", "Spannung")
    #     amplitude = st.number_input("Amplitude", value=1,min_value=0,max_value=1000)
    #     noise_level = st.number_input("noise_level", value= 1,min_value=0,max_value=20)
    #     duration = st.number_input("duration", value=1,min_value=1,max_value=86400)
    #     offset = st.number_input("offset", value=0)
    #     phase = st.number_input("phasen verschiebung", value=0)
    #     click = st.button("Modbus Register hinzufügen")
    #     if click:
    #         virtual_register: ModbusAddr = VirtualRegister(name=register_name,
    #                                                   amplitude=amplitude,
    #                                                   noise_level=noise_level,
    #                                                   duration=duration,
    #                                                   offset=offset,
    #                                                   phase_shift=phase
    #                                                        )
    #         already_created = False
    #         for save_virtual_register in virtual_register_list:
    #             if virtual_register.name == save_virtual_register.name:
    #                 already_created = True
    #
    #         if not already_created:
    #             virtual_register_list.append(virtual_register)
    #             save(config.INSTANCE_FILE_PATH + config.INSTANCE_VIRTUAL_REGISTER, virtual_register_list)
    #             st.rerun()
    #         else:
    #             st.write(f"Modbus-Register mit der Nummer {virtual_register} wurde bereits angelegt")
    #
    #     virtual_select_list = st.multiselect("Zu löschen Modbus Addressen", virtual_register_list)
    #     click_delete = st.button("Modbus Register löschen")
    #
    #     if click_delete:
    #         virtual_register= [reg for reg in virtual_register_list if reg not in virtual_select_list]
    #         save(config.INSTANCE_FILE_PATH + config.INSTANCE_VIRTUAL_REGISTER, virtual_register)
    #         st.rerun()

    # with st.expander("Neues Task mit virtuellen Registern auf dem Client anlegen"):

with st.expander("Neuer Anomalie Task"):

    try:
        response_callables = requests.get(f'http://{client.url}/getCallables/', timeout=2)
        # response_register = requests.get(f'http://{client.url}/virtual/getRegisters/', timeout=2)
    except:
        st.write(f"Client {client.url} nicht erreichbar")

    parsed_list = response_callables.text.replace('"', '').strip('[]').split(',')

    name = st.text_input("name Task")
    task_to_be_tested = st.selectbox("Task", options=[task["name"] for task in tasks])
    # url = f'http://{client.url}/monitor_data_transfer/getRegisters/'
    url = "http://192.168.100.104:29000/monitor_data_transfer/getRegisters/"
    registers_for_tasks = requests.get(url,params={"measurement_name": task_to_be_tested}, timeout=2)
    registers_to_be_checked = st.multiselect("Register die geprüft werden sollten", options=[register for register in json.loads(registers_for_tasks.text)])

    characteristics_list = st.multiselect("Zu erfassende Grenzwerte", character_list)
    critcal_limits = {}
    limits_ok = {}
    numbers = []

    test_for_limits = st.multiselect("Zu Prüfende Grenzwerte", characteristics_list)
    if len(test_for_limits) > 0:
        left, right = st.columns(2)
        for characteristics in test_for_limits:
            numbers.append(right.number_input(characteristics))

    interval = st.number_input("Interval", min_value=10,value=10)


    for i,number in enumerate(numbers):
        critcal_limits[characteristics_list[i]] = number
        limits_ok[characteristics_list[i]] = True
    #Click add new task on client
    print(critcal_limits)
    click = st.button("Virtuellen Task zum Client hinzufügen")

    if click and interval:

        task = AnomalyTask(name=name,
                           func="calculate_stats",
                           type="stats",
                            interval=interval,
                            task_name= task_to_be_tested,
                            critcal_limits=critcal_limits,
                            limits_ok=limits_ok,
                            characteristics=characteristics_list,
                           registers_to_be_checked = registers_to_be_checked,
                    )

        st.write(task.name)
    #   req
        request = task.dict()
        try:
            # post_response = requests.post(f'http://192.168.100.104:29000/monitor_data_transfer/addTask/', json=task.dict())
            post_response = requests.post(f'http://192.168.100.104:29000/monitor_data_transfer/addTask/', json=request)
        except Exception as e:
            st.write(e)
        st.write(post_response.status_code)
        st.rerun()



