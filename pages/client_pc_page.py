import ipaddress
import pandas as pd
import streamlit as st
import config
import init
from Save.Save import save
from models.client_pcs import ClientPC

init.init_clients(st)
client_device_list:list[ClientPC]
if "client_pcs" in st.session_state.keys():
    client_device_list = st.session_state["client_pcs"]

#function check if a ip is valid
def is_valid_ipv4_address(ip) -> bool:
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

#show all created pc
with st.expander("show ipc``"):
    listof = [obj.dict() for obj in client_device_list]
    df = pd.DataFrame(listof)
    st.dataframe(df)

#Create a new ClientPC and Save it
with st.expander("add new ipc"):
    url: str = ""
    #get data input
    name = st.text_input("name", )
    ip = st.text_input("Ip", )
    port = st.number_input("Port für RestInterface", step=1)
    #ip is ok
    valid_Ip = is_valid_ipv4_address(ip)
    click = st.button("Gerät hinzufügen")

    #save ipc
    if click:
        if valid_Ip and port != 0:
            device_already_saved = False
            url = f"{ip}:{port}"
            new_client = ClientPC(name=name, url= url)

            for client in client_device_list:
                if new_client.url == client.url or new_client.name == client.url:
                    st.write("Ein Client mit dieser IP oder Namen wurde bereits festgelegt.")
                    device_already_saved = True
                    break

            if not device_already_saved:
                client_device_list.append(new_client)
                save(config.INSTANCE_FILE_PATH + config.INSTANCE_CLIENTPCs_FILENAME, client_device_list)
                # st.write("client pc gespeichert")
                st.rerun()
        else:
            st.write("keine gültige IP oder port ist null")

#delete a client pc
with st.expander("remove ipc"):
    left, mid, right = st.columns(3)
    result = {}
    for index, item in enumerate(client_device_list): #create a chosable checkbox for all saved client pc
        result[item.name] = st.checkbox(item.name+str(index))
    click = st.button("remove")
    if click:
        client_device_list_new = []
        client_device_list_new = [client for client in client_device_list for key, item in result.items() if key == client.name and not item ] #get all client pc which are not selected
        save(config.INSTANCE_FILE_PATH + config.INSTANCE_CLIENTPCs_FILENAME, client_device_list_new) #save all not selected clientpc`s
        st.rerun() #rerun whole page