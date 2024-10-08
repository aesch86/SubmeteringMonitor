import json
import numpy as np
import pandas as pd
import requests
import streamlit as st
import config
import init
from Save.Save import save
from models.client_pcs import ClientPC
from models.modbus_task import ModbusTask, ModbusAddr
from models.virtual_task import VirtualTask, VirtualRegister


init.init_clients(st)
client_device_list:list[ClientPC]
if "client_pcs" in st.session_state.keys():
    client_device_list = st.session_state["client_pcs"]

init.init_virtual_register(st)
virtual_register_list:list[VirtualRegister] = []
if "virtual_register" in st.session_state.keys():
    virtual_register_list = st.session_state["virtual_register"]

client:ClientPC = st.selectbox("Client auswählen", client_device_list)
response = ""

if "client" in locals() and client:

    try:
        response = requests.get(f'http://{client.url}/virtual/getRunningTasks/', timeout=2)
    except Exception as e:
        st.write(f"Client {client.url} nicht erreichbar")

    if response:

        st.write(f"Die folgenden Tasks sind auf {client.name} aktiv:")
        if response:
            tasks = json.loads(response.text)
            task_list = [[task["name"],task["func"],"Nein" if not task["isError"] else "Ja" ,task["interval"], task["interface"],task["protocol"],False] for task in tasks]
            task_dataframe = pd.DataFrame(task_list, columns=["Name", "Funktion", "IsError", "Intervall","interface", "protocol", "Löschen"])
            task_list = []
            table_result = ""
            table_result = st.data_editor(
                task_dataframe,
                # column_config={
                #     "favorite": st.column_config.CheckboxColumn(
                #         "blablalba",
                #         help="Select your **favorite** widgets",
                #         default=F,
                #     )
                # },
                # disabled=["widgets"],
                hide_index=False,
            )

            delete_coloumn = table_result.iloc[:, -1]

            if np.count_nonzero(delete_coloumn == True):
                deleting_tasks = dict(zip(table_result.iloc[:, 0], table_result.iloc[:, -1]))
                # print(task_dataframe.iloc[:,-1])
                click = st.button("remove")

                if click:
                    for key in deleting_tasks.keys():
                        if deleting_tasks[key]:
                            response = requests.delete(f'http://{client.url}/virtual/removeTask/',
                                                       params={"task_name": key}, timeout=2)

                    st.rerun()

        with st.expander("Neues virtuelles Register anlegen"):
            register_name = st.text_input("Register Namen festlegen", "Spannung")
            amplitude = st.number_input("Amplitude", value=1,min_value=0,max_value=1000)
            noise_level = st.number_input("noise_level", value= 1,min_value=0,max_value=20)
            duration = st.number_input("duration", value=1,min_value=1,max_value=86400)
            offset = st.number_input("offset", value=0)
            phase = st.number_input("phasen verschiebung", value=0)
            click = st.button("Modbus Register hinzufügen")
            if click:
                virtual_register: ModbusAddr = VirtualRegister(name=register_name,
                                                          amplitude=amplitude,
                                                          noise_level=noise_level,
                                                          duration=duration,
                                                          offset=offset,
                                                          phase_shift=phase
                                                               )
                already_created = False
                for save_virtual_register in virtual_register_list:
                    if virtual_register.name == save_virtual_register.name:
                        already_created = True

                if not already_created:
                    virtual_register_list.append(virtual_register)
                    save(config.INSTANCE_FILE_PATH + config.INSTANCE_VIRTUAL_REGISTER, virtual_register_list)
                    st.rerun()
                else:
                    st.write(f"Modbus-Register mit der Nummer {virtual_register} wurde bereits angelegt")

            virtual_select_list = st.multiselect("Zu löschen Modbus Addressen", virtual_register_list)
            click_delete = st.button("Modbus Register löschen")

            if click_delete:
                virtual_register= [reg for reg in virtual_register_list if reg not in virtual_select_list]
                save(config.INSTANCE_FILE_PATH + config.INSTANCE_VIRTUAL_REGISTER, virtual_register)
                st.rerun()

        # with st.expander("Neues Task mit virtuellen Registern auf dem Client anlegen"):
        with st.expander("Neuer Task"):

            try:
                response_callables = requests.get(f'http://{client.url}/virtual/getCallables/', timeout=2)
                # response_register = requests.get(f'http://{client.url}/virtual/getRegisters/', timeout=2)
            except:
                st.write(f"Client {client.url} nicht erreichbar")

            if response_callables and response_callables.status_code == 200:
                parsed_list = response_callables.text.replace('"', '').strip('[]').split(',')
                # register_list = response_register.text.replace('"', '').strip('[]').split(',')

                name = st.text_input("name virtual Task", )
                func = st.selectbox("Funktion virtual", options=parsed_list)
                virtual_registers = st.multiselect("Virtuelle Register", virtual_register_list)
                interval = st.number_input("Interval", 1)
                send_via = st.selectbox("Mit welchen Protokoll soll versendet werden",
                                        options=["websocket", "rest", "mqtt"])
                send_interface = st.selectbox("Mit welchen interface", options=["5G", "eth"])

                #Click add new task on client
                click = st.button("Virtuellen Task zum Client hinzufügen")

                if click and name and func and interval:

                    virtual_task = VirtualTask(name=name,
                                               interval=interval,
                                               func=func,
                                               virtual_register=virtual_registers,
                                               send_interface=send_interface,
                                               send_via=send_via
                                             )

                    try:
                        post_response = requests.post(f'http://{client.url}/virtual/addTask/', json=virtual_task.dict())
                    except Exception as e:
                        st.write(e)
                    st.write(post_response.status_code)
                    st.rerun()



