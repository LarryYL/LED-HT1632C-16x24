import RPi.GPIO as GPIO
from time import sleep
import math

CS = 3
DATA = 5
WRITE = 7

SYSON = '100000000010'
LEDON = '100000000110'
BLINK = '100000010010'
LEDOFF = '100000000100'
SYSOFF = '100000000000'
SYSSET = '100001001000'
write = '101'



GPIO.setmode(GPIO.BOARD)

GPIO.setup(DATA,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(CS,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(WRITE,GPIO.OUT,initial=GPIO.HIGH)

def Tobin(inter,digit):
	raw = bin(inter)
	raw = raw[2:]
	if len(raw) != int(digit):
		no = int(digit - len(raw))
		zeros = '0' * no
		raw = zeros + raw
	return raw

def sendString(bitString,auto=True):
	if auto:
		GPIO.output(CS,GPIO.LOW)
	for bit in bitString:
		bit = int(bit)
		GPIO.output(WRITE,GPIO.LOW)
		if bit:
			GPIO.output(DATA,GPIO.HIGH)
		else:
			GPIO.output(DATA,GPIO.LOW)
		GPIO.output(WRITE,GPIO.HIGH)
	GPIO.output(DATA,GPIO.HIGH)
	if auto:
		GPIO.output(CS,GPIO.HIGH)

def beaMap(x,y):
	if x<0 or x>23 or y<0 or y>15:
		raise ValueError('Pixel out of range!')
	
	colSkip = y/8
	rowSkip = x/8
	
	if (x/4)%2 == 0:
		ori = 0
	else:
		ori = 1
	
	if colSkip == 0:
		address = ori + rowSkip*(16*2) + y*4 + colSkip*2
	else:
		address = ori + rowSkip*(16*2) + (y-8)*4 + colSkip*2
	binAdd = Tobin(address,7)
	append = x%4
	if append == 0:
		appendBin = '1000'
	if append == 1:
		appendBin = '0100'
	if append == 2:
		appendBin = '0010'
	if append == 3:
		appendBin = '0001'

	outputStr = '101' + binAdd + appendBin	
	return outputStr

def reset():
	add = 0
	GPIO.output(CS,GPIO.LOW)
	sendString('101'+Tobin(add,7)+'0000'*96)		
	GPIO.output(CS,GPIO.HIGH)

	
try:
	sendString(SYSON)
	sendString(SYSSET)
	sendString(LEDON)
	sleep(0.5)
	reset()
	while True:
		'''
		for y in range(0,16):
			for x in range(0,24):
				mem = beaMap(x,y)
				print mem
				sendString(mem)
				sleep(0.1)
				reset()

		'''
		
		mem1 = beaMap(5,5)
		mem2 = beaMap(5,6)
		mem3 = beaMap(5,7)
		mem4 = beaMap(5,8)
		mem5 = beaMap(5,9)
		mem7 = beaMap(5,10)
		mem8 = beaMap(5,11)
		mem9 = beaMap(5,12)
		mem6 = beaMap(5,13)
		
		memList=[]
		for y in range(1,10):
			mem = beaMap(5,y)
			memList.append(mem)
		for item in memList:
			sendString(item)
		
		
		'''
		for x in range(3):
			mem = beaMap(x,3)
			memList.append(mem)
		for item in memList:
			sendString(item)
		
		sendString(mem1)
		sendString(mem2)
		sendString(mem3)
		sendString(mem4)
		sendString(mem5)
		sendString(mem6)
		sendString(mem7)
		sendString(mem8)
		sendString(mem9)
		'''
	
	'''
	start = 0
	while True:	
		binStart = Tobin(start,7)
		for address in ['1000','0100','0010','0001']:
			GPIO.output(CS,GPIO.LOW)
			sendString(write)
			sendString(binStart)
			sendString(address)
			GPIO.output(CS,GPIO.HIGH)
			sleep(0.1)			
		GPIO.output(CS,GPIO.LOW)
		sendString(write)
		sendString(binStart)
		sendString('0000')
		GPIO.output(CS,GPIO.HIGH)
			
		if start == 96:
			start = 0
		else:
			start += 1
	'''

except KeyboardInterrupt:
	sendString(LEDOFF)
	sendString(SYSOFF)
	GPIO.cleanup()
