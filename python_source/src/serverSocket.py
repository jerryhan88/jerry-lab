pass

if __name__ == '__main__':
    from socket import *
    svrsock = socket(AF_INET, SOCK_STREAM)
    svrsock.bind(('',8000))
    svrsock.listen(1)
    conn, addr = svrsock.accept()
    