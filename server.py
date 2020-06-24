import socket


host = '127.0.0.1'
port = 8080

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

c.bind((host, port))

c.listen(2)

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
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')

    final_response = header.encode('utf-8')
    final_response += response
    return final_response


while True:
    connection, address = c.accept()
    req = connection.recv(1024).decode('utf-8')
#    print(req)
    string_list = req.split(' ')  # Split request from spaces

    method = string_list[0]  # First string is a method
    requesting_file = string_list[1]  # Second string is request file
#    print(method)

#    print('Client request ', requesting_file)

    myfile = requesting_file.split('?')[0]  # After the "?" symbol not relevent here
    myfile = requesting_file.lstrip('/')
#    print(myfile)
#    print(requesting_file)

    if (myfile == ''):
        myfile = 'form2.html'  # Load index file as default

    if(myfile.find("?") == 0):
        check_split = myfile.split('=')
        password = check_split[2]
        check_split = check_split[1].split('&')
        username = check_split[0]
        if(username == "admin" and password == "admin"):
            myfile = 'profile.html'
        print(username)
        print(password)

    if(myfile.find("down") == 0):
        myfile = myfile.split('?')[0]

    print(myfile)



    final_response = Open_File(myfile)
#    print(final_response)
    connection.send(final_response)



    connection.close()