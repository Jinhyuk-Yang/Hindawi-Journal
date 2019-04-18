import os
import sys
import socket

def openRegistrationInterface(IP, PORT, converter):
  while True:
    server_socket1 = socket.socket()
    server_socket1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket1.bind((IP, PORT))
    client_socket1, addr = server_socket.accept()
    print('DMS is connected to Security Controller')
    data = client_socket1.recv(1024)
    converter.registerNSF(data)

def request_nsf(IP, PORT, nsf_name):
  ADDR = (IP, PORT)
  client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    client_socket2.connect(ADDR)
    client_socket2.send(nsf_name)
  except Exception as e:
    print("%s:%s" % ADDR)
    sys.exit()

def receive_nsf_ip(IP, PORT):
  while True:
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(1024)
    data = data.split(",")
    os.system("sudo /home/ubuntu/confd-6.6/bin/netconf-console --host "+data[1]+" /home/ubuntu/"+data[0]+".xml > factor/ip.txt")


