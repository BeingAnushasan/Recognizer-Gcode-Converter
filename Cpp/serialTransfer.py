
#======================================

def recvFromArduino():
    global startMarker, endMarker
    
    ck = ""
    x = "z" # any value that is not an end- or startMarker
    byteCount = -1 # to allow for the fact that the last increment will be one too many
    
    # wait for the start character
    while  ord(x) != startMarker:
        x = ser.read()
    
    # save data until the end marker is found
    while ord(x) != endMarker:
        if ord(x) != startMarker:
            ck = ck + x.decode("utf-8") # change for Python3
            byteCount += 1
        x = ser.read()
    
    return(ck)


#============================

def waitForArduino():

    # wait until the Arduino sends 'Ok' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded
    
    global startMarker, endMarker
    
    msg = ""
    while msg.find("Arduino is ready") == -1:

        while ser.inWaiting() == 0:
            pass
        
        msg = recvFromArduino()

        print (msg) # python3 requires parenthesis
        print ()
        
#======================================


import serial
import time

print ()
print ()

# NOTE the user must ensure that the serial port and baudrate are correct
# serPort = "/dev/ttyS80"
serPort = "COM4"
baudRate = 115200
ser = serial.Serial(serPort, baudRate)
print ("Serial port " + serPort + " opened  Baudrate " + str(baudRate))

startMarker = 60
endMarker = 62

file = open('input.txt')
waitForArduino()
waitingForReply = False  

while 1:
    
    line = file.readline()
    if not line:
       break
    
    if waitingForReply == False:
       waitingForReply = True
       ser.write(str.encode(line))
       print ("reading file and writing line to arduino  " +  line)
      
      
    if waitingForReply == True:
       print ("waiting for reply")
       while ser.inWaiting() == 0:
           pass
        
       dataRecvd = recvFromArduino()
       print ("Reply Received  " + dataRecvd)
       waitingForReply = False

       print ("===========")

    time.sleep(5)

      
      
file.close
print ('file closed')
print
ser.close
print ('serial closed')