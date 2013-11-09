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

def beaMap(pixelList):
	
	strList = []
	for pixel in pixelList:
		x = pixel[0]
		y = pixel[1]
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
		strList.append(outputStr)
	
	prefixList = []
	indexList = []
	print strList
	for add in strList:
		prefix = add[0:10]
		prefixList.append(prefix)
	for prefix in prefixList:
		tempList = []
		for index,refPrefix in enumerate(prefixList):
			if prefix == refPrefix:
				tempList.append(index)
		indexList.append(tempList)
		
	addList = []	
	count = 0
	for item in indexList:
		prefix = prefixList[count]
		num1 = 0
		num2 = 0
		num3 = 0
		num4 = 0
		for index in item:
			strSuff = strList[index][-4:]
			if int(strSuff) == 1000:
				num1 = 1
			elif int(strSuff) == 100:
				num2 = 1
			elif int(strSuff) == 10:
				num3 = 1
			elif int(strSuff) == 1:
				num4 = 1
		suffix = '%s%s%s%s' %(num1,num2,num3,num4)
		add = prefix + suffix
		addList.append(add)
		
	return addList

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
	
	pixelList = []
	for x in range(5):
		for y in range(2):
			pixelList.append([x,y])
	memList = beaMap(pixelList)
	print memList
		

	for item in memList:
		sendString(item)

	
	
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
