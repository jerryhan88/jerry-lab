# -*- coding: cp949-*-

import socket
from SocketServer import ThreadingTCPServer, StreamRequestHandler
import thread

PORT = 8037
lock = thread.allocate_lock()

class Subscriber(object):
    def __init__(self, parent, name=''):
        self.parent = parent
        self.name =name
        self.sock = parent.reqest
    def setName(self, name):
        self.name = name
    def getName(self):
        return self.name
    def upload(self, msg):
        self.getParent().publisher.handleMessage(self, msg)
    def send(self, msg):
        self.parent.request.sendall(msg)
    def close(self):
        self.parent.request.shutdown(socket.SHUT_RD | socket.SHUT_WR)
        self.parent.request.close()
    def getParent(self):
        return self.parent
    
class Publisher(object):
    def __init__(self):
        self.subscribers = {}
        
    def addUser(self, user):
        if user.getName() in self.subscribers:
            user.send('이미 등록된 이름입니다.\n')
            return False
        lock.acquire()
        self.subscribers[user.getName()] = user
        lock.release()
        self.broadcastMessage('[' + user.getName() + '] ' + '님께서 입장하셨습니다\n')
        user.send('[%s]님 어서오세요. \n' % user.getName())
        print '%s joined' % user.getName()
        print len(self.subscribers), 'connections'
        return True
    
    def removeUser(self, name):
        if name not in self.subscribers:
            return False
        user = self.subscribers[name]
        user.send("연결을 종료합니다 \n")
        user.close()
        user.getParent().connectedFlag = False
        lock.acquire()
        del self.subscribers[name]
        lock.release()
        self.broadcastMessage('[' + name + '] ' + '님께서 나가셨습니다 \n')
        print '%s left' % name
        print len(self.subscribers), 'connections'
        return True
    
    def handleMessage(self, user, msg):
        if not msg.strip():
            return
        if not msg.startswith('/'):
            self.boradcastMessage('[' + user.getName() + '] ' + msg)
            return
        args = msg[1:].split()
        if hasattr(self, 'action_' + args[0]):
            getattr(self, 'action_' + args[0])(user.getName(), args[1:])
            
    def boradcastMessage(self, msg):
        for user in self.subscribers.values():
            user.send(msg)
            
    def action_quit(self, name, args):
        return self.removeUser(name)
    
class ChatRequestHandler(StreamRequestHandler):
    publisher = Publisher()
    
    def handle(self):
        print 'connection from', self.client_address
        try:
            user = self.readAndRegisterName()
            if not user : raise Exception
            self.connectedFlag = True
            data = self.rfile.readline()
            
            while data:
                user.upload(data)
                if not self.connectedFlag:
                    break
                data = self.rfile.readline()
        except socket.error:
            print 'Socket Error'
        except Exception, msg:
            pass
        print 'Disconnected from', self.client_address
        
        try:
            self.publisher.removeUser(user.getName())
        except: pass
        
    def readAndRegusterName(self):
        user = Subscriber(self)
        while 1:
            user.send('이름을 입력해주세요')
            try:
                name = self.rfile.readline().strip()
            except socket.error:
                user.close()
                return
            if not name or name.startwith('/'):
                user.send('잘못된 이름입니다.\n')
                continue
            if self.publisher.addUser(user):
                return user
            
class ChatServer(ThreadingTCPServer):
    allow_reuse_address = True
    
        
if __name__ == '__main__':
    server = ChatServer(("", PORT), ChatRequestHandler)
    print 'listening on port', PORT
    server.serve_forever()