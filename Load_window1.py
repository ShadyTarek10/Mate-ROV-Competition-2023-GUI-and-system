from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import subprocess
from threading import *
from multiprocessing.connection import Listener
from vidgear.gears import NetGear
from imutils import build_montages
import cv2
import pygame
from socket import *
from socket import socket
import socket
import struct
import pickle
import designer
import time
class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        #Load UI file
        uic.loadUi("window1.ui", self)
    
    


#self.pushButton_upward = self.findChild(QPushButton, "pushButton_upward")

      #  self.horizontalLayoutWidget_2=self.findChild(QWidget,"horizontalLayoutWidget_2")
        self.armed = 0
        self.deadZone= 0.05
        self.movement = 0
        self.mode = "MANUAL"
        self.grip = 1
        self.speed = 0
        self.docking_speed=1700
        self.stoping_speed=1500
        self.led =0
        self.can_grip = True
        self.prev_mov = False
        self.prev_pump = False
        self.pump=0
        self.prev_r1 = 0
        self.prev_led = 0
        self.prev_ps = 0
        self.radioButton_off_camera_options=self.findChild(QRadioButton,"radioButton_off_camera_options")
        #self.radioButton_off_camera_options =QRadioButton(clicked= lambda : self.presscam)
        self.radioButton_off_camera_options.clicked.connect(self.presscam)

        self.radioButton_on_camera_options=self.findChild(QRadioButton,"radioButton_on_camera_options")
        #self.radioButton_on_camera_options =QRadioButton(clicked= lambda : self.presscam)
        self.radioButton_on_camera_options.clicked.connect(self.presscam)


        self.checkBox_Autodocking=self.findChild(QCheckBox,"checkBox_Autodocking")
        # self.checkBox_Autodocking =QCheckBox(clicked= lambda : self.pressAutoDocking)
        self.checkBox_Autodocking.clicked.connect(self.pressAutoDocking)

        self.checkBox_joystick=self.findChild(QCheckBox,"checkBox_joystick")
        # self.checkBox_joystick =QCheckBox(clicked= lambda : self.JoyStick_Start)

        self.Camera_representation=self.findChild(QLabel,"Camera_representation")
        self.Camera_representation_2=self.findChild(QLabel,"Camera_representation_2")

        self.label_value_XACC=self.findChild(QLabel,"label_value_XACC")
        self.label_value_YACC=self.findChild(QLabel,"label_value_YACC")
        self.label_value_ZACC=self.findChild(QLabel,"label_value_ZACC")

        self.label_value_XGRO=self.findChild(QLabel,"label_value_XGRO")
        self.label_value_YGRO=self.findChild(QLabel,"label_value_YGRO")
        self.label_value_ZGRO=self.findChild(QLabel,"label_value_ZGRO")
        self.output_Textfloat=self.findChild(QLabel,"loutput_Textfloat")

        self.label_value_XMAG=self.findChild(QLabel,"label_value_XMAG")
        self.label_value_YMAG=self.findChild(QLabel,"label_value_YMAG")
        self.label_value_ZMAG=self.findChild(QLabel,"label_value_ZMAG")

        self.Startbtn_Timer=self.findChild(QPushButton,"Startbtn_Timer")
        self.pausebtn_Timer=self.findChild(QPushButton,"pausebtn_Timer")
        self.Resetbtn_Timer=self.findChild(QPushButton,"Resetbtn_Timer")
        self.rep_timer=self.findChild(QLabel,"rep_timer")

        self.pushButton_anticlockwise=self.findChild(QPushButton,"pushButton_anticlockwise")
        self.pushButton_left=self.findChild(QPushButton,"pushButton_left")
        self.pushButton_upward=self.findChild(QPushButton,"pushButton_upward")
        self.pushButton_forward=self.findChild(QPushButton,"pushButton_forward")
        self.pushButton_backward=self.findChild(QPushButton,"pushButton_backward")
        # self.pushButton_tilt=self.findChild(QPushButton,"pushButton_tilt")
        self.pushButton_clockwise=self.findChild(QPushButton,"pushButton_clockwise")
        self.pushButton_right=self.findChild(QPushButton,"pushButton_right")
        self.pushButton_downward=self.findChild(QPushButton,"pushButton_downward")
        self.pushButton_horizontal_gripper=self.findChild(QPushButton,"pushButton_horizontal_gripper")

        self.pushButton_pump=self.findChild(QPushButton,"pushButton_pump")
        self.pushButton_pump2=self.findChild(QPushButton,"pushButton_pump2")
        self.pushButton_speed=self.findChild(QPushButton,"pushButton_speed")
        self.pushButton_lift_back=self.findChild(QPushButton,"pushButton_lift_back")

        self.label_value_depth=self.findChild(QLabel,"label_value_depth")

        self.pushButton_ready=self.findChild(QPushButton,"pushButton_ready")

        self.pushButton_cureentmode=self.findChild(QPushButton,"pushButton_cureentmode")

        self.checkBox_joystick.clicked.connect(self.JoyStick_Start)
        












        # self.label_value_XACC.setText("-499")
        # fontXACC =QFont()
        # fontXACC.setPointSize(11)
        # fontXACC.setBold(True)
        # fontXACC.setWeight(75)
        # self.label_value_XACC.setFont(fontXACC)
        # #self.label_value_XACC.

        # self.label_value_YACC.setText("-499")
        # fontYACC =QFont()
        # fontYACC.setPointSize(11)
        # fontYACC.setBold(True)
        # fontYACC.setWeight(75)
        # self.label_value_YACC.setFont(fontYACC)

        # self.label_value_ZACC.setText("-499")
        # fontZACC =QFont()
        # fontZACC.setPointSize(11)
        # fontZACC.setBold(True)
        # fontZACC.setWeight(75)
        # self.label_value_ZACC.setFont(fontZACC)
        self.c=0
        self.c1=0
        self.seconds=0
        self.counter=0
        self.timer=QTimer()
        self.timer.setInterval(1000)
        self.Startbtn_Timer.clicked.connect(self.startTime)
        self.pausebtn_Timer.clicked.connect(self.stopTime)
        self.Resetbtn_Timer.clicked.connect(self.reset)
        self.timer.timeout.connect(self.showClock)
        self.manual=False
        self.depth_hold=False
        self.stabilize=False
        self.w=False
        self.counterGain=0
        self.gainRef=0
        self.Xgripper=False
        self.Ygripper=False
        self.XgripperCounter=0
        self.YgripperCounter=0
        self.flag_gripper=False
        self.dcv2=False
        self.camflag=False
        self.AutoDocking_Flag=False
        UI.keyPressEvent=self.keyPressEvent
        # self.SensorsThrd=Thread(target=self.jethandler)
        # self.SensorsThrd.start()
        # cmd='python OakClient.py'
        # self.cameraa=subprocess.Popen(cmd,shell=True)
        # cmd2='python floatReceiver.py'
        # p3=subprocess.Popen(cmd2,shell=True)
        # thread_float=Thread(target=self.Floathandler)
        # thread_float.start()
        












        self.show()



    def Floatinit(self):
        adrrgui=('localhost',4000)
        floatListener=Listener(adrrgui,authkey=b'123')
        self.floatconn=floatListener.accept()
        self.format="utf-8"
    def Floathandler(self):
        self.Floatinit()
        floatcounter=0
        ms=''
        while True:
            msg=self.floatconn.recv()
            print(msg)
        #     tmp = QtWidgets.QText
        #     print(type(msg))
        #     self.output_Textfloat.set
        #     self.output_Textfloat.setPlainText("jfhtd")
            msg=msg.split("\n")
            c+=1
        #     print(len(msg))
            if floatcounter<=4:
                ms+=msg[0]+'\n'
            else:
                # font = QtGui.QFont()
                # font.setPointSize(10)
                # font.setBold(True)
                # font.setWeight(50)
                # self.output_Textfloat.setFont(font)
                self.output_Textfloat.setText(ms)
                ms=msg[0]+'\n'
                floatcounter=1
    def pressAutoDocking(self):
        if self.checkBox_Autodocking.isChecked()==True:
                self.AutoDocking_Flag=True
                cmd='python AutoDocking.py'
                self.AutoDockingProcess=subprocess.Popen(cmd,shell=True)
                # self.SensorsThrd=Thread(target=self.jethandler)
                # self.SensorsThrd.start()
        elif self.checkBox_Autodocking.isChecked()==False:

             if self.AutoDocking_Flag==True:
                self.AutoDockingProcess.terminate()
                self.AutoDocking_Flag=False

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_L:
             self.led = not (self.led)
             
        # if self.led == 0:
        #      print("off") 
        # else : 
        #      print("on")
                 
            #  print("hello")
      




    def presscam(self):
        p2=None

        if (self.radioButton_off_camera_options.isChecked()):
            if self.camflag:
                print("fo22")
                # self.p2.terminate()
                # self.conn2.close()
                # del self.p2

                # self.tcam1.quit()
                print("ta7tt")
                #del self.tcam1
                self.camflag=False
                





        elif(self.radioButton_on_camera_options.isChecked()):
            print('7ansha8al el cameraa')
            self.camflag=True

            # cmd='python OakClient.py'
            # self.p2=subprocess.Popen(cmd,shell=True)
            self.tcam1=Thread(target=self.Camhandler1)
            self.tcam1.start()


    def caminit1(self):
    
            
        self.options = {"bidirectional_mode": False,"max_retries":1000,"jpeg_compression":False}

        self.client = NetGear(
        address="192.168.33.100",
        port="12345",
        protocol="tcp",
        pattern=1,
        receive_mode=True,
        logging=True,
        **self.options
        )


        # self.adrr = ('localhost', 17255)
        # self.lis = Listener(self.adrr, authkey=b'bsc')
        # print(self.adrr)
        # self.client = self.lis.accept()

    def Camhandler1(self):
        
            self.caminit1()

            while True:
                # try: 
                    #self.caminit1()
                    out = self.client.recv()
                    frame =out
                    frame= cv2.flip(frame, 0)
                    
                    frame= cv2.flip(frame, 1)
                    # address, frame = out
                    #     data = base64.b64decode(packet,' /')
                    #     npdata = np.fromstring(data,dtype=np.uint8)
                    #     frame = cv.imdecode(npdata,1)
                    #     frame = cv.flip(frame, 1)
                    converted = QImage(frame, frame.shape[1],
                        frame.shape[0], frame.shape[1] * 3,QImage.Format_RGB888).rgbSwapped()
                #     Pic = converted.scaled(640, 480, Qt.KeepAspectRatio)
                    # if self.radioButton_cam1.isChecked():
                    #     self.Cam1lbl.setPixself.map(QPixmap.fromImage(converted))
                    if self.radioButton_on_camera_options.isChecked():
                        #self.conn1.close()
                        self.Camera_representation_2.show()
                        #check momkn tkon frame
                        self.Camera_representation_2.setPixmap(QPixmap.fromImage(converted))
                    elif self.radioButton_off_camera_options.isChecked():
                        self.Camera_representation_2.close()
                        self.client.close()
                        #return
                # except:
                    #   print("####CAM CONNECTION PROBLEM#####")
                    #print("###CAM CONNECTION LOST###")


    # def jetinit(self):
    #     #PortCheck========================================================
    #     addr=('192.168.33.100',8500)
    #     l1=Listener(addr,authkey=b'123')
    #     self.conn5=l1.accept()
    #     #sensors = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     #sensors.bind(("192.168.33.100", 8500))
    #     self.format="utf-8"
    #     header=1000
    #     # print("connection accepted from", addr)

    # def jethandler(self):
    #     self.jetinit()
    #     while True:
    #         ms=self.conn5.recv()
    #         #ms = self.sensors.recvfrom(1024).decode("utf-8")
    #         # ms = struct.unpack('<10f', ms[0])
    #         msg=[]
    #         msg=ms.split(",")
    #         print(msg)
    #         self.label_value_XACC.setText(msg[0])
    #         self.label_value_YACC.setText(msg[1])
    #         self.label_value_ZACC.setText(msg[2])
    #         self.label_value_XGRO.setText(msg[3])
    #         self.label_value_YGRO.setText(msg[4])
    #         self.label_value_ZGRO.setText(msg[5])
    #         self.label_value_XMAG.setText(msg[6])
    #         self.label_value_YMAG.setText(msg[7])
    #         self.label_value_ZMAG.setText(msg[8])
    #         fontXACC =QFont()
    #         fontXACC.setPointSize(13)
    #         fontXACC.setBold(True)
    #         fontXACC.setWeight(75)
    #         #self.label_value_XACC.
    #         self.label_value_XACC.setFont(fontXACC)
    #         fontYACC =QFont()
    #         fontYACC.setPointSize(13)
    #         fontYACC.setBold(True)
    #         fontYACC.setWeight(75)
    #         self.label_value_YACC.setFont(fontYACC)
    #         fontZACC =QFont()
    #         fontZACC.setPointSize(13)
    #         fontZACC.setBold(True)
    #         fontZACC.setWeight(75)
    #         self.label_value_ZACC.setFont(fontZACC)
    #         fontXGRO =QFont()
    #         fontXGRO.setPointSize(13)
    #         fontXGRO.setBold(True)
    #         fontXGRO.setWeight(75)
    #         self.label_value_XGRO.setFont(fontXGRO)
    #         fontYGRO =QFont()
    #         fontYGRO.setPointSize(13)
    #         fontYGRO.setBold(True)
    #         fontYGRO.setWeight(75)
    #         self.label_value_YGRO.setFont(fontYGRO)
    #         fontZGRO =QFont()
    #         fontZGRO.setPointSize(13)
    #         fontZGRO.setBold(True)
    #         fontZGRO.setWeight(75)
    #         self.label_value_ZGRO.setFont(fontZGRO)
    #         fontXMAG =QFont()
    #         fontXMAG.setPointSize(13)
    #         fontXMAG.setBold(True)
    #         fontXMAG.setWeight(75)
    #         self.label_value_XMAG.setFont(fontXMAG)
    #         fontYMAG = QFont()
    #         fontYMAG.setPointSize(13)
    #         fontYMAG.setBold(True)
    #         fontYMAG.setWeight(75)
    #         self.label_value_YMAG.setFont(fontYMAG)
    #         fontZMAG = QFont()
    #         fontZMAG.setPointSize(13)
    #         fontZMAG.setBold(True)
    #         fontZMAG.setWeight(75)
    #         self.label_value_ZMAG.setFont(fontZMAG)

    def  JoyStick_Start(self):
            try:   

                p2=None
                if self.checkBox_joystick.isChecked()==True:
                        print("joy")
                        self.pushButton_cureentmode.setText("Manual")
                        icon = QIcon()
                        icon.addPixmap(QPixmap(":/icons/IconJPG/image 3.jpg"), QIcon.Active)
                        icon.addPixmap(QPixmap(":/icons/IconJPG/image.jpg"), QIcon.Disabled)
                        self.pushButton_speed.setIcon(icon)

                        #cmd2='python sendjoysticksocket.py'
                        #p2=subprocess.Popen(cmd2,shell=True)
                        pygame.init()
                        self.events=pygame.event.get()
                        joystick_count = pygame.joystick.get_count()
                        clock = pygame.time.Clock()
                        for i in range(joystick_count):

                            self.joystick = pygame.joystick.Joystick(i)
                            self.joystick.init()

                        # t=Thread(target=self.joyhandler)
                        # t.start()
                        self.Header = 1000
                        # PORT = 5050
                        self.Format = 'utf-8'
                        self.Joystick_client  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        #PortCheck========================================================
                        self.Joystick_client.connect(('192.168.33.1',9009))
                        self.timer1 = QTimer()

                        self.timer1.timeout.connect(self.joyhandler)  # execute `display_time`
                        #to be checked
                        self.timer1.setInterval(200)  # 1000ms = 1s
                        self.timer1.start()
                elif self.checkBox_joystick.isChecked()==False:
                        self.pushButton_cureentmode.setText("-------")
                        self.timer1.stop()
                        self.Joystick_client.close()
            except:
                  print("joystick connection error")            

    # def joystickrecv(self)
    def send(self,msg):
        # message = msg
        # msg_length = len(message)
        # send_length = str(msg_length).encode(self.Format)
        # send_length = b' ' * (self.Header - len(send_length))
        # print("df", send_length)
        # self.clientgui.send("1024".encode())
        self.clientgui.send(msg)
        

    def map(self, val):
        if not self.speed:
            return int((val * 115) + 1500)
        else:
            return int((val * 230) + 1500)
    def joyinit(self):
        try:    
            pygame.event.pump()
            # key= pygame.key.get_pressed()
            # # for  event in pygame.event.get():
            # #   if event.type==pygame.KEYDOWN:
            # if self.events.key== pygame.K_m:
            #     print("M pressed") 
            xaxl = self.joystick.get_axis(0)
            yaxl = self.joystick.get_axis(1)
            xaxr = self.joystick.get_axis(2)
            yaxr = self.joystick.get_axis(3)
            l2 = self.joystick.get_axis(4)
            r2 = self.joystick.get_axis(5)

            x = self.joystick.get_button(0)
            o = self.joystick.get_button(1)
            sqr = self.joystick.get_button(2)
            tri = self.joystick.get_button(3)
            share = self.joystick.get_button(4)
            ps = self.joystick.get_button(5)
            options = self.joystick.get_button(6)
            left_scroll_button = self.joystick.get_button(7)
            right_scroll_button = self.joystick.get_button(8)
            l1 = self.joystick.get_button(9)
            r1 = self.joystick.get_button(10)
            upward = self.joystick.get_button(11)
            downward = self.joystick.get_button(12)
            left = self.joystick.get_button(13)
            right = self.joystick.get_button(14)
            touch_pad=self.joystick.get_button(15)
            #touch_pad = joystick.get_button(15)
            #         0   1  2    3   4     5   6            7                 8              9  10   11     12      13    14   15         16    17  18  19  20    21        
            self.b = [x, o, sqr, tri,share,ps,options,left_scroll_button,right_scroll_button,l1, r1,upward,downward,left,right,touch_pad, xaxl, yaxl,l2,r2,xaxr,yaxr]
            channels = [1500, 1500, 1500,1500, 1500, 1500, 1500, 1500, 1500]
            if x and (not self.armed):
                msg = bytes("am", "latin-1")
                self.armed=1
                self.Joystick_client.send(msg)
            
            if x and (self.armed):
                msg = bytes("dm", "latin-1")
                self.armed=0
                self.Joystick_client.send(msg)
            
            if upward:
                  self.speed = 1
            if downward:
                  self.speed = 0    
            if left:
                  start=time.time()
                  while time.time()-start <5 and xaxr < self.deadZone and xaxr > -self.deadZone:
                        print("docking")
                        channels[4] =  self.docking_speed
                        channels[3] =  self.stoping_speed
                        channels[2] =  self.stoping_speed
                        channels[5] =  self.stoping_speed
                        msg = bytes("th", "latin-1")
                        self.Joystick_client.send(msg)
                        print(xaxr, yaxl)
                        self.Joystick_client.send(pickle.dumps(channels))


            
            if xaxr > self.deadZone or xaxr < -self.deadZone:
                channels[3] = self.map(xaxr)
                self.movement=1
            
            if xaxl > self.deadZone or xaxl < -self.deadZone:
                channels[5] = self.map(xaxl)
                self.movement = 1
            if yaxl > self.deadZone or yaxl < -self.deadZone:
                channels[4] = self.map(-yaxl)
                self.movement = 1
            if r2 > -0.8:
                r2 = (r2+1)/2
                channels[2] = self.map(-abs(r2))
                self.movement = 1
            if l2 > -0.8:
                l2 = (l2+1)/2
                channels[2] = self.map(abs(l2))
                self.movement = 1

            ### INTERLOCKING ###
            upwardFlag = (channels[2]!=1500) 
            no_movement  = 1
            if upwardFlag:
                minimi=0
                for i in range(0,len(channels)):
                    no_movement = (channels[i]==1500 and no_movement)
                    if i==2:
                            continue
                    minimi += (channels[i]!=1500)
                
                if minimi:
                    for i in range(0,len(channels)):
                        if channels[i] > 1500:
                                channels[i] = min(channels[i], int((0.45*230) + 1500))
                        elif channels[i]<1500:
                                channels[i] = max(channels[i], int(1500 - (0.45*230)))

            send_movement = (self.movement or (self.prev_mov and (not self.movement)))
            if l1 and ((xaxl>self.deadZone or xaxl<-self.deadZone)or(yaxl>self.deadZone or yaxl<-self.deadZone)):
                    msg = bytes("th", "latin-1")
                    self.Joystick_client.send(msg)
                    self.Joystick_client.send(pickle.dumps(channels))
                    if self.grip and self.can_grip:
                        self.grip = 0
                        msg = bytes("ar", "latin-1")
                        print("no grip")
                        self.Joystick_client.send(msg)
                        self.Joystick_client.send(bytes("g", "latin-1"))
                        self.can_grip = False
                    elif not self.grip and self.can_grip:
                        self.grip = 1
                        msg = bytes("ar", "latin-1")
                        print("grip")
                        self.Joystick_client.send(msg)
                        self.Joystick_client.send(bytes("h", "latin-1"))
                        self.can_grip = False
            if send_movement:
                msg = bytes("th", "latin-1")
                self.Joystick_client.send(msg)
                print(xaxr, yaxl)
                self.Joystick_client.send(pickle.dumps(channels))
            self.prev_mov = self.movement
            self.movement = 0

            if o and self.mode!= "MANUAL":
                msg = bytes("md", "utf-8")
                self.Joystick_client.send(msg)
                msg = bytes("m", "latin-1")
                self.Joystick_client.send(msg)
                self.mode = "MANUAL"

            if tri and self.mode!= "STABILIZE":
                msg = bytes("md", "utf-8")
                self.Joystick_client.send(msg)
                msg = bytes("s", "latin-1")
                self.Joystick_client.send(msg)
                self.mode = "STABILIZE"
            
            if sqr and self.mode!= "ALT_HOLD":
                msg = bytes("md", "utf-8")
                self.Joystick_client.send(msg)
                msg = bytes("a", "latin-1")
                self.Joystick_client.send(msg)
                self.mode = "ALT_HOLD"
            
            if l1:
                if self.grip and self.can_grip:
                    self.grip= 0
                    msg = bytes("ar", "latin-1")
                    self.Joystick_client.send(msg)
                    self.Joystick_client.send(bytes("g", "latin-1"))
                    self.can_grip = False
                elif not self.grip and self.can_grip:
                    self.grip= 1
                    msg = bytes("ar", "latin-1")
                    self.Joystick_client.send(msg)
                    self.Joystick_client.send(bytes("h", "latin-1"))
                    self.can_grip = False
            else:
                 self.can_grip = True


            if options ==1 and share ==0:
                  msg=bytes("ar" , "latin-1")
                  self.Joystick_client.send(msg)
                  self.Joystick_client.send(bytes("r", "latin-1"))
            if share ==1 and options ==0:
                  msg=bytes("ar" , "latin-1")
                  self.Joystick_client.send(msg)
                  self.Joystick_client.send(bytes("l", "latin-1"))
            # if share == 0 and options == 0 : ##### 
                #    msg=bytes("ar" , "latin-1")
                #    self.Joystick_client.send(msg)
                #    self.Joystick_client.send(bytes("t", "latin-1"))
            send_pump = self.prev_pump and (not (share or options))
            if send_pump:
                msg=bytes("ar" , "latin-1")
                self.Joystick_client.send(msg)
                self.Joystick_client.send(bytes("t", "latin-1"))
            self.prev_pump = (share or options)
            
            if r1:
                   msg=bytes("ar" , "latin-1")
                   self.Joystick_client.send(msg)
                   self.Joystick_client.send(bytes("x", "latin-1"))
            elif self.prev_r1 and (not r1) :  ######
                   msg=bytes("ar" , "latin-1")
                   self.Joystick_client.send(msg)
                   self.Joystick_client.send(bytes("o", "latin-1"))
            self.prev_r1 = r1


            if ps:
                   msg=bytes("ar" , "latin-1")
                   self.Joystick_client.send(msg)
                   self.Joystick_client.send(bytes("q", "latin-1"))
            elif self.prev_ps and (not ps): #####
                   msg=bytes("ar" , "latin-1")
                   self.Joystick_client.send(msg)
                   self.Joystick_client.send(bytes("w", "latin-1"))
            self.prev_ps = ps

            if self.prev_led != self.led:
                if self.led == 0:
                    print("led off")
                    msg=bytes("ar" , "latin-1")
                    self.Joystick_client.send(msg)
                    self.Joystick_client.send(bytes("d", "latin-1"))
                
                else :
                    print("led on")
                    msg=bytes("ar" , "latin-1")
                    self.Joystick_client.send(msg)
                    self.Joystick_client.send(bytes("s", "latin-1"))
            self.prev_led = self.led
        except:
              print("joystick connection error")          
                  

                    
            # print("3amlna el array")
        # print(self.b)
    

    def joyhandler(self):

        self.joyinit()
        msg=self.b
        # print(msg)

       # QTimer.singleShot(10, self.joyhandler)
#         if self.c1==0:
#             # self.joyinit()
#             self.c1+=1


#             #msg=self.conn.recv()
#             #print(msg)
#         #     msg=[]
#         #     msg=msg


#             if msg[1]==1:
#                  self.manual=True
#                  self.depth_hold=False
#                  self.stabilize=False
#                  self.pushButton_cureentmode.setText("Manual")
#             elif msg[2]==1:
#                  self.manual=False
#                  self.depth_hold=True
#                  self.stabilize=False
#                  self.pushButton_cureentmode.setText("Stabilize")
#             elif msg[3]==1:
#                  self.manual=False
#                  self.depth_hold=False
#                  self.stabilize=True
#                  self.pushButton_cureentmode.setText("Depth-Hold")




#             if msg[19]>self.deadZone or msg[19]>- self.deadZone :
#                 icon = QIcon()
#                 icon.addPixmap(QPixmap("IconJPG/ascending-green.jpg"), QIcon.Active)
#                 icon.addPixmap(QPixmap("IconJPG/ascending-grey.jpg"), QIcon.Disabled)
#                 self.pushButton_upward.setIcon(icon)
#             elif  msg[11]==0:
#                     icon = QIcon()

#                     icon.addPixmap(QPixmap("IconJPG/ascending-green.jpg"), QIcon.Disabled)
#                     icon.addPixmap(QPixmap("IconJPG/ascending-grey.jpg"), QIcon.Active)
#                     self.pushButton_upward.setIcon(icon)
#             if msg[11]==1 and msg[12]==0:
#                 self.counterGain=self.counterGain+1
#                 if self.counterGain<3:
#                         self.counterGain+=1
#                         print(self.counterGain)
#                 else:
#                      pass
#                 # if self.counterGain==1:
#                 #         # time.sleep(0.2)
#                 #         icon = QIcon()
#                 #         icon.addPixmap(QPixmap(":/icons/IconJPG/image2.jpg"), QIcon.Active)
#                 #         icon.addPixmap(QPixmap(":/icons/IconJPG/image.jpg"), QIcon.Disabled)
#                 #         self.pushButton_speed.setIcon(icon)
#                 if self.counterGain==1:
#                         # time.sleep(0.2)
#                         icon = QIcon()
#                         icon.addPixmap(QPixmap(":/icons/IconJPG/image 3.jpg"), QIcon.Active)
#                         icon.addPixmap(QPixmap(":/icons/IconJPG/image2.jpg"), QIcon.Disabled)
#                         self.pushButton_speed.setIcon(icon)
#                 elif self.counterGain==2:
#                         # time.sleep(0.2)
#                         icon = QIcon()
#                         icon.addPixmap(QPixmap(":/icons/IconJPG/image 4.jpg"), QIcon.Active)
#                         icon.addPixmap(QPixmap(":/icons/IconJPG/image 3.jpg"), QIcon.Disabled)
#                         self.pushButton_speed.setIcon(icon)
#                 elif self.counterGain==3:
#                         # time.sleep(0.2)
#                         icon = QIcon()
#                         icon.addPixmap(QPixmap(":/icons/IconJPG/image 5.jpg"), QIcon.Active)
#                         icon.addPixmap(QPixmap(":/icons/IconJPG/image 4.jpg"), QIcon.Disabled)
#                         self.pushButton_speed.setIcon(icon)
#             elif  msg[12]==1:
#                     icon = QIcon()

#                     icon.addPixmap(QPixmap(":/icons/IconJPG/descending-green.jpg"), QIcon.Disabled)
#                     icon.addPixmap(QPixmap(":/icons/IconJPG/descending-grey.jpg"), QIcon.Active)
#                 #     self.pushButton_downward.setIcon(icon)
#             if float(msg[17])<0.2:
#                 iconr = QIcon()
#                 iconr.addPixmap(QPixmap(":/icons/IconJPG/downward-grey.jpg"), QIcon.Active)
#                 iconr.addPixmap(QPixmap(":/icons/IconJPG/downward-green.jpg"), QIcon.Disabled)
#                 self.pushButton_backward.setIcon(iconr)
#             elif float(msg[17])>0.2:
#                 iconr = QIcon()
#                 iconr.addPixmap(QPixmap(":/icons/IconJPG/downward-green.jpg"), QIcon.Active)
#                 iconr.addPixmap(QPixmap(":/icons/IconJPG/downward-grey.jpg"), QIcon.Disabled)
#                 self.pushButton_backward.setIcon(iconr)

#             if float(msg[17])>-0.2:
#                 iconr = QIcon()
#                 iconr.addPixmap(QPixmap("IconJPG//upward-grey.jpg"), QIcon.Active)
#                 iconr.addPixmap(QPixmap("IconJPG//upward-green.jpg"), QIcon.Disabled)
#                 self.pushButton_forward.setIcon(iconr)

#             elif float(msg[17])<-0.2:
#                 iconr = QIcon()
#                 iconr.addPixmap(QPixmap("IconJPG//upward-green.jpg"), QIcon.Active)
#                 iconr.addPixmap(QPixmap("IconJPG//upward-grey.jpg"), QIcon.Disabled)
#                 self.pushButton_forward.setIcon(iconr)
#             if float(msg[16])>-0.2: #####left
#                 iconr = QIcon()
#                 iconr.addPixmap(QPixmap(":/icons/IconJPG/left-green.jpg"), QIcon.Disabled)
#                 iconr.addPixmap(QPixmap(":/icons/IconJPG/left-grey.jpg"), QIcon.Active)
#                 self.pushButton_left.setIcon(iconr)

#             elif float(msg[16])<-0.2:
#                 iconr = QIcon()
#                 iconr.addPixmap(QPixmap(":/icons/IconJPG/left-grey.jpg"), QIcon.Disabled)
#                 iconr.addPixmap(QPixmap(":/icons/IconJPG/left-green.jpg"), QIcon.Active)
#                 self.pushButton_left.setIcon(iconr)
# #------------------------------------------RIGHT
#             if msg[16]<self.deadZone: ####right
#                 iconr = QIcon()
#                 iconr.addPixmap(QPixmap("IconJPG/right-green.jpg"), QIcon.Disabled)
#                 iconr.addPixmap(QPixmap("IconJPG/right-grey.jpg"), QIcon.Active)
#                 self.pushButton_right.setIcon(iconr)

#             elif msg[16]>self.deadZone:
#                 iconr = QIcon()
#                 iconr.addPixmap(QPixmap("IconJPG/right-grey.jpg"), QIcon.Disabled)
#                 iconr.addPixmap(QPixmap("IconJPG/right-green.jpg"), QIcon.Active)
#                 self.pushButton_right.setIcon(iconr)
# #---------------------------------------------- TILT
#             if msg[13]==0 and msg[14]==0 :
#                 icon = QIcon()
#                 icon.addPixmap(QPixmap("IconJPG/tilt-grey.jpg"), QIcon.Active)
#                 icon.addPixmap(QPixmap("IconJPG/tilt-green-left.jpg"), QIcon.Disabled)
#                 icon.addPixmap(QPixmap("IconJPG/tilt-green-right.jpg"), QIcon.Disabled)

#                 self.pushButton_pump2.setIcon(icon)

#             elif msg[13]==1 and msg[14]==0 :
#                 icon = QIcon()
#                 icon.addPixmap(QPixmap("IconJPG/tilt-green-left.jpg"), QIcon.Active)
#                 icon.addPixmap(QPixmap("IconJPG/tilt-grey.jpg"), QIcon.Disabled)
#                 self.pushButton_pump2.setIcon(icon)

#             elif  msg[13]==0 and msg[14]==1 :
#                     icon = QIcon()
#                     icon.addPixmap(QPixmap("IconJPG/tilt-grey.jpg"), QIcon.Disabled)
#                     icon.addPixmap(QPixmap("IconJPG/tilt-green-right.jpg"), QIcon.Active)
#                     self.pushButton_pump2.setIcon(icon)
#         #     if msg[9]==1 :
#         #             self.Xgripper=not self.Xgripper
#         #             if self.Xgripper==True:
#         #                 icon = QIcon()
#         #                 icon.addPixmap(QPixmap(":/icons/IconJPG/\x-open.jpg"), QIcon.Active)
#         #                 icon.addPixmap(QPixmap(":/icons/IconJPG/\x-close.jpg"),QIcon.Disabled)
#         #                 self.pushButton_horizontal_gripper.setIcon(icon)
#         # #     elif msg[9]==0 and msg[10]==1:
#         #             if self.Xgripper==False:
#         #                 icon = QIcon()
#         #                 icon.addPixmap(QPixmap(":/icons/IconJPG/\x-open.jpg"), QIcon.Disabled)
#         #                 icon.addPixmap(QPixmap(":/icons/IconJPG/\x-close.jpg"),QIcon.Active)
#         #                 self.pushButton_horizontal_gripper.setIcon(icon)
#         #     if float(msg[19])<0 and float(msg[18])>-1:
#         #     if msg[10]==1:
#         #             self.Ygripper=not self.Ygripper
#         #             if self.Ygripper==True:
#         #                 icon = QIcon()
#         #                 icon.addPixmap(QPixmap(":/icons/IconJPG/y-open.jpg"), QIcon.Active)
#         #                 icon.addPixmap(QPixmap(":/icons/IconJPG/y-close.jpg"), QIcon.Disabled)
#         #                 self.pushButton_horizontal_gripper_2.setIcon(icon)
#         # #     elif float(msg[19])>-1 and float(msg[18])<0:
#         #             if self.Ygripper==False:
#         #                 icon = QIcon()
#         #                 icon.addPixmap(QPixmap(":/icons/IconJPG/y-open.jpg"), QIcon.Disabled)
#         #                 icon.addPixmap(QPixmap(":/icons/IconJPG/y-close.jpg"), QIcon.Active)
#         #                 self.pushButton_horizontal_gripper_2.setIcon(icon)
#             if msg[1]==0 and msg[2]==1:
#                     icon = QIcon()
#                     icon.addPixmap(QPixmap("IconJPG/antiClockwise-green.jpg"), QIcon.Active)
#                     icon.addPixmap(QPixmap("IconJPG/antiClockwise-grey.jpg"), QIcon.Disabled)
#                     self.pushButton_anticlockwise.setIcon(icon)
#             elif msg[1]==1 or msg[2]==0:
#                     icon = QIcon()
#                     icon.addPixmap(QPixmap("IconJPG/antiClockwise-green.jpg"), QIcon.Disabled)
#                     icon.addPixmap(QPixmap("IconJPG/antiClockwise-grey.jpg"), QIcon.Active)
#                     self.pushButton_anticlockwise.setIcon(icon)
#             if msg[1]==1 and msg[2]==0:
#                     icon = QIcon()
#                     icon.addPixmap(QPixmap(":/icons/IconJPG/clockwise-green.jpg"), QIcon.Active)
#                     icon.addPixmap(QPixmap(":/icons/IconJPG/clockwise-grey.jpg"), QIcon.Disabled)
#                     self.pushButton_clockwise.setIcon(icon)
#             elif msg[1]==0 or msg[2]==1:
#                     icon = QIcon()
#                     icon.addPixmap(QPixmap(":/icons/IconJPG/clockwise-green.jpg"), QIcon.Disabled)
#                     icon.addPixmap(QPixmap(":/icons/IconJPG/clockwise-grey.jpg"), QIcon.Active)
#                     self.pushButton_clockwise.setIcon(icon)
#             if msg[4]==1:
#                     self.flagarm=1
#                     #3ayzeen label b msg armed wala disarmed

        # elif self.c1>0:

            #msg=self.conn.recv()
            #print(msg)
        #     msg=[]
        #     msg=msg
        #     print(msg)
            # print(msg)
            # print(f" {type(msg[0])}========= {msg[0]}")
        #     print(len(msg))
        #     for i in range(0,len(msg)):
        #       msg[i]=msg[i].lstrip('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        #       msg[i]=msg[i].rstrip('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

            # zero=0
            # print(bytes(zero,'utf-8'))
        #     print(msg)
        if msg[0]==1:
            if self.w==False:
                self.w=True
                icon = QIcon()
                icon.addPixmap(QPixmap("IconJPG/right.jpg"), QIcon.Active)
                icon.addPixmap(QPixmap(":/icons/IconJPG/wrong.jpg"), QIcon.Disabled)
                self.pushButton_ready.setIcon(icon)
            elif self.w==True:
                self.w=False
                icon = QIcon()
                icon.addPixmap(QPixmap(":/icons/IconJPG/wrong.jpg"), QIcon.Active)
                icon.addPixmap(QPixmap("IconJPG/right.jpg"), QIcon.Disabled)
                self.pushButton_ready.setIcon(icon)
        if msg[11]==1 and msg[12]==0:

            if self.counterGain<=2:
                    self.counterGain+=1
            else:
                    pass
            if self.counterGain==1:
                    # time.sleep(0.2)
                    icon = QIcon()
                    icon.addPixmap(QPixmap(":/icons/IconJPG/image 3.jpg"), QIcon.Active)
                    icon.addPixmap(QPixmap(":/icons/IconJPG/image 5.jpg"), QIcon.Disabled)
                    self.pushButton_speed.setIcon(icon)
            elif self.counterGain==2:
                    # time.sleep(0.2)
                    icon = QIcon()
                    icon.addPixmap(QPixmap(":/icons/IconJPG/image 5.jpg"), QIcon.Active)
                    icon.addPixmap(QPixmap(":/icons/IconJPG/image 3.jpg"), QIcon.Disabled)
                    self.pushButton_speed.setIcon(icon)
            # elif self.counterGain==3:
            #         # time.sleep(0.2)
            #         icon = QIcon()
            #         icon.addPixmap(QPixmap(":/icons/IconJPG/image 4.jpg"), QIcon.Active)
            #         icon.addPixmap(QPixmap(":/icons/IconJPG/image 3.jpg"), QIcon.Disabled)
            #         self.pushButton_speed.setIcon(icon)
            # elif self.counterGain==4:
            #         # time.sleep(0.2)
            #         icon = QIcon()
            #         icon.addPixmap(QPixmap(":/icons/IconJPG/image 5.jpg"), QIcon.Active)
            #         icon.addPixmap(QPixmap(":/icons/IconJPG/image 4.jpg"), QIcon.Disabled)
            #         self.pushButton_speed.setIcon(icon)
        elif  msg[12]==1 and msg[11]==0:

            if self.counterGain>=1:
                    self.counterGain-=1

            else:
                    pass
            if self.counterGain==1:
                    # time.sleep(0.2)
                    icon = QIcon()
                    icon.addPixmap(QPixmap(":/icons/IconJPG/image 3.jpg"), QIcon.Active)
                    icon.addPixmap(QPixmap(":/icons/IconJPG/image 5.jpg"), QIcon.Disabled)
                    self.pushButton_speed.setIcon(icon)

            elif self.counterGain==2:
                    # time.sleep(0.2)
                    icon = QIcon()
                    icon.addPixmap(QPixmap(":/icons/IconJPG/image 5.jpg"), QIcon.Active)
                    icon.addPixmap(QPixmap(":/icons/IconJPG/image 3.jpg"), QIcon.Disabled)
                    self.pushButton_speed.setIcon(icon)
            # elif self.counterGain==3:
            #         # time.sleep(0.2)
            #         icon = QIcon()
            #         icon.addPixmap(QPixmap(":/icons/IconJPG/image 4.jpg"), QIcon.Active)
            #         icon.addPixmap(QPixmap(":/icons/IconJPG/image 3.jpg"), QIcon.Disabled)
            #         self.pushButton_speed.setIcon(icon)
            # elif self.counterGain==4:
            #         # time.sleep(0.2)
            #         icon = QIcon()
            #         icon.addPixmap(QPixmap(":/icons/IconJPG/image 5.jpg"), QIcon.Active)
            #         icon.addPixmap(QPixmap(":/icons/IconJPG/image 4.jpg"), QIcon.Disabled)
            #         self.pushButton_speed.setIcon(icon)

        if msg[1]==1 :
                self.manual=True
                self.depth_hold=False
                self.stabilize=False
                self.pushButton_cureentmode.setText("Manual")
        elif msg[2]==1:
                self.manual=False
                self.depth_hold=True
                self.stabilize=False
                self.pushButton_cureentmode.setText("Depth-Hold")
        elif msg[3]==1:
                self.manual=False
                self.depth_hold=False
                self.stabilize=True
                self.pushButton_cureentmode.setText("Stabilize")
        if msg[4]==1 and msg[6]==0:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/IconJPG/pup1.jpg"), QIcon.Active)
            icon.addPixmap(QPixmap(":/icons/IconJPG/pup0.jpg"), QIcon.Disabled)
            self.pushButton_pump.setIcon(icon)
        elif msg[4]==0 and msg[6]==0:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/IconJPG/pup1.jpg"), QIcon.Disabled)
            icon.addPixmap(QPixmap(":/icons/IconJPG/pup0.jpg"), QIcon.Active)
            self.pushButton_pump.setIcon(icon)
        if msg[6]==1 and msg[4]==0:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/IconJPG/pup2.jpg"), QIcon.Active)
            icon.addPixmap(QPixmap(":/icons/IconJPG/pup0.jpg"), QIcon.Disabled)
            self.pushButton_pump.setIcon(icon)
        elif msg[6]==0 and msg[4]==0:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/IconJPG/pup2.jpg"), QIcon.Disabled)
            icon.addPixmap(QPixmap(":/icons/IconJPG/pup0.jpg"), QIcon.Active)
            self.pushButton_pump.setIcon(icon)

        if  msg[19]>self.deadZone or msg[19]>- self.deadZone :
            icon = QIcon()
            icon.addPixmap(QPixmap("IconJPG/ascending-green.jpg"), QIcon.Active)
            icon.addPixmap(QPixmap("IconJPG/ascending-grey.jpg"), QIcon.Disabled)
            self.pushButton_upward.setIcon(icon)
        elif   msg[19]<self.deadZone or msg[19]<- self.deadZone:
                icon = QIcon()

                icon.addPixmap(QPixmap("IconJPG/ascending-green.jpg"), QIcon.Disabled)
                icon.addPixmap(QPixmap("IconJPG/ascending-grey.jpg"), QIcon.Active)
                self.pushButton_upward.setIcon(icon)
        if  msg[18]>self.deadZone or msg[18]>- self.deadZone:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/IconJPG/descending-green.jpg"), QIcon.Active)
            icon.addPixmap(QPixmap(":/icons/IconJPG/descending-grey.jpg"), QIcon.Disabled)
            self.pushButton_downward.setIcon(icon)
        elif   msg[18]<self.deadZone or msg[18]<- self.deadZone:
                icon = QIcon()

                icon.addPixmap(QPixmap(":/icons/IconJPG/descending-green.jpg"), QIcon.Disabled)
                icon.addPixmap(QPixmap(":/icons/IconJPG/descending-grey.jpg"), QIcon.Active)
                self.pushButton_downward.setIcon(icon)
        if msg[17]<self.deadZone:
            iconr = QIcon()
            iconr.addPixmap(QPixmap(":/icons/IconJPG/downward-grey.jpg"), QIcon.Active)
            iconr.addPixmap(QPixmap(":/icons/IconJPG/downward-green.jpg"), QIcon.Disabled)
            self.pushButton_backward.setIcon(iconr)
        elif msg[17]>self.deadZone:
            iconr = QIcon()
            iconr.addPixmap(QPixmap(":/icons/IconJPG/downward-green.jpg"), QIcon.Active)
            iconr.addPixmap(QPixmap(":/icons/IconJPG/downward-grey.jpg"), QIcon.Disabled)
            self.pushButton_backward.setIcon(iconr)

        if msg[17]>-self.deadZone:
            iconr = QIcon()
            iconr.addPixmap(QPixmap("IconJPG//upward-grey.jpg"), QIcon.Active)
            iconr.addPixmap(QPixmap("IconJPG//upward-green.jpg"), QIcon.Disabled)
            self.pushButton_forward.setIcon(iconr)

        elif msg[17]<-self.deadZone:
            iconr = QIcon()
            iconr.addPixmap(QPixmap("IconJPG//upward-green.jpg"), QIcon.Active)
            iconr.addPixmap(QPixmap("IconJPG//upward-grey.jpg"), QIcon.Disabled)
            self.pushButton_forward.setIcon(iconr)
        if msg[16]>-self.deadZone: #####left
            iconr = QIcon()
            iconr.addPixmap(QPixmap(":/icons/IconJPG/left-green.jpg"), QIcon.Disabled)
            iconr.addPixmap(QPixmap(":/icons/IconJPG/left-grey.jpg"), QIcon.Active)
            self.pushButton_left.setIcon(iconr)

        elif msg[16]<-self.deadZone:
            iconr = QIcon()
            iconr.addPixmap(QPixmap(":/icons/IconJPG/left-grey.jpg"), QIcon.Disabled)
            iconr.addPixmap(QPixmap(":/icons/IconJPG/left-green.jpg"), QIcon.Active)
            self.pushButton_left.setIcon(iconr)
#------------------------------------------RIGHT
        if msg[16]>self.deadZone:
            iconr = QIcon()
            iconr.addPixmap(QPixmap("IconJPG/right-grey.jpg"), QIcon.Disabled)
            iconr.addPixmap(QPixmap("IconJPG/right-green.jpg"), QIcon.Active)
            self.pushButton_right.setIcon(iconr)
        if msg[16]<self.deadZone: ####right
            iconr = QIcon()
            iconr.addPixmap(QPixmap("IconJPG/right-green.jpg"), QIcon.Disabled)
            iconr.addPixmap(QPixmap("IconJPG/right-grey.jpg"), QIcon.Active)
            self.pushButton_right.setIcon(iconr)

        
#---------------------------------------------- Orange pump and left back --------------------------------------------
        if msg[10]==0 :
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/IconJPG/pump_off.png"), QIcon.Active)
            icon.addPixmap(QPixmap(":/icons/IconJPG/pump_on.png"), QIcon.Disabled)

            self.pushButton_pump2.setIcon(icon)

        elif msg[10]==1 :
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/IconJPG/pump_off.png"), QIcon.Disabled)
            icon.addPixmap(QPixmap(":/icons/IconJPG/pump_on.png"), QIcon.Active)
            self.pushButton_pump2.setIcon(icon)

        if msg[5]==0 :
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/IconJPG/without_bubble2.jpg"), QIcon.Active)
            icon.addPixmap(QPixmap(":/icons/IconJPG/with_bubble.jpg"), QIcon.Disabled)

            self.pushButton_lift_back.setIcon(icon)

        elif msg[5]==1 :
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/IconJPG/without_bubble2.jpg"), QIcon.Disabled)
            icon.addPixmap(QPixmap(":/icons/IconJPG/with_bubble.jpg"), QIcon.Active)
            self.pushButton_lift_back.setIcon(icon)

        # elif  msg[13]==0 and msg[14]==1 :
        #         icon = QIcon()
        #         icon.addPixmap(QPixmap("IconJPG/tilt-grey.jpg"), QIcon.Disabled)
        #         icon.addPixmap(QPixmap("IconJPG/tilt-green-right.jpg"), QIcon.Active)
        #         self.pushButton_pump2.setIcon(icon)
    #     if msg[9]==1 and self.XgripperCounter==0:
    #             self.XgripperCounter=1
    #             if self.XgripperCounter==1:
    #                 icon = QIcon()
    #                 icon.addPixmap(QPixmap(":/icons/IconJPG/\x-open.jpg"), QIcon.Active)
    #                 icon.addPixmap(QPixmap(":/icons/IconJPG/\x-close.jpg"),QIcon.Disabled)
    #                 self.pushButton_horizontal_gripper.setIcon(icon)
    #     elif msg[9]==0 and msg[10]==1:
            #     if self.XgripperCounter==False:
            #         icon = QIcon()
            #         icon.addPixmap(QPixmap(":/icons/IconJPG/\x-open.jpg"), QIcon.Disabled)
            #         icon.addPixmap(QPixmap(":/icons/IconJPG/\x-close.jpg"),QIcon.Active)
            #         self.pushButton_horizontal_gripper.setIcon(icon)

    #     if msg[9]==0:
    #         icon = QIcon()
    #         icon.addPixmap(QPixmap(":/icons/IconJPG/\x-open.jpg"), QIcon.Disabled)
    #         icon.addPixmap(QPixmap(":/icons/IconJPG/\x-close.jpg"),QIcon.Active)
    #         self.pushButton_horizontal_gripper.setIcon(icon)
        if msg[9]==1 :
            if self.flag_gripper == False:
                    self.flag_gripper =True 
                    icon = QIcon()

                    icon.addPixmap(QPixmap(":/icons/IconJPG/gripper_open.jpg"), QIcon.Active)
                    icon.addPixmap(QPixmap(":/icons/IconJPG/gripper_close.jpg"),QIcon.Disabled)
                    self.pushButton_horizontal_gripper.setIcon(icon)
                    
                    

            elif self.flag_gripper == True:
                self.flag_gripper = False
                icon = QIcon()
                icon.addPixmap(QPixmap(":/icons/IconJPG/gripper_close.jpg"),QIcon.Active)
                icon.addPixmap(QPixmap(":/icons/IconJPG/gripper_open.jpg"), QIcon.Disabled)
                
                self.pushButton_horizontal_gripper.setIcon(icon)
        # print(self.dcv2)
        if msg[5]==1:
                if self.dcv2==True:
                    self.dcv2=False
                    

                elif self.dcv2==False:
                    self.dcv2=True
                            
            # if msg[0]==1:
            # if self.w==False:
            #     self.w=True
            #     icon = QIcon()
            #     icon.addPixmap(QPixmap("IconJPG/right.jpg"), QIcon.Active)
            #     icon.addPixmap(QPixmap(":/icons/IconJPG/wrong.jpg"), QIcon.Disabled)
            #     self.pushButton_ready.setIcon(icon)
            # elif self.w==True:
            #     self.w=False
            #     icon = QIcon()
            #     icon.addPixmap(QPixmap(":/icons/IconJPG/wrong.jpg"), QIcon.Active)
            #     icon.addPixmap(QPixmap("IconJPG/right.jpg"), QIcon.Disabled)
            #     self.pushButton_ready.setIcon(icon)



            # if self.XgripperCounter==0:
            #         self.XgripperCounter=1
            # else:
            #      self.XgripperCounter=0
        
    # if self.Xgripper==False:
    #         icon.addPixmap(QPixmap(":/icons/IconJPG/\y-open.jpg"), QIcon.Active)
    #         icon.addPixmap(QPixmap(":/icons/IconJPG/\y-close.jpg"),QIcon.Disabled)
            
        # elif msg[9]==0  :
        #     # if self.XgripperCounter==0:
        #     #         self.XgripperCounter=1
        #     # else:
        #     #      self.XgripperCounter=0
        #     icon = QIcon()
        #     # self.Ygripper=False
        #     # if self.Xgripper==True:

        #     #         icon.addPixmap(QPixmap(":/icons/IconJPG/\y-open.jpg"), QIcon.Disabled)
        #     #         icon.addPixmap(QPixmap(":/icons/IconJPG/\y-close.jpg"),QIcon.Active)
        #     # if self.Xgripper==False:
        #     icon.addPixmap(QPixmap(":/icons/IconJPG/\x-openn.png"), QIcon.Disabled)
        #     icon.addPixmap(QPixmap(":/icons/IconJPG/\x-closse.png"),QIcon.Active)
        #     self.pushButton_horizontal_gripper.setIcon(icon)

        if msg[20]<-self.deadZone:
                icon = QIcon()
                icon.addPixmap(QPixmap(":/icons/IconJPG/antiClockwise-green.jpg"), QIcon.Active)
                icon.addPixmap(QPixmap(":/icons/IconJPG/antiClockwise-grey.jpg"), QIcon.Disabled)
                self.pushButton_anticlockwise.setIcon(icon)
        elif msg[20]>-self.deadZone:
                icon = QIcon()
                icon.addPixmap(QPixmap(":/icons/IconJPG/antiClockwise-green.jpg"), QIcon.Disabled)
                icon.addPixmap(QPixmap(":/icons/IconJPG/antiClockwise-grey.jpg"), QIcon.Active)
                self.pushButton_anticlockwise.setIcon(icon)
        if  msg[20]>self.deadZone:
                icon = QIcon()
                icon.addPixmap(QPixmap(":/icons/IconJPG/clockwise-green.jpg"), QIcon.Active)
                icon.addPixmap(QPixmap(":/icons/IconJPG/clockwise-grey.jpg"), QIcon.Disabled)
                self.pushButton_clockwise.setIcon(icon)
        elif msg[20]<self.deadZone:
                icon = QIcon()
                icon.addPixmap(QPixmap(":/icons/IconJPG/clockwise-green.jpg"), QIcon.Disabled)
                icon.addPixmap(QPixmap(":/icons/IconJPG/clockwise-grey.jpg"), QIcon.Active)
                self.pushButton_clockwise.setIcon(icon)




    def startTime(self):
            self.timer.start(1000)
            self.Startbtn_Timer.setEnabled(False)
            self.pausebtn_Timer.setEnabled(True)
    def stopTime(self):
            self.timer.stop()
            self.pausebtn_Timer.setEnabled(False)
            self.Startbtn_Timer.setEnabled(True)
    def reset(self):
            self.c=0
            self.seconds = 0
            self.timer.stop()
            self.pausebtn_Timer.setEnabled(False)
            self.Startbtn_Timer.setEnabled(True)
            self.rep_timer.setText("       "+"0:00:00")


    def showClock(self):

                lbl_clck=self.convert(self.seconds)
                self.seconds = self.seconds + 1

                font =QFont()
                font.setPointSize(18)
                font.setBold(True)
                font.setWeight(70)
                self.rep_timer.setFont(font)
                self.rep_timer.setGeometry(QRect(140, 20, 251, 31))
                self.rep_timer.setStyleSheet("color: white; ")
                self.rep_timer.setText("       "+lbl_clck)


    def convert(self,sec):
            sec=sec%(24*3600)
            hrs=sec//3600
            sec%=3600
            min=sec//60
            sec%=60
            return "%d:%02d:%02d" % (hrs,min,sec)


app = QApplication(sys.argv)
UiWindow = UI()
app.exec_()
