import socket
import os
import time
import math


host = '127.0.0.1'
print("Server dang duoc chay o IP: " + str(host) + ", port: 8080")
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

def responseGET(path):
    if (path == '/'):
        data, fileType = procFile("index.html")

    elif (path.find('.') == -1 or path == "/files.html?"):
        if (path == "/files.html?"):
            path = "/data"
        files = [f for f in os.listdir(path[1:])]

        data, fileType = procFile("files.html")
        
        for file in files:
            filePath = path[1:] + '/' + file
            timeStr = time.ctime(os.path.getatime(filePath))
            size = os.path.getsize(filePath)
            index = data.find(b"</pre>\r\n    <hr>")

            for i in range(35 - len(file)):
                timeStr = " " + timeStr
            
            if (size == 0):
                sizeStr = "&lt;dir&gt"
            else:
                digitNum = math.floor(math.log10(size))
                if (digitNum < 3):
                    digitNum = 0
                    sizeStr = "B"
                elif (digitNum < 6):
                    digitNum = 3
                    sizeStr = "KB"
                elif (digitNum < 9):
                    digitNum = 6
                    sizeStr = "MB"
                elif (digitNum < 12):
                    digitNum = 9
                    sizeStr = "GB"
                size = size / (10 ** digitNum)
                sizeStr = "{:.1f}".format(round(size, 1)) + sizeStr

            data = data[:index] + bytes("     <a href=\"" + filePath + "\">" + file + "</a>" + timeStr + "  " +  sizeStr + "\r\n    ", 'utf-8') + data[index:]
            fileType = " "
    else:
        data, fileType = procFile(path[1:].split('?')[0])

    return data, fileType

def responsePOST(dataBody):
    # username = "username=..." & password = "password=..."
    username = dataBody.split('&')[0]
    password = dataBody.split('&')[1]

    if (username[9:] == "admin" and password[9:] == "admin"):
        data, fileType = procFile("info.html")

    return data, fileType

def response(HTTPHeader, dataBody):
    try:
        headerStrList = HTTPHeader.split(' ')
        responsePackage = ""
    
        if (headerStrList[0] == "GET"):
            data, fileType = responseGET(headerStrList[1])
        elif (headerStrList[0] == "POST"):
            data, fileType = responsePOST(dataBody)

        header = "HTTP/1.1 200 OK\n"

        if (fileType == "jpg" or fileType == "png" or fileType == "jpeg"):
            mimetype = "image/" + fileType
        elif (fileType == "css"):
            mimetype = "text/css"
        else:
            mimetype = "text/html"

        header = header + mimetype + "\n\n"
        responsePackage = header.encode('utf-8')
        responsePackage += data

    except Exception as e:
        print(e)
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

        # print(HTTPHeader)
        # print(dataBody)

        responsePackage = response(HTTPHeader, dataBody)
        connection.send(responsePackage)

        connection.close()


if __name__ == "__main__":
    connectionLoop()
