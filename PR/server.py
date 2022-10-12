import socket
s = socket.socket()
print('Socket successfully created')
port = 8080
s.bind(('127.0.0.1', port))
print(f'socket binded the port{port}')
s.listen(5)
print('Socket is listening')
while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    message = 'Thank you for connecting'
    c.send(message.encode())
    c.close()

