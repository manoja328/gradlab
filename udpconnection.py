
import socket
import time
import numpy as np
import matplotlib.pyplot as plt

UDP_IP = "169.254.185.14"
UDP_PORT = 30444

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
print ("---socket made -----")
sock.connect((UDP_IP, UDP_PORT))
print ("---connection established ----")

sock.send(b"Bind HTPA series device")
time.sleep(1)
sock.send(b"k")

for i in range(10):
    data = sock.recv(1283)


sock.send(b"M")
time.sleep(1)
sock.send(b"K")

xx = np.zeros((10,641),dtype=np.uint16)

#%%
#sock.send(b"X")  #to stop data collection

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
            x[i]=data[k+1]+256*data[k+2]
        xx[frame-1]=x

datastream = xx.ravel()
image = datastream[:5120]      
img=np.reshape(image,(64,80))
plt.imshow(img)
plt.axis('off')
plt.show()
    

#%%    
#while True:
#     try:
#         data = sock.recv(1283)
#         print (data)
#     except KeyboardInterrupt:
#         break


