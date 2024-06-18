import streamlit as st
import config
import init
from Save.Restore import restore

init.init_devices(st)
init.init_clients(st)

client_device_list = []

if "client_pcs" in st.session_state.keys():
    client_device_list = st.session_state["client_pcs"]

st.write(client_device_list)