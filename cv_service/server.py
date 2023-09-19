import socket

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(("127.0.0.1", 5000))
ss.listen()


while True:
    (clientConnected, clientAddress) = ss.accept()
    print("Accepted a connection request from %s:%s" % (clientAddress[0], clientAddress[1]))

    with open('output.png', 'wb') as img:
        while True:
            dataFromClient = clientConnected.recv(1024)
            if not dataFromClient:
                break
            img.write(dataFromClient)






