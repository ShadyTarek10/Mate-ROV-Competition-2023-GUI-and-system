import serial.tools.list_ports
from multiprocessing.connection import Client as cli
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portList= []
for onePort in ports:
    portList.append(str(onePort))
    # print(str(onePort))

    
for x in range(0,len(portList)):
    if portList[x].startswith("COM10"):
        portVar="COM10"
        # print(portList[x])

serialInst.baudrate = 9600
serialInst.port= "COM10"
serialInst.open()



adrrgui=('localhost',4000)
clientgui=cli(adrrgui,authkey=b'123')
while True:
    if serialInst.in_waiting:
        packet = serialInst.readline()
        message=packet.decode('utf')
        clientgui.send(message)
        # print(message,end='')