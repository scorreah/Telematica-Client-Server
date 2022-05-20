# ********************************************************************************************
    # Project: Cliente-Servidor API Sockets
    # Course: ST0255 - Telemática
    # MultiThread TCP-SocketServer
# ********************************************************************************************

# Import libraries for networking communication and concurrency...

import socket
import threading
import constants
import methods
import time

# Defining a socket object...
# AF_INET define la familia(tipo) de direcciones como ipv4
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Define la direccion del servidor
server_address = constants.IP_SERVER

def main():
    print("***********************************")
    print("Server is running...")
    print("Dir IP:",server_address )
    print("Port:", constants.PORT)
    server_execution()
    
# Handler for manage incomming clients conections...

def handler_client_connection(client_connection,client_address):
    print(f'New incomming connection is coming from: {client_address[0]}:{client_address[1]}')
    is_connected = True
    while is_connected:
        # Mensaje de Request
        data_recevived = b''
        # while True:
        #     datos = client_connection.recv(constants.RECV_BUFFER_SIZE)
        #     if (len(datos) < 2):
        #         break
        #     data_recevived = data_recevived + datos
        #     time.sleep(0.1)
        data_recevived = client_connection.recv(999999999)
        print('Data received.')
        remote_string = data_recevived.split(b'\r\n\r\n') 
        header = remote_string[0].decode(constants.ENCONDING_FORMAT)
        if len(remote_string) > 1:
            data = remote_string[1]
        else:
            data = ''
        remote_command = header.split()
        command = remote_command[0]
        print (f'Data received from: {client_address[0]}:{client_address[1]}')
        print(f'Metodo: {command}')
        #print('Client request ' + command +' '+ remote_command[1])
        
        if (command == constants.GET):
            response = methods.get(header, data)
            #client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
            client_connection.sendall(response)
            is_connected = False
        elif (command == constants.POST):
            response = methods.post(header, data)
            #client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
            client_connection.sendall(response)
            is_connected = False
        elif (command == constants.HEAD):
            response = methods.head(header, data)
            #client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
            client_connection.sendall(response)
            is_connected = False
        
        else:
            response = '400 BCMD\n\rCommand-Description: Bad command\n\r'
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
    
    print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')
    client_connection.close()

#Function to start server process...
def server_execution():
    # Tupla ip - puerto
    tuple_connection = (server_address,constants.PORT)
    # Colocamos el socket visible en privado
    server_socket.bind(tuple_connection)
    # Definimos la configuracion del socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print ('Socket is bind to address and port...')
    # Especificamos al socket tener en cola no mas de 5 solicitudes por conexion
    server_socket.listen(5)
    print('Socket is listening...')
    while True:
        # Objeto socket, ip-puerto
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handler_client_connection, args=(client_connection,client_address))
        client_thread.start()
    print('Socket is closed...')
    server_socket.close()

if __name__ == "__main__":
    main()