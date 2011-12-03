pass

if __name__ == '__main__':
    from socket import *
    clientsock = socket(AF_INET, SOCK_STREAM)
    clientsock.connect(('',8000))
    clientsock.send('hello')