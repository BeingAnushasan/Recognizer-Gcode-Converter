import time
import serial
ser = serial.Serial(port="COM4", baudrate=115200)
try:
	file=open('./gcodeOutput.gcode')
	temp=file.readlines()
	for l in temp:
		ser.write(l.encode())
		print(ser.readline())
except KeyboardInterrupt:
	print("Termination")