import datetime


def get(r_header, r_data):
    string_list = r_header.split(" ")
    method = string_list[0]
    requesting_file = string_list[1]

    print('*'*51)
    print(' '*21, 'REQUEST', ' '*21)
    print(f'{r_header}\r\n')


    myfile = requesting_file.split("?")[0]
    myfile = myfile.lstrip("/") # Remueve ese caracter

    if(myfile == "" or myfile == "/"):
        myfile = "index.html"

    print('*'*51)
    #print('myfile: '+str(myfile))
    try:
        # Lee en formato byte
        file = open(myfile, 'rb')
        response = file.read()
        file_len = len(response)
        file.close()

        header = 'HTTP/1.1 200 OK\r\n'

        x = datetime.datetime.now()
        header += f'Date: {x.strftime("%a, %d %b %Y %X %Z")}\r\n'

        server = 'Python-Sockets/1.0 (Ubuntu)'
        header += f'Server: {server}\r\n'

        header += f'Content-Length: {file_len}\r\n'

        if myfile.endswith('.jpg') or myfile.endswith('jpeg'):
            mimetype = 'image/jpeg'
        elif (myfile.endswith('.gif')):
            mimetype = 'image/gif'
        elif (myfile.endswith('.csv')):
            mimetype = 'text/csv'
        elif (myfile.endswith('.css')):
            mimetype = 'text/css'
        elif (myfile.endswith('.json')):
            mimetype = 'application/json'
        elif (myfile.endswith('.pdf')):
            mimetype = 'application/pdf'
        else: 
            mimetype = 'text/html'
        header += 'Content-Type: ' + str(mimetype) + '\r\n\r\n'
    except Exception as e:
        header = 'HTTP/1.1 404 Not Found \r\n\r\n'
        response = '<html><body>Error 404: File not found</body></html>'.encode('utf-8')

    print(' '*21, 'RESPONSE', ' '*21)
    print(header)
    
    final_response = header.encode('utf-8') + response
    return final_response


def post(r_header, data):
    string_list = r_header.split(" ")
    method = string_list[0]
    requesting_file = string_list[1]

    print('*'*51)
    print(' '*21, 'REQUEST', ' '*21)
    print(f'{r_header}\r\n')


    myfile = requesting_file.split("?")[0]
    myfile = myfile.lstrip("/") # Remueve ese caracter

    if(myfile == "" or myfile == "/"):
        myfile = "uploads/noname"
        print('No name')

    print('*'*51)
    print('myfile: '+str(myfile))
    try:
        # Lee en formato byte
        file = open(myfile, 'wb')
        print(f'Writing {len(data)}b of data')
        file.write(data)
        file.close()

        header = 'HTTP/1.1 201 OK\r\n'

        x = datetime.datetime.now()
        header += f'Date: {x.strftime("%a, %d %b %Y %X %Z")}\r\n'

        server = 'Python-Sockets/1.0 (Ubuntu)'
        header += f'Server: {server}\r\n'

        #header += f'Content-Length: {file_len}\r\n'
 
        mimetype = 'text/html'
        header += 'Content-Type: ' + str(mimetype) + '\r\n\r\n'

        #response = '<html><body>201: OK</body></html>'
    except Exception as e:
        header = 'HTTP/1.1 403 Forbidden \r\n\r\n'
        #response = '<html><body>Error 403: Forbidden</body></html>'

    print(' '*21, 'RESPONSE', ' '*21)
    
    final_response = header.encode('utf-8')
    print(header)
    return final_response

def head(r_header, r_data):
    string_list = r_header.split(" ")
    method = string_list[0]
    requesting_file = string_list[1]

    print('*'*51)
    print(' '*21, 'REQUEST', ' '*21)
    print(f'{r_header}\r\n')


    myfile = requesting_file.split("?")[0]
    myfile = myfile.lstrip("/") # Remueve ese caracter

    if(myfile == "" or myfile == "/"):
        myfile = "index.html"

    print('*'*51)
    #print('myfile: '+str(myfile))
    try:
        # Lee en formato byte
        file = open(myfile, 'rb')
        response = file.read()
        file_len = len(response)
        file.close()

        header = 'HTTP/1.1 200 OK\r\n'

        x = datetime.datetime.now()
        header += f'Date: {x.strftime("%a, %d %b %Y %X %Z")}\r\n'

        server = 'Python-Sockets/1.0 (Ubuntu)'
        header += f'Server: {server}\r\n'

        header += f'Content-Length: {file_len}\r\n'

        if myfile.endswith('.jpg') or myfile.endswith('jpeg'):
            mimetype = 'image/jpeg'
        elif (myfile.endswith('.gif')):
            mimetype = 'image/gif'
        elif (myfile.endswith('.csv')):
            mimetype = 'text/csv'
        elif (myfile.endswith('.css')):
            mimetype = 'text/css'
        elif (myfile.endswith('.json')):
            mimetype = 'application/json'
        elif (myfile.endswith('.pdf')):
            mimetype = 'application/pdf'
        else: 
            mimetype = 'text/html'
        header += 'Content-Type: ' + str(mimetype) + '\r\n\r\n'
    except Exception as e:
        header = 'HTTP/1.1 404 Not Found \r\n\r\n'
        response = '<html><body>Error 404: File not found</body></html>'.encode('utf-8')

    print(' '*21, 'RESPONSE', ' '*21)
    print(header)
    
    final_response = header.encode('utf-8')
    return final_response