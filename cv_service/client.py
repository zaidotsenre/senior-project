import socket

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect(('127.0.0.1', 5000))
img = ''
with open('input.png', 'rb') as f:
    img = f.read()
cs.send(img)

