import socket


host = '127.0.0.1'
port = 8080

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

c.bind((host, port))

c.listen()

def procFile(fileName):
    file = open(fileName, 'rb')
    data = file.read()
    file.close()
    return data, fileName.split('.')[1]

def response(HTTPHeader, dataBody):
    try:
        headerStrList = HTTPHeader.split(' ')
        responsePackage = ""
    
        if (headerStrList[0] == "GET"):
            if (headerStrList[1] == '/'):
                data, fileType = procFile("index.html")
            else:
                data, fileType = procFile(headerStrList[1][1:].split('?')[0])
        elif (headerStrList[0] == "POST"):
            # username = "username=..." & password = "password=..."
            username = dataBody.split('&')[0]
            password = dataBody.split('&')[1]

            if (username[9:] == "admin" and password[9:] == "admin"):
                data, fileType = procFile("info.html")

        header = "HTTP/1.1 200 OK\n"

        if (fileType == "jpg"):
            mimetype = "image/jpg"
        elif (fileType == "css"):
            mimetype = "text/css"
        else:
            mimetype = "text/html"

        header = header + mimetype + "\n\n"
        responsePackage = header.encode('utf-8')
        responsePackage += data

    except Exception as e:
        header = "HTTP/1.1 404 Not found\n\n"
        data = procFile("404notfound.html")[0]
        responsePackage = header.encode('utf-8') + data
    
    return responsePackage

def connectionLoop():
    while True:
        connection, address = c.accept()
        req = connection.recv(1024).decode('utf-8')

        HTTPRequestLines = req.split('\n')

        HTTPHeader = HTTPRequestLines[0]
        dataBody = HTTPRequestLines[-1]

        print(HTTPHeader)
        print(dataBody)

        responsePackage = response(HTTPHeader, dataBody)
        connection.send(responsePackage)

        connection.close()


if __name__ == "__main__":
    connectionLoop()