import socket
from socket import timeout
from check import ip_checksum
import sys
#from threading import Thread
#import thread
from thread import *
HOST = ''     #my addr
PORT = 3502   #my port

DEST_HOST = ''
DEST_PORT = 2222

try:
	#create an AF_INET, STREAM socket (UDP)
	recv_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	send_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit()
    
print 'Send/Recieve Socket Created'
#~ s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    recv_sock.bind((HOST, PORT))
    #~ send_sock.bind((HOST,LISTEN_PORT))
except socket.error, msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit()

print 'Socket Bind Complete'
recv_sock.settimeout(1)

print 'Socket now listening...'

curr_seq = 0

def is_ACK(rcvpkt, expected_seq):
    if (str(rcvpkt[0]) == str(expected_seq)):
		return True
	#~ print "recieved seq: %s" %rcvpkt[0]
	#~ print "expected seq: %s" %expected_seq
	#~ print "Warning Machines in differing states?"
    return False

def notcorrupt(rcvpkt):
	
	message = rcvpkt.rsplit(None,1)[-2][1:]
	expected_checksum = rcvpkt.rsplit(None,1)[-1]#last element in rcvpkt is checksum

	if (expected_checksum == ip_checksum(message)):
		return True
	
	#For debugging purposes
	#~ print "Apparent data: " + message
	#~ print "Expected checksum: " + expected_checksum
	#~ print "Calculated checksum: " + ip_checksum(message)
	
	return False

    
def rdt_send(data, seq):
	sndpkt = str(seq) + data + " " + ip_checksum(data)
	
	#For debuggin purposes
	#~ print str(seq)
	#~ print data
	#~ print ip_checksum(data)
	
	send_sock.sendto(sndpkt,(DEST_HOST,DEST_PORT))
	return True

def rdt_rcv ():
    try:
        rcvpkt, addr = recv_sock.recvfrom(1024)
    except timeout:
        print "Timeout... resending data"
        rdt_send(data, curr_seq)
        return rdt_rcv()
    else:
        print "Message received:"
        if (notcorrupt(rcvpkt) and is_ACK(rcvpkt, curr_seq)): #everything is OK
            print rcvpkt
            return True
	print "uwotm8"
    return False

temp = 0
while 1:
    
    ACK = False;
    
    while not ACK:
        data = raw_input("type a message to send: ")
        rdt_send(data, curr_seq)
        if (rdt_rcv()): #if we got a message correctly
            ACK = True
            #If you want to end prematurely
            #~ if (temp == 2):
                #~ send_sock.close()
                #~ recv_sock.close()
                #~ sys.exit()
    curr_seq = 1 - curr_seq #alternate the seq



send_sock.close()
recv_sock.close()
sys.exit()
