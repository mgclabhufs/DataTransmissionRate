from rawsocketpy import RawSocket , to_str, get_hw, to_bytes
import time
from multiprocessing import Process
import threading
import os
import numpy as np
import cv2
import base64


def send_msg(interface, network, performance,Uid ,msg):
    sock = RawSocket(interface, 0xEEFA)
    sock.Uid = Uid
    if msg=='Discover':
        sock.send(to_str(len(msg)).ljust(64))
        sock.send(msg)
        print('\n'+interface+' send: '+msg)
        packet = sock.recv()
        print("Discover-- "+interface+": "+to_str(packet.src))    
    elif msg == 'exit':
        sock.send(msg)
        print('\n'+interface+' send: '+msg)
    else:
        Dmsg = Divide_msg(interface, network, performance, msg)
        sock.send(to_str(len(Dmsg)).ljust(64))
        sock.sendall(Dmsg)
        print('\n'+interface+' send: '+Dmsg)

def send_img(interface, network, performance,Uid ,img):
    sock = RawSocket(interface, 0xEEFA)
    sock.Uid = Uid 
    Bimg = base64.b64encode(cv2.imencode('.jpg',img)[1]).decode('utf-8')
    Dimg = Divide_msg(interface, network, performance, Bimg)
    sock.send(to_str(len(Dimg)).ljust(64))
    sock.sendall(to_bytes(Dimg))
    print('\n'+interface+' send: ',end='')
    print(to_bytes(Dimg))
    print('done')

def Divide_msg(interface, network, performance, msg):
    for i in range(len(network)):
        if interface == network[i]:
            start = int(len(msg)*(sum(performance[:i])/sum(performance)))
            end = int(len(msg)*(sum(performance[:i+1])/sum(performance)))
            break
    Dmsg = msg[start:end]
    return Dmsg

def find_network():
    stream = os.popen('ifconfig -s').read().split('\n')
    network = []
    for i in range(len(stream)-1):
        re = stream[i].split(' ')
        #In Resberry
        if re[0]=='Iface' or re[0]=='lo':
            continue
        network.append(re[0])
    return network

def net_pf(network):
    performance = []
    for i in range(len(network)):
        performance.append(50)
    return performance

def Unique_id(network):
    mac = []
    for i in range(len(network)):
        mac.append(to_str(get_hw(network[i])))
    print(mac)
    return mac[0]

def main():
    network = find_network()
    performance = net_pf(network)
    #test
    #network = ['eth0', 'wlan0']
    #performance = [10,1]
    Uid = Unique_id(network)
    #first Discover server MAC Address
    procs = []
    print(network)
    for interface in network:
        proc = threading.Thread(target=send_msg, args=(interface, network, performance,Uid, 'Discover' ,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    while True:
        msg = input("\nEnter send message : ")
        procs = []
        if msg == 'send img':
            img = input('Enter img file name :  ')
        for interface in network:
            if msg=='send img':
                #try:
                #    img = cv2.imread(img+'.jpg',cv2.IMREAD_COLOR)
                #except:
                #    img = np.full((100,100,3),(255,0,255),dtype=np.uint8)
                img = np.full((1000,1000,3),(255,0,255),dtype=np.uint8)
                proc = threading.Thread(target=send_img, args=(interface, network, performance, Uid, img ,))
            else:
                proc = threading.Thread(target=send_msg, args=(interface, network, performance, Uid, msg ,))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

        if msg=='exit':
            print("\nExit Program")
            break


if __name__ == '__main__':
    main()


