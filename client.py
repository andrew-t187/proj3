#Socket client example in python
import socket #for sockets
import sys    #for exit
import getpass

try:
    #creat an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

except socket.error:
    print 'Failed to create socket'
    sys.exit();

print 'Socket Created \n'

host = 'localhost';
port = 7244;

try:
    remote_ip = socket.gethostbyname(host)

except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exitiing'
    sys.exit();


s.connect((remote_ip, port))


#Sending data to remote server
message = "GET / HTTP/1.1\r\n\r\n"

while(1):
    reply = s.recv(4096)
    try:
        #Set the whole string
        if reply == 'Username: ':
            print reply
            userName = raw_input()
            s.sendall(userName)
        elif reply == 'Password: ':
            password = getpass.getpass()
            s.sendall(password)
        elif reply == 'Enter a new password: ':
            newPass = getpass.getpass(prompt = reply)
            s.sendall(newPass)
        elif reply == 'Enter your current password: ':
            currentPass = getpass.getpass(prompt = reply)
            s.sendall(currentPass)
        elif reply == 'Login successful' :
            print reply
            #print 'hit login'
            continue
        elif reply == 'Type the message you would like to broadcast: ':
            broadMsg = raw_input(reply)
            s.sendall(broadMsg)
        elif reply[0:4] == '\nBro':
            print reply
            continue
        elif reply == 'You have been signed out. Please enter your username and new password.':
            print reply
            continue
        elif reply[0:3] == 'Who':
            userPM = raw_input(reply)
            s.sendall(userPM)
        elif reply[0:12] == 'Message from':
            print reply
            continue
        elif reply == 'Message Sent\n':
            print reply
            continue
        elif reply == 'Type your message here: ':
            sendMsg = raw_input(reply)
            s.sendall(sendMsg)
        elif reply == 'You are now logged out and will be disconnected':
            print reply
            s.close()
            sys.exit()
        else:
            #print 'before acceptig user reply to'
            print reply
            #print 'accepting user reply to prompt'
            userAct = raw_input()
            s.sendall(userAct)
    

    except socket.error:
        #Send failed
        print 'Send failed'
        sys.exit()

s.close()
