import os
import socket
import sys
import time
import struct

def computeChecksum(data):
	sum = 0
	
	for i in range(0, len(data), 2):
		if i+1 < len(data):
			data16 = ord(data[i]) + (ord(data[i+1])) << 8
			interSum = sum + data16
			sum = (interSum & 0xffff) + (interSum >> 16)
	return ~sum & 0xffff

def formPacket(data, windowIndex, sequenceNum):
	seqNum = struct.pack('=I',sequenceNum)
	windowIndex = struct.pack('=h',windowIndex)
	checksum = struct.pack('=H',computeChecksum(data))
	packet = seqNum + windowIndex + checksum + data
	return packet

ServerIP = sys.argv[1]
ServerPORT = int(sys.argv[2])
filePath = sys.argv[3]
address = (ServerIP,ServerPORT)

if len(sys.argv) < 3:
	print "[Dest IP Addr] [Dest Port] [File Path]"
	sys.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sequenceSize = 8
sequenceNum = 0
windowSize = 4
bufferSize = 1024
filesize = int(os.path.getsize(filePath))
sock.sendto(str(filesize),address)

f = open(filePath,'rb')

data = f.read(bufferSize - 2)
cnt = 0
ack = None
readytransmission = []

while (data) :

	for index in range(0, windowSize):

		if readyretransmission[index] is None:
			packet = formPakcet(f.read(1024), windowIndex, seque
			readytransmission.append()
		
			cnt = cnt + len(data)
			print "%d / %d (current size / total size), %.2f %%" % (cnt, int(filesize), float((cnt*100) / float(filesize)))
		sock.sendto(readytransmission[index],address)
	
	for index in range(0,


	windowIndex = 0
	while windowIndex < windowSize:

		packet = formPacket(data, windowIndex, sequenceNum % 8)
		sock.sendto(packet, address)
		if data is not "":
			cnt = cnt + len(data)
			print "%d / %d (current size / total size), %.2f %%" % (cnt, int(filesize), float((cnt*100) / float(filesize)))
		data = f.read(bufferSize - 2)
		sequenceNum = sequenceNum + 1
		readyretransmission[int(windowIndex)] = packet
		windowIndex = windowIndex + 1

#cnt = cnt + len(data)
#print "%d / %d (current size / total size), %.2f %%" % (cnt, int(filesize), float((cnt*100) / float(filesize)))
	try:
		sock.settimeout(0.07)
		windowIndex = 0
		while True:
			frame = None
			frame,addr = sock.recvfrom(1024)
			windowNum = frame[0]
			
			if frame[1::] == "ACK":
				readyretransmission[int(windowNum)] = None	

			if readyretransmission.count(None) == 4:
				sock.sendto("dont retransmission...",address)
				break;

	except socket.error as e:
		print  e

		while True:
			if readyretransmission.count(None) is not 4:
				sock.sendto("retransmission.."+str(windowSize - readyretransmission.count(None)),address)
			else :
				break
			for index in range(0,len(readyretransmission)):
				if readyretransmission[index] is not None:
					sock.sendto(readyretransmission[index],address)
					try:
						sock.settimeout(0.1)
						ack = None
						ack, addr  = sock.recvfrom(1024)
						if ack is not None:
							readyretransmission[int(ack[0])] = None
							continue
							
					except socket.error as e:
					  print "retransmission",e, readyretransmission.count(None)
					  print index
					  continue
	continue
sock.sendto("finish",address)
f.close()
sock.close()
sys.exit()
