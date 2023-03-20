import network
import time
import socket
from secrets import secrets


host, port =('172.20.10.10', 1234)

def run():
    wlan_connection = connect_to_wlan(secrets)
    
    if wlan_connection.isconnected():
        print("Successfully connected to wlan")
        socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_conn.connect((host, port))
        
        while True:
            time.sleep(5)
            try:
                data = "Bonjour, je suis le client"
                send_data(socket_conn, data)
                print("ok")
            except Exception as e:
                print("Connexion au serveur refusé")
                print(e)
                
    else:
        print("Fail to connect to wlan, ensure that network is 2.4 Ghz")
        
def send_data(socket_conn, json_data):
    encoded_data = json_data.encode("utf8")
    socket_conn.sendall(encoded_data)

def connect_to_wlan(secrets: dict):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets['ssid'], secrets['pw'])
    
    return wlan

if __name__ == "__main__":
    run()