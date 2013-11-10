import RPi.GPIO as GPIO
from time import sleep,strftime
import math
import numpy as np

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

zero = [[1,0],[2,0],[0,1],[3,1],[0,2],[3,2],[0,3],[3,3],[0,4],[3,4],[0,4],[3,4],[0,5],[3,5],[1,6],[2,6]]
one = [[2,0],[2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[1,1],[1,6],[3,6]]
two = [[0,6],[1,6],[2,6],[3,6],[1,0],[2,0],[0,1],[3,1],[3,2],[2,3],[1,4],[0,5]]
three = [[1,0],[2,0],[0,1],[3,1],[3,2],[1,3],[2,3],[3,4],[3,5],[0,5],[1,6],[2,6]]
four = [[2,0],[2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[1,1],[0,2],[0,3],[0,4],[1,4],[3,4]]
five = [[0,0],[0,1],[0,2],[0,3],[0,5],[1,0],[2,0],[3,0],[1,3],[2,3],[3,4],[3,5],[1,6],[2,6]]
six = [[1,0],[2,0],[3,1],[0,1],[0,2],[0,3],[0,4],[0,5],[1,3],[2,3],[3,4],[3,5],[1,6],[2,6]]
seven = [[3,0],[1,0],[2,0],[0,1],[0,2],[3,1],[3,2],[3,3],[3,4],[3,5],[3,6]]
eight = [[1,0],[2,0],[0,1],[3,1],[0,2],[3,2],[0,4],[3,4],[0,5],[3,5],[1,6],[2,6],[1,3],[2,3]]
nine = [[3,1],[3,2],[3,3],[3,4],[3,5],[0,5],[1,6],[2,6],[1,0],[2,0],[0,1],[0,2],[1,3],[2,3]]

numbers = np.array([zero,one,two,three,four,five,six,seven,eight,nine])


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
		count += 1
		
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
	'''
	addList = []
	for number in numbers:
	   memList = beaMap(number)
	   addList.append(memList)
	while True:
	    for memList in addList:
       	        for mem in memList:
        	       sendString(mem)
        	sleep(0.5)
        	reset()
	'''
        dateTimeLast = None
        while True:
            dateTime =  strftime('%H%M')
            if dateTime == dateTimeLast:
                continue     
            else:
                hr = dateTime[0:2]
                digit3 = dateTime[2]
                digit4 = dateTime[3]
                
                hr = str(int(hr) + 4)
                
                if len(hr) == 1: 
                	hr = '0' + str(hr)

                digit1 = hr[0]
                digit2 = hr[1]
                
                number1 = numbers[int(digit1)] + np.array([1,3])
                number2 = numbers[int(digit2)] + np.array([6,3])
                number3 = numbers[int(digit3)] + np.array([14,3])
                number4 = numbers[int(digit4)] + np.array([19,3])
                
                numberList = number1.tolist() + number2.tolist() + number3.tolist() + number4.tolist()
                memList = beaMap(numberList)
                reset()
                for add in memList:
                    sendString(add)
            
            dateTimeLast = dateTime
            sleep(0.5)
        
            
except KeyboardInterrupt:
	sendString(LEDOFF)
	sendString(SYSOFF)
	GPIO.cleanup()
