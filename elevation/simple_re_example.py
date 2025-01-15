from multiprocessing import Process
import socket
import sys
import threading

HOST = '127.0.0.1'
          #         .         .         .         .         .         .         .         .
          #123456789012345678901234567890123456789012345678901234567890123456789012345678901
cstring = '1100	51231	2022	AA	0,00	30.06.2021	05.07.2021	REF: 2633107	05.07.2021'
BUFF = len(cstring)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, 9999))

def func_b(cstring, sock):
    while True:
        message, address = sock.recvfrom(BUFF)
        sock.sendto(cstring.encode('utf-8'), address)

def func_a(cstring,sock,remote):
    while True:
        sock.sendto(cstring.encode('utf-8'), remote)
        message, address = sock.recvfrom(81)
        print(message.decode('utf-8'))

HOST = input('Remote IP: ')
p1 = Process(target=func_b,args=(cstring,sock,))
p2 = Process(target=func_a,args=(cstring,sock,HOST))
p1.start()
p2.start()
