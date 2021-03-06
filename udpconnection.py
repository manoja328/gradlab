# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 11:04:48 2017

@author: gradlab
"""


import socket
import time
import numpy as np
import matplotlib.pyplot as plt
import cv2

#specify the ip address , the port is always same
UDP_IP = "169.254.185.14"
UDP_PORT = 30444

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
print ("---socket made -----")
sock.connect((UDP_IP, UDP_PORT))
print ("---connection established ----")

#command must be send in the following format in order
sock.send(b"Bind HTPA series device")
time.sleep(1)
sock.send(b"k")

#initial data may contain junk
datainit=[]
for i in range(10):
    datainit.append(sock.recv(1283))


sock.send(b"M")
time.sleep(1)
#send coninuous frames from camera
sock.send(b"K")

xx = np.zeros((10,641),dtype=np.uint16)

#%%

#data received in 10 frames in length of 1283
#data is in 16 bit format 
#the image data is first 5120 (80*64) numbers
while True: 
    try:
        frame=0
        while frame <10:
            data = sock.recv(1283)
            #print (data[:100])
            frame = data[0]
            #print ("frame no:",frame)
            if len(data) == 1283:
                x=np.zeros(641,dtype=np.uint16)
                for i in range(len(x)):
                    k=i*2
                    #little endian format 
                    x[i]=data[k+1]+256*data[k+2]
                xx[frame-1]=x
        
        datastream = xx.ravel()
        image = datastream[:5120] 
        offsets=datastream[5120:6400]
        vdd=datastream[6400]
        tamb=datastream[6401]
        ptat=datastream[6402:]
        img=np.reshape(image,(64,80))
        #temperature data is in kelvin multiplied by 10 
        max_temp = np.max(img/10.0 - 273)
        min_temp = np.min(img/10.0 - 273)
        print("Max: %f C  Min: %f C"%(max_temp,min_temp))
        #change 16bit to 8bit image
        res=256*(img - img.min())/(img.max() - img.min())
        r=np.uint8(res)
        imgresized = cv2.resize(r,(400,400))
        #apply color map for better visualization
        colormapped_img=cv2.applyColorMap(imgresized,cv2.COLORMAP_JET)
        cv2.imshow("image",colormapped_img)
        if cv2.waitKey(1) & 0xFF == 27:
            sock.send(b"X")  #to stop data collection
            sock.close()
            cv2.destroyAllWindows()
            break
    except KeyboardInterrupt:
            sock.send(b"X")  #to stop data collection
            sock.close()
            cv2.destroyAllWindows()
            break
    
    #plt.imshow(img)
    #plt.axis('off')
    #plt.show()
    

#%%    
#while True:
#     try:
#         data = sock.recv(1283)
#         print (data)
#     except KeyboardInterrupt:
#         break


