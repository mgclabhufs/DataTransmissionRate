
from tkinter import OUTSIDE
from rawsocketpy import RawRequestHandler, RawAsyncServerCallback
import time
from rawsocketpy import get_hw, to_str, protocol_to_ethertype, to_bytes, to_int
from rawsocketpy import HashChaining
from multiprocessing import Process
import threading
import os
import cv2
import numpy as np
import base64

global dic
H= HashChaining(17)
dic={}

def callback(handler, server):
    #print("Testing")
    handler.setup()
    handler.handle()
    handler.finish()

def User_name(packet,data):
    OUI = to_int(to_str(packet.Uid[1:3]))
    UUA = to_int(to_str(packet.Uid[3:5]))
    return H.set_name(OUI,UUA,msg=data)    

def sum_msg(packet,user,data):
    global dic
    if packet.src == packet.Uid:
        dic={} 
    try:
        dic[user]+=data
    except:
        dic[user]=data 
    print(user + ' total == '+dic[user])
    if packet.src != packet.Uid:
        try:
            imgdata = base64.b64decode(dic[user])
            imgarr = np.frombuffer(imgdata, dtype=np.uint8)
            image = cv2.imdecode(imgarr, cv2.IMREAD_COLOR)
            cv2.imshow('image',image)
            cv2.waitKey(0)
        except:
            pass

class LongTaskTest(RawRequestHandler):
    def handle(self):
        time.sleep(1)

        data = self.packet.data.decode('utf-8').strip('\x00')
        user = User_name(self.packet,data)

        print(to_str(self.packet.src)+"-->"+ user)
        print(to_str(self.packet.Uid)+"--> Uid")
        print(user+' send:  '+data)
        if data!='Discover': sum_msg(self.packet, user,data)
        
    def finish(self):
        print("End\n")

    def setup(self):
        #print("Begin")
        pass 

def lets_start(interface):
    rs = RawAsyncServerCallback(interface, 0xEEFA, LongTaskTest, callback)
    rs.spin()    

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

def Unique_id(network):
    mac = []
    for i in range(len(network)):
        mac.append(to_str(get_hw(network[i])))
    print(mac)
    return mac[0]

def main():
    network = find_network()
    procs = []
    Uid = Unique_id(network)
    for interface in network:
       proc = threading.Thread(target=lets_start, args=(interface, ))
       procs.append(proc)
       proc.start()

    for proc in procs:
        proc.join()

if __name__ == '__main__':
    main()
