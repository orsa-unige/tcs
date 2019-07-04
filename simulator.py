import socket, threading
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 65432))
s.listen(1)
 
lock = threading.Lock()
 
welcome_message = 'Welcome to MUD\n1. Go west\n2. Open a window\n3. Quit\n'




def manage(data):
        keyval=data[1:].strip().replace("\r\n","").split("=")
        print(keyval)

        response=keyval
    
        if keyval[0].strip()=="set pointing.track":
                if keyval[1].strip()=='0':
                        response='ciao'
                elif keyval[1].strip()=='1':
                        response='come'
                elif keyval[1].strip()=='2':
                        response='stai'
                else :
                        response='bene'                   
        else:
                response='other'
        
        return response
 
 
class daemon(threading.Thread):
 
    def __init__(self, (socket,address)):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
 
    def run(self):
 
        # display welcome message
        self.socket.send(welcome_message)
 
        while(True):
 
            # wait for keypress + enter
            data = self.socket.recv(1024)
 
            # handle menu alterantives and set proper return message
            if data[0] == '1':                
                data = manage(data)
            elif data[0] == '2':
                data = 'I feel a chilly wind\n'
            elif data[0] == '3':
                break;
            else:
                data = welcome_message
 
            # send the designated message back to the client
            self.socket.send(data);
 
        # close connection
        self.socket.close()
 
while True:
    daemon(s.accept()).start()


# From:
# https://grocid.net/2012/06/14/a-very-simple-server-telnet-example/
