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
for item in client_device_list:
    st.markdown("[![Foo](http://www.google.com.au/images/nav_logo7.png)](http://localhost:8501/virtual_task_page)")