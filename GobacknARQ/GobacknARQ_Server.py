import sys
import socket
import struct
import time
import random

def parsePacket(packet):
	header = packet[0:8]
	data = packet[8::]

	sequenceNum = struct.unpack('=I',header[0:4])
	windowSize = struct.unpack('=h',header[4:6])
	checksum = struct.unpack('=H',header[6:8])

	return sequenceNum, windowSize, checksum, data

def calcchecksum(data, checksum):
	sum = 0

	for i in range(0, len(data), 2):
		if i+1 < len(data):
			data16 = ord(data[i]) + (ord(data[i+1])) << 8
			interSum = sum + data16
			sum = (interSum & 0xffff) + (interSum >> 16)
	currChk = sum & 0xffff

	result = currChk & checksum
	if result == 0:
		return True
	else:
		return False

UDP_IP = ""
UDP_PORT = 4363

bufferSize = 1030
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((UDP_IP, UDP_PORT))
print "ready for client..."


sequence = 0
sequenceSize = 8
windowSize = 4
receiveFrame = [None,None,None,None] 
retransack = []

filesize,addr = sock.recvfrom(bufferSize)
f = open('test.pdf','wb')
cnt = 0
while True:
	windowIndex = 0
	receiveFrame = [None,None,None,None]
	while windowIndex < windowSize:

		packet, addr = sock.recvfrom(bufferSize)
		if packet == "finish":
			sock.close()
			f.close()
			sys.exit()
		sequenceNum, windowNumber, checksum, data = parsePacket(packet)
		
		#a  = random.randint(0,5)
		if calcchecksum(data, int(checksum[0])) is True:
			receiveFrame[int(windowNumber[0])] = data
		windowIndex = windowIndex + 1

	for index in range(0,len(receiveFrame)):
		if receiveFrame[index] is not None:
			sock.sendto(str(index) + "ACK",addr)

	while True:
		require ,addr = sock.recvfrom(bufferSize)
		
		if require[0] == 'r':
			count = require[-1]
		elif require[0] =='d':
			break
		
		for index in range(0,int(count)):
			data, addr = sock.recvfrom(bufferSize)
			sequenceNum, windowNumber, checksum, data = parsePacket(data)
			if calcchecksum(data, int(checksum[0])):
				receiveFrame[int(windowNumber[0])] = data
				sock.sendto(str(windowNumber[0]) + "ACK",addr)
		if receiveFrame.count(None) is 0:
			break

	for i in range(0,len(receiveFrame)):

		f.write(receiveFrame[i])
		cnt = cnt + int(len(receiveFrame[i]))
		print "%d / %d (current size / total size), %.2f %%" % (cnt, int(filesize), float((cnt * 100) / float(filesize)))
		if cnt == filesize :
		 break
f.close()
sock.close()
sys.exit()
