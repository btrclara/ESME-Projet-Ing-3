import socket
import csv
import time
import os

def write_csv(data):
    filename = '/home/pi/Desktop/Projet_gant-main/Projet_gant-main/real_time_system/data2.csv'
    if not os.path.exists(filename):
        open(filename, 'a').close
    if os.stat(filename).st_size == 0:
        with open('data2.csv', 'w', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow(['ax','ay','az','gx','gy','gz','flex0','flex1','flex2','flex3','flex4','duree','mot'])
    with open('data2.csv', 'a',newline = '') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)
            

host, port = ('0.0.0.0',1234)
MAX_CONNECTION = 2

while True:
    try :
        print("Start")
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
        socket_server.bind((host, port))
        print("Ready to receive ")
        while True:
            try:
                socket_server.listen(MAX_CONNECTION)
                conn, adress = socket_server.accept()
                print("Accept connexion")
                data = conn.recv(4096)
                if not data:
                    raise socket.error
                print("Data received")
                data = data.decode("utf8")
                print(data)
                print("//////////////")
                lst = eval(data)
                print(lst)
                write_csv(lst)
                print("Data in csv")
            except socket.error:
                print("Connection lost...reconnecting in 2 seconds")
                conn.close()
                socket_server.close()
                time.sleep(1)
                break
            except socket.error as e:
                print('Socket error occurred:', e)
                conn.close()
                break
                
    except KeyboardInterrupt:
        conn.close()
        socket_server.close()
        break