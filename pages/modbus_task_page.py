import json
import requests
import streamlit as st
import config
import init
from Save.Save import save
from models.client_pcs import ClientPC
from models.modbus_task import ModbusTask, ModbusAddr

modbus_device_list = []
init.init_devices(st)

if "device_list" in st.session_state.keys():
    modbus_device_list = st.session_state["device_list"]

init.init_clients(st)
client_device_list:list[ClientPC]
if "client_pcs" in st.session_state.keys():
    client_device_list = st.session_state["client_pcs"]

init.init_modbus_register(st)
modbus_register_list:list[ModbusAddr] = []
if "modbus_register" in st.session_state.keys():
    modbus_register_list = st.session_state["modbus_register"]

client:ClientPC = st.selectbox("Client auswählen", client_device_list)

if client:
    device = st.selectbox("select device", options=modbus_device_list)
    response = []

try:
    response = requests.get(f'http://{client.url}/modbus/getRunningTasks/', timeout=2)
except Exception as e:
    st.write(f"Client {client.url} nicht erreichbar")

if response:

    with st.expander("Laufenden Modbus-Tasks anzeigen"):
        st.write(f"Die folgenden Tasks sind auf {client.name}/ {client.url} aktiv")
        if response:
            tasks = json.loads(response.text)
            task_list = []
            st.write(tasks)
        errors = []
        for task in tasks:
            if task["isError"]:
                errors.append(task)
        if errors:
            st.write("Task with errors")
            st.write(errors)
        else:
            st.write("no errors in tasks")

    with st.expander("Neues Register anlegen"):
        modbus_addr_name = st.text_input("Register Namen festlegen", "Spannung")
        modbus_addr = st.number_input("Modbus Addresse",19000)
        modbus_type = st.selectbox("Typ festlegen", ["float","short"])
        NB = st.number_input("NB",1)
        click = st.button("Modbus Register hinzufügen")
        if click:
            modbus_addr: ModbusAddr = ModbusAddr(name=modbus_addr_name, type=modbus_type, addr=modbus_addr, nb=NB)
            already_created = False
            for saved_modbus_addr in modbus_register_list:
                if modbus_addr.addr == saved_modbus_addr.addr or modbus_addr.name == saved_modbus_addr.name:
                    already_created = True

            if not already_created:
                modbus_register_list.append(modbus_addr)
                save(config.INSTANCE_FILE_PATH + config.INSTANCE_MODBUS_REGISTER, modbus_register_list)
                st.rerun()
            else:
                st.write(f"Modbus-Register mit der Nummer {modbus_addr} wurde bereits angelegt")

        modbus_addr_select_list = st.multiselect("Zu löschen Modbus Addressen", modbus_register_list)
        click_delete = st.button("Modbus Register löschen")

        if click_delete:
            modbus_addr =  [reg for reg in modbus_register_list if reg not in modbus_addr_select_list ]
            save(config.INSTANCE_FILE_PATH + config.INSTANCE_MODBUS_REGISTER, modbus_addr)
            st.rerun()

    with st.expander("Task vom Client entfernen "):
        if response:
            tasks = json.loads(response.text)
            task_list = []
            result ={}
            for item in tasks:
                result[item["name"]] = st.checkbox(item["name"])

            click = st.button("remove")

            if click:

                for key, item in result.items():
                    if item:
                        response = requests.delete(f'http://{client.url}/modbus/removeTask/',params={"task_name":key},  timeout=2)
                        print(response)
                        print(key)
                st.rerun()

    with st.expander("Neuen Modbus-Task auf dem Client anlegen"):

            try:
                response_callables = requests.get(f'http://{client.url}/modbus/getCallables/',timeout=2)
            except:
                st.write(f"Client {client.url} nicht erreichbar")

            if response_callables and response_callables.status_code == 200 and device:
                response_without_quotes = response_callables.text.replace('"', '')
                parsed_list = response_without_quotes.strip('[]').split(',')
                name = st.text_input("name", )
                func = st.selectbox("Funktion",options=parsed_list)
                modbus_addr_list = st.multiselect("Modbus Addressen", modbus_register_list)
                interval = st.number_input("Interval", 1)

                click = st.button("Task zum Client hinzufügen")

                if click and name and func and interval:
                    modbus_task = ModbusTask(name=name, interval=interval, func=func, MODBUS_ADDR=modbus_addr_list ,credentials=device)
                    print(modbus_task.dict())
                    try:
                        # post_response =  requests.post(f'http://{client.url}/modbus/addTask/', json=json.dumps(modbus_task))
                        post_response =  requests.post(f'http://{client.url}/modbus/addTask/', json=modbus_task.dict())
                    except Exception as e:
                        print(e)
                    st.write(post_response.status_code)

                    st.rerun()

