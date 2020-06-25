import socket


host = '127.0.0.1'
port = 8080

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

c.bind((host, port))

c.listen(1)

def Open_File(file_name):
    try:
        file = open(file_name, 'rb')  # open file , r => read , b => byte format
        response = file.read()
        file.close()

        header = 'HTTP/1.1 200 OK\n'

        if (myfile.endswith(".jpg")):
            mimetype = 'image/jpg'
        elif (myfile.endswith(".css")):
            mimetype = 'text/css'
        else:
            mimetype = 'text/html'

        header += 'Content-Type: ' + str(mimetype) + '\n\n'

    except Exception as e:
        file = open('404notfound.html', 'rb')  # open file , r => read , b => byte format
        response = file.read()
        file.close()

        header = 'HTTP/1.1 200 OK\n'
        mimetype = 'text/html'
        header += 'Content-Type: ' + str(mimetype) + '\n\n'

    final_response = header.encode('utf-8')
    final_response += response
    return final_response



while True:
    connection, address = c.accept()
    req = connection.recv(1024).decode('utf-8')
    string_list = req.split(' ')  # Split request from spaces

    method = string_list[0]  # First string is a method
    requesting_file = string_list[1]  # Second string is request file

    login_info = ''
    if(method == "POST"):
        login_info = string_list[-1]

    myfile = requesting_file.split('?')[0]  # After the "?" symbol not relevent here
    myfile = requesting_file.lstrip('/')    # Remove "/"

    if (myfile == ''):
        myfile = 'index.html'  # Load index file as default

    # Check in formation when login
    if(login_info.find("username") == 39):
        # Slip username and password
        check_split = login_info.split('\r')
        check_split = check_split[-1]
        check_split = check_split.split('=')
        password = check_split[-1]
        check_split = check_split[1].split('&')
        username = check_split[0]

        # Check whether login is right
        if(username == "admin" and password == "admin"):
            myfile = 'info.html'
        else:
            myfile = '404notfound.html'

#        print(username)
#        print(password)

    # Check whether having download files request?
    if(myfile.find("files") == 0):
        myfile = myfile.split('?')[0]

    final_response = Open_File(myfile)
    connection.send(final_response)
    connection.close()