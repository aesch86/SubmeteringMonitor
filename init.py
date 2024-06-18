import streamlit as st
import config
from Save.Restore import restore

st.session_state["device_list"] = []
def init_devices(st):
    st.session_state["device_list"] = restore(config.INSTANCE_FILE_PATH + config.INSTANCE_FILENAME)

def init_clients(st):
    st.session_state["client_pcs"] = restore(config.INSTANCE_FILE_PATH + config.INSTANCE_CLIENTPCs_FILENAME)

def init_modbus_register(st):
    st.session_state["modbus_register"] = restore(config.INSTANCE_FILE_PATH + config.INSTANCE_MODBUS_REGISTER)

def init_virtual_register(st):
    st.session_state["virtual_register"] = restore(config.INSTANCE_FILE_PATH + config.INSTANCE_VIRTUAL_REGISTER)

