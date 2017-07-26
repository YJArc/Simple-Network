import socket
from check import ip_checksum
import sys
#from threading import Thread
#import thread
from thread import *
HOST = ''     #dest addr
PORT = 2222   #dest port

DEST_HOST = ''
DEST_PORT = 3502

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

print 'Socket now listening...'
oncethru = 0

def has_seq(rcvpkt, expected_seq):
	if (str(rcvpkt[0]) == str(expected_seq)):
		return True
	
	print "recieved seq: %s" %rcvpkt[0]
	print "expected seq: %s" %expected_seq

	print "Machines in differing states? Possible duplicate?"
	return False
    
def notcorrupt(rcvpkt):
	
	message = rcvpkt.rsplit(None,1)[-2][1:]
	expected_checksum = rcvpkt.rsplit(None,1)[-1]#last element in rcvpkt is checksum
	
	if (expected_checksum == ip_checksum(message)):
		return True
	
	print "Warning: received corrupted data. Dumping data [no ACK sent]"
	#For debugging purposes
	#~ print "Apparent data: " + message
	#~ print "Expected checksum: " + expected_checksum
	#~ print "Calculated checksum: " + ip_checksum(message)
	
	return False

def rdt_send(data, seq): #sends from receiver will always look like 0ACK checksum
    sndpkt = str(seq) + data + " " + ip_checksum(data)
    send_sock.sendto(sndpkt,(DEST_HOST,DEST_PORT))
    return True


seq = 0
while 1:
    rcvpkt, address = recv_sock.recvfrom(1024)
    if (notcorrupt(rcvpkt)):
        rdt_send("ACK", seq)
        if (has_seq(rcvpkt, seq)):
            print "Message recieved: "
            print "    " + rcvpkt.rsplit(None,1)[-2][1:]
            
            seq = 1 - seq
            #~ temp += 1
            
            #~ if(temp == 3):  #not sure if end connection prematurely or continue
                #~ print "Did we make it here?"
                #~ send_sock.close()
                #~ recv_sock.close()
                #~ sys.exit()
                
        else:
            rdt_send("ACK",1-seq)




send_sock.close()
recv_sock.close()
sys.exit()
