import socket
import sys
import getpass
import time
from thread import *

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 7244 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

userClient = []

#Start listening on socket
s.listen(10)
print 'Socket now listening'

user1MSG = []
user2MSG = []
user3MSG = []
user4MSG = []
onlineUsers = []
users = [['user1', 'test123'], ['user2', 'test1234'], ['user3', 'userthree'], ['user4', 'userfour']]
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    userClient.append(conn)
    #Sending message to connected client
    
    userMsgList = [['user1'], ['user2'], ['user3'], ['user4']]
    userListName = ''
    userListPass = ''

   #conn.sendall('Welcome to mini-Facebook. Please enter your username and password.')
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        conn.sendall('Username: ')
        username = conn.recv(1024)
        
        conn.sendall('Password: ')
        password = conn.recv(1024)

        for i in users:
            if username == i[0]:
                userListName = i[0]
                userListPass = i[1]
                userLoc = i
        if userListName != username or userListPass != password:
            continue
        
        conn.sendall('Login successful')
        time.sleep(0.2)

        if username == 'user1':
            unreadMessage = user1MSG
        elif username == 'user2':
            unreadMessage = user2MSG
        elif username == 'user3':
            unreadMessage = user3MSG
        else:
            unreadMessage = user4MSG
                
        while True:
            conn.sendall('Number of unread messages: ' + str(len(unreadMessage)) + '\nType 0 to logout\nType 1 to broadcast a message to all other users\nType 2 to change your password\nType 3 to send a private message to any other user\nType 4 to read all unread messages')
            userAction = conn.recv(1024)
            if userAction == '0':
                conn.sendall('You are now logged out and will be disconnected')
                conn.close()
                i = userClient.index(conn) #delete the user index after disconnected
                del userClient[i]
                break
            elif userAction == '1':
                conn.sendall('Type the message you would like to broadcast: ')
                broadcastMsg = conn.recv(1024)
                for j in userClient:
                    j.sendall('\nBroadcast message from another user: ' + broadcastMsg)
                    conn.recv(1024)
            elif userAction == '2':
                conn.sendall('Enter your current password: ')
                password = conn.recv(1024)
                if password == userListPass:
                    conn.sendall('Enter a new password: ')
                    userNewPass = conn.recv(1024)
                    userLoc[1] = userNewPass
                    conn.sendall('You have been signed out. Please enter your username and new password.')
                    break
            elif userAction == '3':
                conn.sendall('Who would you like to send a message to? ')
                userPM = conn.recv(1024)
                for i in userMsgList:
                    if i[0] == userPM:
                        conn.sendall('Type your message here: ')
                        userMes = conn.recv(1024)
                        sendMessage = 'Message from ' + username + ': ' + userMes
                        if userPM == 'user1':
                            user1MSG.append(sendMessage)
                            conn.sendall('Message Sent\n')
                            break
                        elif userPM == 'user2':
                            user2MSG.append(sendMessage)
                            conn.sendall('Message Sent\n')
                            break
                        elif userPM == 'user3':
                            user3MSG.append(sendMessage)
                            conn.sendall('Message Sent\n')
                            break
                        else:
                            user4MSG.append(sendMessage)
                            conn.sendall('Message Sent\n')
                            break
            elif userAction == '4':
                for i in unreadMessage:
                    conn.sendall(i + '\n')
                    conn.recv(1024)
                del unreadMessage[:]
                continue

                        
                        
    #came out of loop
    conn.close()

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))

s.close()
