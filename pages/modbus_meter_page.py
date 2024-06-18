import pandas as pd
import streamlit as st
import config
import init
from Save.Save import save
from models.modbus_task import ModbusCredentials

init.init_devices(st)

modbus_device_list=[]
if "device_list" in st.session_state.keys():
    modbus_device_list = st.session_state["device_list"]

with st.expander("show devices"):
    listof = [obj.dict() for obj in modbus_device_list]
    df = pd.DataFrame(listof)
    st.dataframe(df)

with st.expander("add new device"):
    host = st.text_input("Host adresse", "192.168.200.100")
    unit_id = st.number_input("Unit ID", 1)
    timeout = st.number_input("Timeout", 2)
    port = st.number_input("Port", 502)

    click = st.button("Gerät hinzufügen")

    if click:
        new_modbus_device = ModbusCredentials(HOST=host,
                                              PORT=port,
                                              TIMEOUT=timeout,
                                              UNIT_ID=unit_id,
                                              AUTO_OPEN=True,
                                              )
        device_already_saved = False
        for device in modbus_device_list:
            if device == new_modbus_device:
                st.write("Das Gerät wurde bereits angelegt!")
                device_already_saved = True
                break

        if not device_already_saved:
            modbus_device_list.append(new_modbus_device)
            save(config.INSTANCE_FILE_PATH + config.INSTANCE_FILENAME, modbus_device_list)
            st.write("Gerät gespeichert")
            st.rerun()

with st.expander("remove device"):
    left, mid, right = st.columns(3)
    result = {}
    for index, item in enumerate(modbus_device_list):
        result[item] = st.checkbox(item.HOST + f"({index})")
    click = st.button("remove")
    if click:
        # modbus_device_list_new = [client for client in modbus_device_list for key, item in result.items() if
        #                           key != client and not item]
        modbus_device_list_new= []

        for key, item in result.items():
            if not item:
                modbus_device_list_new.append(key)

        save(config.INSTANCE_FILE_PATH + config.INSTANCE_FILENAME, modbus_device_list_new)
        st.rerun()
