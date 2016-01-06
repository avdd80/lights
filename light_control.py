from   socket      import *

BUFSIZE = 32
MY_PORT = 10000
MY_LISTENING_ADDR = ('', MY_PORT)

udp_recv_client = socket( AF_INET,SOCK_DGRAM)
udp_recv_client.setsockopt (SOL_SOCKET, SO_REUSEADDR, 1)
udp_recv_client.bind (MY_LISTENING_ADDR)

while True:
    # Blocking call
    data = udp_recv_client.recv(BUFSIZE)
    
    print data