# ********************************************************************************************
    # Project: Client-Server using API Socket
    # Course: ST0255 - Telemática
    # TCP-Socket Client
    # By Simon Correa Henao
# ********************************************************************************************

#Import libraries for networking communication...
import os
import time
import socket
import constants
import re

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def print_request(request):
    separator = '-'
    print(separator*51)
    print(separator*21, 'REQUEST', separator*21)
    print(separator*51)
    print(request)
    print(separator*51)
    print(separator*20, 'RESPONSE', separator*21)
    print(separator*51)

def parseo_recursivo(referencias, host, port, position):
    print('-'*50)
    print('Retreaving external files and references...')
    for ref in referencias:
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f'Reference: {ref}')
        request = f'GET {position}{ref} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n'
        print(request)
        requesting_parts = request.split()
        file_name_path = requesting_parts[1]
        file_name = file_name_path.rsplit('/', 1)
        file_name = file_name[len(file_name)-1]
        print(f'File: {file_name}')
        if file_name == '/' or file_name == '':
            file_name = 'index.html'
            file_type = 'html'
        else:

            file_type = file_name.split(".")[1]
            print(f'File type: {file_type}')
            
        request = request.encode()
        client_socket.send(request)
        client_socket.send(b'')
        response = b""
        while True:
            datos = client_socket.recv(constants.RECV_BUFFER_SIZE)
            if (len(datos) < 1):
                break
            response = response + datos
            time.sleep(0.1)
        print('File recovered...')
        path = f'{host}/'
        try:
            # os.mkdir(host)
            if ref.find('/') != -1:
                path = ref.rsplit('/', 1)[0]
                print(path)
                path = f'{host}/{position}{path}'
                print(path)
                os.makedirs(path)
        except:
            pass
        file = open(f'{path}/{file_name}', 'wb')
        file.write(response.split(b"\r\n\r\n")[1])
        file.close()

        client_socket.close()
        print(f'File {ref} saved locally\n')

def get():
    pass


def main():
    # ESTABLISH SOCKET CONNECTION
    print('***********************************')
    print('Client is running...')
    message = 'Enter the host and port you want to connect\nseparated by space:\n> '
    message_splitted = input(message).split()
    host, port = message_splitted[0], int(message_splitted[1])
    client_socket.connect((host, port))
    local_tuple = client_socket.getsockname()
    print('Connected to the server from:', local_tuple)

    # CHOOSING HTTP METHOD
    choosen_method = int(input('Choose a method using its number:\n1. GET\n2. POST\n3. HEAD\n> '))
    if choosen_method == 1:
        method = constants.GET
    elif choosen_method == 2:
        method = constants.POST
        post_type = int(input('What would you like to submit?\r\n1. Json\r\n2. File\r\n> '))
        if post_type == 2:
            content_type = 'multipart/form-data'
            file_path = input('Please specify the relative path of the file: ')
            try:
                print(f'File loading: {file_path}')
                file = open(file_path, 'rb')
                file_data = file.read()
                file_len = len(file_data)
                file.close()
            except Exception:
                print(Exception)
    elif choosen_method == 3:
        method = constants.HEAD
    else:
        method = 'ERROR'
    
    # RESOURCE OF THE REQUEST
    resource = input('Please specify the resource you require:\n> ')

    # BUILDING HTTP REQUEST
    if choosen_method == 1:
        request = f'{method} {resource} HTTP/1.1\r\nHost: {host}:{port}\r\nConnection: keep-alive\r\n\r\n'
    elif choosen_method == 2:
        request = f'{method} {resource} HTTP/1.1\r\nHost: {host}:{port}\r\nConnection: keep-alive\r\n'
        request += f'Content-Type: {content_type};\r\nContent-length: {file_len}\r\n\r\n'
    else:
        request = f'{method} {resource} HTTP/1.1\r\nHost: {host}:{port}\r\nConnection: keep-alive\r\n\r\n'

    # SENDING AND PRINTING REQUEST
    print_request(request)
    request = request.encode() #REQUEST HEADER
    if choosen_method == 2:
        request += file_data    # REQUEST CONTENT (POST METHOD)
    client_socket.send(request)

    # RECEIVING RESPONSE
    file_name = file_type = ''    
    response = b""
    while True:
        datos = client_socket.recv(constants.RECV_BUFFER_SIZE)
        if (len(datos) < 1):
            break
        response = response + datos
        time.sleep(0.1)
    print('Data received.')

    # PRINTING AND PROCESSING RESPONSE
    response_splitted = response.split(b"\r\n\r\n")
    response_headers = response_splitted[0].decode(constants.ENCONDING_FORMAT)
    response_content = response_splitted[1]
    if choosen_method == 1: # GET
        # Obtaining host and file name
        hostname = host
        # Processing Content-Type
        match = re.search(r"^Content-Type:\s(\w+/\w+).*$", response_headers, re.MULTILINE)
        mimetype = match.group(1)
        print(f'Mimetype: {mimetype}')
        # Processing file path and name
        file_name = resource.rsplit('/', 1)    # Split the filename from its path
        file_name = file_name[len(file_name)-1]
        position = file_name
        print(file_name)
        if file_name == '/' or file_name == '' and mimetype == 'text/html':
            position = '/'
            file_name = 'index.html'
            file_type = 'html'
        else:
            file_type = file_name.split(".")[1]
            print(file_type)

        # Save the resource in local
        try:
            os.mkdir(hostname)
        except:
            pass
        file = open(f"{hostname}/{file_name}", 'wb')
        file.write(response.split(b"\r\n\r\n")[1])
        file.close()


    client_socket.close()
    # 
    print(response_headers+'\r\n\r\n')
    if choosen_method == 1 and file_type == 'html' or file_type == 'txt':
        # PARSEO HTML
        response_content = response_content.decode(constants.ENCONDING_FORMAT)
        print(response_content)
        # Busqueda de referencias con Regex
        referencias = re.findall("\s(?:src|href)(?:=\")([a-zA-Z0-9._/-]+?)\"", response_content)
        # Elimina repetidos
        referencias = list(dict.fromkeys(referencias))
        print('Reference list: ', referencias)
        print('Position: ', position)
        parseo_recursivo(referencias, host, port, position)
    elif choosen_method == 2:
        print(f'Data sent to {host}{resource}')
    elif choosen_method == 3:
        pass
    else:
        print(f'File {file_name} saved in local')


if __name__ == '__main__':
    main()