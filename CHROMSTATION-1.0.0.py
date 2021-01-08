import PyQt5
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets
import PyQt5.sip
from PyQt5 import QtCore, QtGui, QtWidgets
from scipy import stats
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import math
import scipy
import serial
import sys
import time
import numpy as np
import threading

import input_new_device

import matplotlib
import matplotlib.animation as animation

from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure
from matplotlib import style

LARGE_FONT= QFont("Verdana", 12)
style.use("ggplot")

ab = open('Logs/Data_input.txt', 'w')
ab.write('')
ab.close()

f2 = Figure(figsize=(20,20), dpi=100)
a3 = f2.add_subplot(111)

Cof_file=open('Logs/Input_Coeff.txt').read()
DataInList = Cof_file.split('\n')
list_of_data = []
c1 = 1.0
c2 = 1.0
c3 = 1.0
c4 = 1.0       
for eachLine in DataInList:
    x, y = eachLine.split()
    list_of_data.append(y)
try:
    c1 = float(list_of_data[1])
    c2 = float(list_of_data[2])
    c3 = float(list_of_data[3])
    c4 = float(list_of_data[4])

except:
    pass


def animate2(self):
        pullData3 = open("Logs/Data_input.txt", 'r').read()
        dataList3 = pullData3.split('\n')
        xlist3 = []
        ylist3 = []
        x3 = ''
        y3 = ''
        for eachLine in dataList3 :
            if len(eachLine)!=0:
                x3, y3 = eachLine.split()
                try:
                    x31 = "%.2f"%(float(x3))
                    y31 = "%.2f"%(float(y3))
                    xlist3.append(float(x31))
                    ylist3.append(float(y31))
                except:
                    pass

        a3.clear()
        try:
            a3.plot(xlist3, ylist3, label =(str("%.2f"%(float(x3)))+'min\n'+ str("%.2f"%(float(y3)))+'uScm-1'))
            a3.legend(loc= 'upper right', bbox_to_anchor=(1.1,1.105), ncol=3, fancybox=True, shadow=True)
        except:
            pass
        a3.set_title("CHROMATOGRAM")
        a3.set_ylabel('k / uScm-1')
        a3.set_xlabel('Time / min')

        
class IonWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ion Chrom App")
        msgBox = QMessageBox()
        msgBox.setIconPixmap(QPixmap("Media/ClientIcon.ico"))
        msgBox.setWindowTitle("CHROM-STATION")
        msgBox.setWindowIcon(QIcon("Media/ClientIcon.ico"))
        msgBox.setText("CHROM - STATION")
        msgBox.setInformativeText("\nVersion 1.0.0\nDeveloped by BITS-Pilani")       
        msgBox.exec()

        self.HomePage()
        
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.HomePage_widget)        
        
        self.stacked_layout.setCurrentIndex(0)
        self.setWindowIcon(QIcon("Media/ClientIcon.ico"))
    
        self.Central_widget = QWidget()
        self.Central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.Central_widget)

    def HomePage(self):

        #setting up layout of the page:
        icon = QIcon(QPixmap('Media/ClientIcon.ico'))
        icon2 = QIcon(QPixmap('Media/graphs-review.ico'))
        icon4 = QIcon(QPixmap('Media/Calibration-icon.png'))
        icon3 = QIcon(QPixmap('Media/peak-105546.png'))
        
        self.OnlineBut = QPushButton()
        self.OnlineBut.clicked.connect(self.Online_Mode)

        self.ReviewBut = QPushButton()
        self.ReviewBut.clicked.connect(self.ReviewMode)
        
        self.OverlayBut = QPushButton()
        self.OverlayBut.clicked.connect(self.OverlayMode)

        self.CalibBut = QPushButton()
        self.CalibBut.clicked.connect(self.Calib_Mode)

        for i,j,k in zip([self.OnlineBut, self.ReviewBut, self.OverlayBut, self.CalibBut],
                       [icon, icon2, icon3, icon4],
                         ["Go Online", "Review", "Overlay", "Calibration"]):
            i.setIcon(j)
            i.setIconSize(QSize(128, 128))
            i.setToolTip(k)
            try:
                i.setMaximumWidth(135)
            except:
                pass
        
           
        # set zero border.
        #self.OnlineBut.
        self.TEXT_BOX_H = QPlainTextEdit()
        self.TEXT_BOX_H.setMaximumWidth(135)
        self.TEXT_BOX_H.setReadOnly(True)
        
        self.ex1 = QVBoxLayout()
        self.ex1grp = QGroupBox()

        for i in [self.ReviewBut, self.OverlayBut, self.CalibBut, self.TEXT_BOX_H]:
            i.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding)
            #i.setStyleSheet('QPushButton{border: 0px solid; background: transparent; shadow: True; highlight: true}')
        
        self.ex1.addWidget(self.OnlineBut) 
        self.ex1.addWidget(self.TEXT_BOX_H)
        
        self.ex1grp.setLayout(self.ex1)
        
        
        
        self.ex3 = QVBoxLayout()
        self.ex3grp = QGroupBox()

        for i in [self.ReviewBut, self.OverlayBut, self.CalibBut]:
            self.ex3.addWidget(i)        
        
        self.ex3grp.setLayout(self.ex3)
        
                
        self.tempWid = QGroupBox()
        self.tempLay1 = QVBoxLayout()
               
        self.tempLay1.addWidget(self.ex1grp,)
        self.tempLay1.addWidget(self.ex3grp,)
      
        self.tempWid.setLayout(self.tempLay1)
            
        self.tempWid2 = QGroupBox()
        self.tempLay2 = QVBoxLayout()
                
        canvas = FigureCanvas(Figure(figsize=(10,10), dpi=100))

        self.tempLay2.addWidget(canvas)
        self.Tb = NavigationToolbar(canvas, self)
        self.tempLay2.addWidget(self.Tb)

        self.tempWid2.setLayout(self.tempLay2)

        self.Mode_layout = QGridLayout()
            
        self.Mode_layout.addWidget(self.tempWid, 1,1)
        self.Mode_layout.addWidget(self.tempWid2, 1,3)
                
         #defining widget for the stack:
        
        self.HomePage_widget = QWidget()
        self.HomePage_widget.setLayout(self.Mode_layout)
        self.HomePage_widget.setGeometry(100,100,200,200)
        self.HomePage_widget.setWindowTitle("Ion Chrom APP")
        

        #Initiating the data pulling from log file:
        
        addedData = open("Logs/Log.txt", 'r').read()
        dataList = addedData.split('\n')
        Details = ''
        xlist = []
        ylist = []

        for eachLine in dataList:
                    try:
                        x, y = eachLine.split()
                        xlist.append(float(x))
                        freq = float(y)
                        k = (c1*freq*freq*freq + c2*freq*freq + c3*freq + c4)
                        ylist.append(float(k))
                    except:
                        Details += eachLine+'\n'
                        pass

        
        ax1 = canvas.figure.subplots()
        ax1.plot(xlist, ylist, label='uScm-1')
        ax1.set_title("CHROMATOGRAM")
        ax1.set_ylabel('k / uScm-1')
        ax1.set_xlabel('Time / mins')
        ax1.legend(loc="best")       
        self.TEXT_BOX_H.setPlainText(str(Details))
        
    def OnlineSetting_Page(self):

        #setting up the layout:
        
        self.Group1 = QGroupBox()
        self.tempF = QFormLayout()#
        
        self.Strength = QPushButton('Strength (mM)')
        self.Strength.clicked.connect(self.getstrength)
        self.strenghtline = QLineEdit()
        self.strenghtline.setReadOnly(True)
        self.Strength.setEnabled(False)
        self.CO3 = QLabel('CO3')
        self.CO3IN = QLineEdit()
        self.CO3IN.setReadOnly(True)
        self.HCO3 = QLabel('HCO3')
        self.HCO3IN = QLineEdit()
        self.HCO3IN.setReadOnly(True)

        self.inco3 = ''
        self.inhco3 = ''          

        self.EluentBut = QLabel("Eluent")
        self.LeStatus = QComboBox()
        
        items = open("Logs/Eluent.txt", 'r').read()
        itemsData = []
        itemsData = items.split('\n')
        self.LeStatus.addItems(itemsData)
        
        self.LeStatus.activated.connect(self.gettext)
        self.LeStatus.currentIndexChanged.connect(self.gettext)
        
        self.tempF.addRow(self.EluentBut, self.LeStatus)
        self.tempF.addRow(self.Strength)
        self.tempF.addRow(self.strenghtline)
        self.tempF.addRow(self.CO3, self.CO3IN )
        self.tempF.addRow(self.HCO3, self.HCO3IN)

        
        self.Group1.setLayout(self.tempF)##
        

        self.Group2 = QGroupBox()
        self.tempF2 = QVBoxLayout()#
        
        self.Choice = QRadioButton("Ion Chromatography")
        self.Choice.setChecked(True)
        self.Choice.toggled.connect(self.disable)
        
        self.Choice2 = QRadioButton("Ion Exclusion")
        self.Choice2.toggled.connect(self.disable)######################      

        self.StatusBut = QPushButton("Status")

        self.exhusTime = 0.000
        
        self.StatusBut.clicked.connect(self.Information)##############

        for i in [self.Choice, self.Choice2, self.StatusBut]:
            self.tempF2.addWidget(i)

        self.Group2.setLayout(self.tempF2)##


        self.Group3 = QGroupBox()
        self.tempF3 = QFormLayout()#


        self.FlowRate = QLabel("Flow Rate (ml/min)")
        self.FlowIn = QLineEdit()
        self.FlowIn.editingFinished.connect(self.Check_start_condition)
        self.Vol_lab = QLabel('Sample Volume(uL)')
        self.Vol_lin = QComboBox()
        self.Vol_lin.activated.connect(self.Check_start_condition)
        
        self.Time = QLabel("Expt. Time (min)")
        self.TimeIn = QComboBox()

        #adding time from log file:
        
        Time = open("Logs/TimeDomain.txt", 'r').read()
        TimeData = []
        TimeData = Time.split('\n')
        self.TimeIn.addItems(TimeData)

        vol = open("Logs/Vol_input.txt", 'r').read()
        Volu = []
        Volu = vol.split('\n')
        self.Vol_lin.addItems(Volu)

        self.TimeIn.currentIndexChanged.connect(self.getint)
        self.TimeIn.activated.connect(self.getint)
#####
          
    
        self.DetailsBut = QPushButton("Details")
        self.DetailsBut.clicked.connect(self.DETAILS)
        
        self.startBut = QPushButton("START")     
        self.startBut.setEnabled(False)      
        self.startBut.clicked.connect(self.START)

        self.savBut = QPushButton("File Destination")
        self.savBut.clicked.connect(self.SaveDataLoc)
        
        self.savName = QLineEdit()
        self.savName.setReadOnly(True)
        self.savName.textChanged.connect(self.Check_start_condition)

        self.tempF3.addRow(self.Vol_lab, self.Vol_lin)
        self.tempF3.addRow(self.FlowRate, self.FlowIn)
        self.tempF3.addRow(self.Time, self.TimeIn)
        self.tempF3.addRow(self.DetailsBut,)
        self.tempF3.addRow(self.savBut,)
        self.tempF3.addRow(self.savName,)
        self.tempF3.addRow(self.startBut,)

        self.Group3.setLayout(self.tempF3)

##########
        self.bgLab = QLabel("           CHECK BACKGROUND")
        self.bgTime = QLabel("Time (min)")
        self.bgTimeIn = QComboBox()

        Timebg = open("Logs/TimeDomain.txt", 'r').read()
        TimeDatabg = []
        TimeDatabg = Timebg.split('\n')
        self.bgTimeIn.addItems(TimeDatabg)
        self.bgTimeIn.activated.connect(self.getint2)
        
        
        self.okBut = QPushButton("OK")
        self.okBut.setEnabled(False)
        self.okBut.clicked.connect(self.BACKGROUND)

        self.grp4 = QGroupBox()
        self.tempbg = QFormLayout()
        self.tempbg.addRow(self.bgLab)
        self.tempbg.addRow(self.bgTime, self.bgTimeIn)
        self.tempbg.addRow(self.okBut)
        self.grp4.setLayout(self.tempbg)
        
#########
        self.grp5 = QGroupBox()
        self.tempos22 = QVBoxLayout()

        self.backBut = QPushButton("Back")
        self.backBut.clicked.connect(self.Offline_Mode)
        
        
        self.tempos22.addWidget(self.backBut)
        
        self.grp5.setLayout(self.tempos22)

        
        self.FinalGroup1 = QGroupBox()
        self.OneSide = QVBoxLayout()####

        self.Message_o = QLabel()

        for i in [self.Group2, self.Group1, self.Group3, self.grp4, self.grp5, self.Message_o]:
            self.OneSide.addWidget(i)
        


        self.FinalGroup1.setLayout(self.OneSide)##
        self.OneSide.addStretch()

        self.FinalGroup2 = QGroupBox()
        self.OtherSide = QVBoxLayout()
        
        self.canvas2 = FigureCanvas(Figure(figsize=(20,20), dpi=100))
        self.Tb2 = NavigationToolbar(self.canvas2, self)
        
        self.OtherSide.addWidget(self.canvas2)
        self.OtherSide.addWidget(self.Tb2)

        self.FinalGroup2.setLayout(self.OtherSide)##
      
        self.grow_grid = QHBoxLayout()
        self.grow_grid.addWidget(self.FinalGroup1)
        self.grow_grid.addWidget(self.FinalGroup2)

        self.FinalGroup1.setMaximumWidth(190)
                        
        self.view_mode_widget = QWidget()
        self.view_mode_widget.setLayout(self.grow_grid)
        

        self.canvas2.addedData = open("Logs/Data_input.txt", 'r').read()
        dataList2 = self.canvas2.addedData.split('\n')
        xlist2 = []
        ylist2 = []

        for eachLine in dataList2 :
                if len(eachLine)>1:
                    x2, y2 = eachLine.split()
                    try:
                        xlist2.append(float(x2))
                        ylist2.append(float(y2))
                    except:
                        pass

        self.ax12 = self.canvas2.figure.subplots()
        self.ax12.plot(xlist2, ylist2, label = 'uScm-1')
        self.ax12.set_title("CHROMATOGRAM")
        self.ax12.set_ylabel('k / uScm-1')
        self.ax12.set_xlabel('Time / mins')
        self.ax12.legend(loc="best")
                
    def StartPage(self):

        self.Group1o = QGroupBox()
        self.tempFo = QFormLayout()#
        
        self.Strengtho = QPushButton('Strenght(mM)')
        self.Strengtho.setEnabled(False)
        self.strenghtlineo = QLineEdit()
        self.strenghtlineo.setReadOnly(True)
        strenText = self.strenghtline.text()
        self.strenghtlineo.setText(strenText)
        
        self.CO3o = QLabel('CO3')
        self.CO3INo = QLineEdit()
        self.HCO3o = QLabel('HCO3')
        self.HCO3INo = QLineEdit()
        
        o3 = self.CO3IN.text()
        ho3 = self.HCO3IN.text()
        self.CO3INo.setText(o3)
        self.HCO3INo.setText(ho3)
      
        self.CO3INo.setReadOnly(True)
        self.HCO3INo.setReadOnly(True)
        self.EluentButo = QLabel("Eluent")
        self.LeStatuso = QComboBox()

        elu = self.LeStatus.currentText()
        self.LeStatuso.addItem(elu)
        
        self.tempFo.addRow(self.EluentButo, self.LeStatuso)
        self.tempFo.addRow(self.Strengtho)
        self.tempFo.addRow(self.strenghtlineo)
        self.tempFo.addRow(self.CO3o, self.CO3INo )
        self.tempFo.addRow(self.HCO3o, self.HCO3INo)

        
        self.Group1o.setLayout(self.tempFo)##

        self.Group2o = QGroupBox()
        self.tempF2o = QVBoxLayout()#
        
        self.Choiceo = QRadioButton("Ion Chromatography")
        if self.Choice.isChecked():
            self.Choiceo.setChecked(True)
        
        self.Choice2o = QRadioButton("Ion Exclusion")
        if self.Choice2.isChecked():
            self.Choice2o.setChecked(True)


        self.StatusButo = QPushButton("Status")
        
        self.StatusButo.clicked.connect(self.Information)##############

        self.tempF2o.addWidget(self.Choiceo)
        self.tempF2o.addWidget(self.Choice2o)
        self.tempF2o.addWidget(self.StatusButo)

    
        self.Group2o.setLayout(self.tempF2o)##


        self.Group3o = QGroupBox()
        self.tempF3o = QFormLayout()#


        self.FlowRateo = QLabel("Flow Rate (ml/min)")
        
        self.FlowIno = QLineEdit()
        flow = self.FlowIn.text()
        self.FlowIno.setText(flow)
        self.FlowIno.setReadOnly(True)

        self.Vol_labo = QLabel('Sample Volume(uL)')
        self.Vol_lino = QComboBox()
        vol = self.Vol_lin.currentText()
        self.Vol_lino.addItem(vol)
        

        self.Timeo = QLabel("Expt. Time (min)")
        self.TimeIno = QComboBox()
        tim = self.TimeIn.currentText()
        self.TimeIno.addItem(tim)


        self.DetailsButo = QPushButton("Details")
        self.DetailsButo.clicked.connect(self.DETAILS)


        self.savButo = QPushButton("File Destination")
        self.savButo.setEnabled(False)
        
        self.savNameo = QLineEdit()
        self.savNameo.setReadOnly(True)
        self.savNameo.setText(self.savName.text())

        self.tempF3o.addRow(self.Vol_labo, self.Vol_lino)
        self.tempF3o.addRow(self.FlowRateo, self.FlowIno)
        self.tempF3o.addRow(self.Timeo, self.TimeIno)
        self.tempF3o.addRow(self.DetailsButo,)
        self.tempF3o.addRow(self.savButo,)
        self.tempF3o.addRow(self.savNameo,)
        
        self.Group3o.setLayout(self.tempF3o)
        
        self.OverLay_online = QPushButton('Overlay')
        self.Group4o = QGroupBox()
        self.tempF4o = QFormLayout()


        self.bgLabo = QLabel("                  CHECK BACKGROUND")
        self.bgTimeo = QLabel("Time (min)")
        self.bgTimeIno = QComboBox()

        Timi = self.bgTimeIn.currentText()

        self.bgTimeIno.addItem(Timi)
        
        self.StopButo = QPushButton("Stop")
        self.StopButo.clicked.connect(self.Quit_Mode2)

        self.backButo2 = QPushButton("Back")
        self.backButo2.setEnabled(False)
        self.backButo2.clicked.connect(self.Offline_Mode2)
        
        
        self.tempF4o.addRow(self.bgLabo)
        self.tempF4o.addRow(self.bgTimeo, self.bgTimeIno)
        self.tempF4o.addRow(self.StopButo)
        self.tempF4o.addRow(self.backButo2)

        self.Group4o.setLayout(self.tempF4o)

        self.Group5o = QGroupBox()
        self.tempF5o = QVBoxLayout()

                
        self.backButo = QPushButton("Back")
        self.backButo.setEnabled(False)
        self.SaveButo = QPushButton("Save")
        self.QuitButo = QPushButton("STOP")

        #self.Message = QLabel("Please Do not disturb\n the setup or the application")
        #self.SaveButo.clicked.connect(self.SaveData)
        self.backButo.clicked.connect(self.Offline_Mode2)
        self.QuitButo.clicked.connect(self.Quit_Mode)
        
        for i in [self.backButo, self.SaveButo, self.QuitButo]:
            self.tempF5o.addWidget(i)

        self.OverLay_online = QPushButton('Overlay')
        self.OverLay_online.clicked.connect(self.On_2_Over)

        self.Group5o.setLayout(self.tempF5o)

        self.FinalGroup1o = QGroupBox()
        self.OneSideo = QVBoxLayout()####

        for i in [self.Group2o, self.Group1o, self.Group3o, self.Group4o, self.Group5o, self.OverLay_online]:
            self.OneSideo.addWidget(i)
        
        self.OneSideo.addStretch(1)
        

        self.FinalGroup1o.setLayout(self.OneSideo)##
        self.FinalGroup1o.setMaximumWidth(190)
        
        self.canvas3 = FigureCanvas(f2)
        self.Tb3 = NavigationToolbar(self.canvas3, self)

        self.Group6o = QGroupBox()
        self.tempF26o = QVBoxLayout()
        self.tempF26o.addWidget(self.canvas3)
        self.tempF26o.addWidget(self.Tb3)

        self.ani2 = animation.FuncAnimation(f2, animate2, interval=1000)

        self.Group6o.setLayout(self.tempF26o)
        
        self.StartPage_Widget = QWidget()
        self.StartPage_Layout = QHBoxLayout()

        self.StartPage_Layout.addWidget(self.FinalGroup1o)
        self.StartPage_Layout.addWidget(self.Group6o)
        self.StartPage_Widget.setLayout(self.StartPage_Layout)


    def START(self):
        self.timeStart = time.time()
        int1 = int(self.TimeIn.currentText())
        
        Details_of_exp = ''
        #log_extra_det = ''
        datetime = QtCore.QDate.currentDate()
        
        #CHANGE SIGNAL HERE
        Valve_Signal = serial.Serial('COM1',57600,timeout=1)
        #print("OKAY")
        t1 = time.time()
        dts = 1
        while(dts):
            Valve_Signal.write(b'B')
            #Valve_Signal.write(b'1000')
            #Valve_Signal.write(b'\r')
              
            signal_string_encoded = Valve_Signal.readline()
            
            signal = signal_string_encoded.decode()
            
            signal2 = signal.strip()
    
            Status = 'Command B : Valve status OPEN'
            t2 = time.time()
            if(Status==signal2):
                continue
            elif(signal2=='Command B : Valve status CLOSE'):
                Valve_Signal.close()
                self.t1 = input_new_device.thread_with_exception(int1, 1)
                self.StartPage()
                self.stacked_layout.addWidget(self.StartPage_Widget)
                self.stacked_layout.setCurrentWidget(self.StartPage_Widget)


                logFile = open('Log.txt', 'w+')
                logFile.seek(0,0)

                type_Ion = ''
                
                if(self.Choice.isChecked()):
                    type_Ion = 'IC\n'
                else:
                    type_Ion = 'IE\n'
                    
                try:
                    pass
                    #log_extra_det = open('LogDetails.txt').read()
                except:
                    pass
                Details_of_exp = 'Eluent:' +self.LeStatus.currentText() +'\n Strength :' + self.strenghtline.text()+'\n Flow Rate:' + self.FlowIn.text() + '\n Sample Volume:'+ self.Vol_lin.currentText()+'\n\n'

                
                logFile.write(datetime.toString(Qt.DefaultLocaleLongDate)+'\n'+'\n')
                logFile.write(type_Ion)
                logFile.write(self.fileNameSA + '\n\n')  
                logFile.write(Details_of_exp +'\n')
                logFile.close()
                self.t1.start()
                break
            elif(t2-t1>=60):
                dts = 0
                Valve_Signal.close()
                break
            else:
                continue 

        try:
            self.StopButo.setEnabled(False)
            self.backButo2.hide()
            self.SaveButo.hide()
            self.QuitButo.setEnabled(True)
            self.StatusButo.setEnabled(True)
            self.DetailsButo.setEnabled(True)
            self.SaveButo.setEnabled(True)
            try:
                self.button.setEnabled(False)
            except:
                pass
        except:
            pass
                
    def BACKGROUND(self):
        
        int2 = int(self.bgTimeIn.currentText())
        
        self.t2 = input_new_device.thread_with_exception(int2, 0)    
        try:
            self.stacked_layout.setCurrentWidget(self.StartPage_Widget)
        except:
            self.StartPage()
            self.stacked_layout.addWidget(self.StartPage_Widget)
            self.stacked_layout.setCurrentWidget(self.StartPage_Widget)

        try:
            self.StopButo.setEnabled(True)
            self.backButo.hide()
            self.backButo2.hide()
            self.SaveButo.hide()
            self.QuitButo.setEnabled(False)
            self.StatusButo.setEnabled(False)
            self.DetailsButo.setEnabled(False)
        except:
            pass        
        self.t2.start()
        
    def Online_Mode(self):

        #If the Widget for Online settings page already exist, raise it
            #for display
        try:
            self.stacked_layout.setCurrentWidget(self.view_mode_widget)
            self.startBut.setEnabled(False)

        #Else initiate the page, add it's widget in stack and raise it
            #for display
        except:
            self.OnlineSetting_Page()
            self.stacked_layout.addWidget(self.view_mode_widget)
            self.stacked_layout.setCurrentWidget(self.view_mode_widget)
            
        
    def Offline_Mode(self):
        self.stacked_layout.setCurrentIndex(0)
        try:
            self.startBut.setEnabled(False)
        except:
            pass
    def Offline_Mode2(self):
        a3.clear()
        clear_showFile = open("Logs/Data_input.txt", 'w')
        clear_showFile.write('')
        clear_showFile.close()
        self.backButo.setEnabled(False)
        self.backButo2.setEnabled(False)
        self.startBut.setEnabled(False)
        
        self.stacked_layout.setCurrentWidget(self.view_mode_widget)


        
    def SaveDataLoc(self):
        try:
            self.fileNameSA,_ = QFileDialog.getSaveFileName(self, 'Save', '', '*.txt')
            file = open(self.fileNameSA, 'w+')
            file.write("")
            file.close()
            self.savName.setText(self.fileNameSA)
        except:
            pass
        

    def Quit_Mode(self):

        try:
            self.button.setEnabled(True)
        except:
            pass
            
        self.t1.raise_exception() 
        self.t1.join()
        try:
            log_extra_det = open('Logs/LogDetails.txt').read()
            log_addition = open('Logs/Log.txt', 'a+')
            log_addition.seek(0,0)
            log_addition.write('Extra Details\n' + log_extra_det)
            log_addition.close()
        except:
            pass
        file = open(self.fileNameSA, 'a+')
        pullDataSA = open("Log.txt", 'r').read()

        file.write(pullDataSA)
        file.close()

        try:
            log_det_clear = open("Logs/LogDetails.txt", 'w')
            log_det_clear.write("")
            log_det_clear.close()
        except:
            pass
        
        self.backButo.setEnabled(True)
        self.SaveButo.setEnabled(True)
        self.backButo2.setEnabled(True)
        try:
            self.BackButOV.setEnabled(True)
            self.Ov_fr_On.setEnabled(False)
        except:
            pass
        
    def Quit_Mode2(self):
    
        self.t2.raise_exception() 
        self.t2.join()
        
        self.backButo.setEnabled(True)
        self.backButo2.setEnabled(True)
        
        a3.clear()
        clear_showFile = open("Logs/Data_input.txt", 'w')
        clear_showFile.write('')
        clear_showFile.close()
        self.backButo.setEnabled(False)
        self.backButo2.setEnabled(False)
        
        self.stacked_layout.setCurrentWidget(self.view_mode_widget)

    def NewItem(self,):
        items = open("Logs/Eluent.txt", 'a+')
        ItemLabel, ok = QLineEdit(self, "New Eluent")
        input1 = getText(ItemLabel)
        items.write(input1)

    def gettext(self):
        if (self.LeStatus.currentIndex()==1):
            text, ok = QInputDialog.getText(self, 'New Entry', 'Enter Eluent Name :')
            if(text):
                self.LeStatus.addItem(text)
                new_entry = text
                items1 = open("Logs/Eluent.txt", 'a+')
                items1.write('\n'+new_entry)
                self.Strength.setEnabled(True)
                self.strenghtline.setReadOnly(False)
                self.CO3IN.setReadOnly(True)
                self.HCO3IN.setReadOnly(True)
                self.CO3IN.setText('')
                self.HCO3IN.setText('')
            
        elif (self.LeStatus.currentIndex()==5):
            self.CO3IN.setReadOnly(False)
            self.HCO3IN.setReadOnly(False)
            self.CO3IN.setText('0.0')
            self.HCO3IN.setText('0.0')
            self.Strength.setEnabled(False)
            self.startBut.setEnabled(False)
            self.strenghtline.setReadOnly(True)
            self.strenghtline.setText('')
            
        elif (self.LeStatus.currentIndex()==6):
            self.CO3IN.setReadOnly(True)
            self.HCO3IN.setReadOnly(True)
            self.Strength.setEnabled(False)
            self.strenghtline.setReadOnly(True)
            self.startBut.setEnabled(False)
            self.CO3IN.setText('')
            self.HCO3IN.setText('')
            self.strenghtline.setText('')
            
        elif(self.LeStatus.currentIndex()>6):
            self.Strength.setEnabled(True)
            self.strenghtline.setReadOnly(False)
            self.startBut.setEnabled(False)
            self.CO3IN.setReadOnly(True)
            self.HCO3IN.setReadOnly(True)
            self.CO3IN.setText('')
            self.HCO3IN.setText('')

        elif(self.LeStatus.currentIndex()==0):
            self.Strength.setEnabled(False)
            self.startBut.setEnabled(False)
            self.strenghtline.setReadOnly(True)
            self.strenghtline.setText('')

        else:
            self.CO3IN.setReadOnly(True)
            self.HCO3IN.setReadOnly(True)
            self.CO3IN.setText('')
            self.HCO3IN.setText('')
            self.startBut.setEnabled(False)
            self.Strength.setEnabled(True)
            self.strenghtline.setReadOnly(False)
            floww3 = self.FlowIn.text()
            timi6 = self.TimeIn.currentText()
            self.startBut.setEnabled(False)
            self.strenghtline.setText('')

    def disable(self):
        if self.Choice.isChecked():
            pass
        elif self.Choice2.isChecked():
            self.LeStatus.setCurrentIndex(6)
            self.Strength.setEnabled(False)
            self.strenghtline.setReadOnly(True)
        else:
            pass

    def Information(self):
        timeRemaining = 0.0
        timeElapsed = time.time()
        DataInfo = open("Logs/Input_Coeff.txt", 'r').readline()

        
        DataInfoList = DataInfo.split()
        
        capa = float(DataInfoList[1])
        exhus = 0.000
        if (True):
            try:
                if (self.LeStatus.currentIndex() != 0 and self.LeStatus.currentIndex() != 6):
                    
                    stren = float(self.strenghtline.text())
                    
                    flow = float(self.FlowIn.text())

                    if (self.LeStatus.currentIndex() == 2 or self.LeStatus.currentIndex()==4):
                        exhus = capa/(stren*0.001)
                        self.exhusTime = exhus/60
                        
                    elif (self.LeStatus.currentIndex()== 3):
                        exhus = capa/(stren*0.002)
                        self.exhusTime = exhus/60

                    elif(self.LeStatus.currentIndex()== 5):
                        try:
                            co3str = float(self.CO3IN.text())
                            hcostr = float(self.HCO3IN.text())
                            exhus = capa/((co3str*0.002)+(hcostr*0.001))
                            self.exhusTime = exhus/60
                        except:
                            pass
                    else:
                        pass
            except:
                pass
            
        try:
            timeElapsed2 = (timeElapsed - self.timeStart)/(60*60)
            timeRemaining = (self.exhusTime - timeElapsed2)
        except:
            timeRemaining = (self.exhusTime)
            pass
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Suppressor Column Status")
        msg.setInformativeText("If time remaining is less than half an hour please go for regeneration.")
        msg.setWindowTitle("Suppressor Status")
        msg.setDetailedText("The details are as follows: \n Eluent being used: %s\n Strength of the Eluent : %s\n Capacity of column: %f\n Total Exhustion time: %f hrs \n Time Remaining: %f hrs" %(self.LeStatus.currentText(), self.strenghtline.text(), capa, self.exhusTime, timeRemaining))

        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.show()
        msg.exec_()
        
    def getint(self):
        index = self.TimeIn.currentIndex()
        dest = self.savName.text()
        floww = self.FlowIn.text()
        stre = self.strenghtline.text()
        elu = self.LeStatus.currentIndex()
        vol = self.Vol_lin.currentText()

        try:
            flow = float(floww)            
            volm = float(vol)
        except:
            flow = 0
            volm = 0
            
        if (index==1):
            num,ok = QInputDialog.getInt(self,"Set Time","Enter a Time Domain")
            numstr = str(num)
            if (numstr != '0' ):
                #self.TimeIn.addItem(numstr)
                self.TimeIn.setItemText(0, numstr)

        elif (index!=0 and elu >1 and dest != '' and flow >0 and volm >0):
            if(elu == 5):
                try:
                    co3In = float(self.HCO3IN.text())
                    hcoIn = float(self.CO3IN.text())
                    if(co3In>0 and hcoIn>0):
                        self.startBut.setEnabled(True)
                except:
                    self.startBut.setEnabled(False)
            elif(elu == 6):
                self.startBut.setEnabled(True)

            else:
                stren = float(stre)
                if(stren>0):
                    self.startBut.setEnabled(True)
                    
        elif(index==0 and dest != ''):
            numt = self.TimeIn.currentText()
            try:
                numtt = float(numt)
                self.startBut.setEnabled(True)
            
            except:
                self.startBut.setEnabled(False)
                pass
        else:
            self.startBut.setEnabled(False)

    def getint2(self):
        index = self.bgTimeIn.currentIndex()
        if (index==1):
            num,ok = QInputDialog.getInt(self,"Set Time","Enter a Time Domain")
            numstr = str(num)
            if (numstr != '0' ):
                #self.TimeIn.addItem(numstr)
                self.bgTimeIn.setItemText(0, numstr)

        elif(index==0):
            numt = self.bgTimeIn.currentText()
            try:
                numtt = float(numt)
                self.okBut.setEnabled(True)
                
            except:
                self.okBut.setEnabled(False)
           
                pass
        elif (index !=1 and index !=0):
            self.okBut.setEnabled(True)


    def Check_start_condition(self):
        index = self.TimeIn.currentText()
        stren = self.strenghtline.text()
        hco3In = self.HCO3IN.text()
        co3In = self.CO3IN.text()
        floww2 = self.FlowIn.text()
        elu_dex = self.LeStatus.currentIndex()
        vol = self.Vol_lin.currentText()
        volm = 0
        try:
            time_check = float(index)
            floNum2 = float(floww2)
            dest_name = self.savName.text()
            volm = float(vol)
            if(dest_name=='' or floNum2 ==0 or time_check == 0 or volm== 0):
                self.startBut.setEnabled(False)
                
            elif(elu_dex == 5):
                try:
                    hco3In_check = float(hco3In)
                    co3In_check = float(co3In)
                    if(hco3In_check > 0 and co3In_check > 0 and floNum2 > 0 and time_check > 0 and volm > 0):
                        self.startBut.setEnabled(True)
                except:
                    self.startBut.setEnabled(False)
                    pass
                
            elif(elu_dex !=5 and elu_dex !=0 and elu_dex != 6):
                try:
                    stren_check = float(stren)
                    if(stren_check > 0 and floNum2 >0 and time_check > 0):
                        self.startBut.setEnabled(True)
                except:
                    self.startBut.setEnabled(False)
                    pass
            elif(elu_dex == 6):
                try:
                    if(floNum2 < 0 or time_check < 0 or volm < 0):
                        self.startBut.setEnabled(False)
                    else:
                        self.startBut.setEnabled(True)
                except:
                    self.startBut.setEnabled(False)
                    pass
        except:
            self.startBut.setEnabled(False)
         
    def DETAILS(self):

        self.w = QDialog()
        self.w.resize(200,200)
        self.lay = QVBoxLayout(self.w)
        self.textBox = QPlainTextEdit()
        self.textBox.resize(200,200)
        datetime = QtCore.QDate.currentDate()
        try:
            det_file = open('Logs/LogDetails.txt').read()
            if det_file =='':
                self.textBox.insertPlainText(datetime.toString(Qt.DefaultLocaleLongDate)+'\n'+'\n')
                pass
            else:
                self.textBox.insertPlainText(det_file)
        except:
            self.textBox.insertPlainText(datetime.toString(Qt.DefaultLocaleLongDate)+'\n'+'\n')
            
        self.label = QLabel('Provide Details here')
        self.button = QPushButton("SAVE")
        self.button.clicked.connect(self.saveInLog)

        self.lay.addWidget(self.label)
        self.lay.addWidget(self.textBox)
        self.lay.addWidget(self.button)
        self.w.setWindowModality(Qt.ApplicationModal)
        self.w.setWindowTitle("Details")
        self.w.setWindowIcon(QIcon("ClientIcon.ico"))
        self.w.show()
        self.w.exec_()

    def saveInLog(self):
        if(self.textBox.toPlainText()):
            f = open('Logs/LogDetails.txt', 'w+')
            details = self.textBox.toPlainText()
            f.write(details+'\n')
            f.close()
            
    def getstrength(self):
        numStgt,ok = QInputDialog.getInt(self,"Set Strength","Enter a strength")
        numstr44 = str(numStgt)
        floww = self.FlowIn.text()
        timi = self.TimeIn.currentText()
        self.startBut.setEnabled(False)
        try:
            floNum78 = float(floww)
            timinum = int(timi)
            self.startBut.setEnabled(True)
        except:
            pass
           
        if (ok and numstr44 != '0' ):
            self.strenghtline.setText(numstr44)


    
        
    def ReviewMode(self):
        try:
            self.stacked_layout.setCurrentWidget(self.ReviewPage_widget)

        except:
            self.ReviewPage()
            self.stacked_layout.addWidget(self.ReviewPage_widget)
            self.stacked_layout.setCurrentWidget(self.ReviewPage_widget)
        
    def On_2_Over(self):
        try:
            self.BackButOV.setEnabled(False)
            self.Ov_fr_On.setEnabled(True)
            self.stacked_layout.setCurrentWidget(self.OverlayPage_widget)
        except:
            self.Overlay()
            self.Ov_fr_On.setEnabled(True)
            self.BackButOV.setEnabled(False)
            self.stacked_layout.addWidget(self.OverlayPage_widget)
            self.stacked_layout.setCurrentWidget(self.OverlayPage_widget)
            

    def Ove_2_On(self):
        self.Ov_fr_On.setEnabled(False)
        self.stacked_layout.setCurrentWidget(self.StartPage_Widget)
        
    def ReviewPage(self):

        self.File1 = QPushButton("Browse file")
        self.File1.clicked.connect(self.fileInput)

        self.clearR = QPushButton("Clear")
        self.clearR.setEnabled(False)
        
        self.clearR.clicked.connect(self.clearFile)
        self.TEXT_BOX_R = QPlainTextEdit()
        self.TEXT_BOX_R.setReadOnly(True)
        self.AreaBox = QLineEdit()
        self.AreaBox.setReadOnly(True)
        self.Area_lab = QLabel()
        self.Area_lab.setText(" AREA : ")
        
        self.ex1R = QVBoxLayout()
        self.ex1grpR = QGroupBox()

        for x in [self.File1, self.clearR, self.TEXT_BOX_R, self.Area_lab, self.AreaBox]:
            self.ex1R.addWidget(x)
        
        self.ex1grpR.setLayout(self.ex1R)
        #self.ex1R.addStretch(0.5)
        
        self.BackButR = QPushButton("Back")
        self.BackButR.clicked.connect(self.Offline_Mode)
        self.OverlayButR = QPushButton("Overlay")
        self.OverlayButR.clicked.connect(self.OverlayMode)
        self.Calib_butR = QPushButton("Calibration")
        self.Calib_butR.clicked.connect(self.Calib_Mode)

        self.ex3R = QVBoxLayout()
        self.ex3grpR = QGroupBox()
                
        self.ex3R.addWidget(self.OverlayButR)
        self.ex3R.addWidget(self.Calib_butR)
        self.ex3R.addWidget(self.BackButR)
        
        self.ex3grpR.setLayout(self.ex3R)
        self.ex3R.addStretch(1)
                
        self.tempWidR = QGroupBox()
        self.tempLay1R = QVBoxLayout()

        for x in [self.ex1grpR, self.ex3grpR]:
            self.tempLay1R.addWidget(x)
        
        self.tempWidR.setMaximumWidth(190)
        self.tempWidR.setLayout(self.tempLay1R)
            
        self.tempWid2R = QGroupBox()
        self.tempLay2R = QVBoxLayout()

                
        self.canvas1R = FigureCanvas(Figure(figsize=(10,10), dpi=100))
        self.tempLay2R.addWidget(self.canvas1R)
        self.Tb1R = NavigationToolbar(self.canvas1R, self)
        self.tempLay2R.addWidget(self.Tb1R,)
        
        self.ax1R = self.canvas1R.figure.subplots()
        self.ax1R.set_title("CHROMATOGRAM")
        self.ax1R.set_ylabel('k / uScm-1')
        self.ax1R.set_xlabel('Time / mins')
        #self.ax1R.legend(loc="best")
        
        cid = self.canvas1R.mpl_connect('button_press_event', self.onclick)
        cid2 = self.canvas1R.mpl_connect('button_release_event', self.click_release)

        

        self.tempWid2R.setLayout(self.tempLay2R)

        self.Mode_layoutR = QGridLayout()
            
        self.Mode_layoutR.addWidget(self.tempWidR, 1,1)
        self.Mode_layoutR.addWidget(self.tempWid2R, 1,3)

                
         #defining widget for the stack:
        
        self.ReviewPage_widget = QWidget()
        self.ReviewPage_widget.setLayout(self.Mode_layoutR)
        self.ReviewPage_widget.setGeometry(100,100,200,200)
        self.ReviewPage_widget.setWindowTitle("Review Mode")

    def onclick(self, event):

        self.X1 = 0.0
        self.Y1 = 0.0
        self.X1 = event.xdata
        self.Y1 = event.ydata
        
    def click_release(self, event):

        self.X2 = 0
        self.Y2 = 0
        try:
            self.X2 = event.xdata
            self.Y2 = event.ydata
        except:
            pass
        area = 0
        for x in range(len(self.xlist1R)):
            try:
                if(self.xlist1R[x] >= float(self.X1) and self.xlist1R[x] <= float(self.X2)):
                    area += 0.5*(((self.xlist1R[x+1]-self.xlist1R[x])*60)*(self.ylist1R[x]+self.ylist1R[x+1]))
            except:
                pass
            
        if(area>0):
            area_new = area-(0.5*(((float(self.X2)-float(self.X1))*60)*(float(self.Y1)+float(self.Y2))))
            
            if(area_new>=0):
                self.AreaBox.setText(str("%.2f"%area_new))
                
                try:
                    self.line.remove()
                except:
                    pass
                
                x_vals = [self.X1, self.X2]
                y_vals = [self.Y1, self.Y2]
                self.line, = self.ax1R.plot(x_vals, y_vals, 'red')
                self.canvas1R.draw_idle()
        
    def fileInput(self):
        try:
            self.clearR.setEnabled(True)
            fileName, _ = QFileDialog.getOpenFileName(self, 'Single File', QDir.rootPath() , '*.txt')
            addedData = open(fileName, 'r').read()
            dataList1R = addedData.split('\n')
            Details1R = ''
            self.xlist1R = []
            self.ylist1R = []
            
            for eachLine in dataList1R :
                    try:
                        x1R, y1R = eachLine.split()
                        self.xlist1R.append(float(x1R))
                        freq = float(y1R)
                        k = freq
                        self.ylist1R.append(float(k))                        
                        
                    except:
                        Details1R += eachLine+'\n'
                        pass
                    
            try:
                self.Main.remove()
                self.line.remove()
                self.TEXT_BOX_R.setPlainText('')
                self.AreaBox.setText('')
            except:
                pass
            self.TEXT_BOX_R.setPlainText(str(Details1R))

            self.arry_Y = np.asarray(self.ylist1R)
            
            self.Main, = self.ax1R.plot(self.xlist1R, self.ylist1R, 'blue')
            self.canvas1R.draw_idle()
        except:
            pass


    def clearFile(self):
        try:
            self.ax1R.clear()
            self.AreaBox.setText('')
            self.ax1R.set_title("CHROMATOGRAM")
            self.ax1R.set_ylabel('k / uScm-1')
            self.ax1R.set_xlabel('Time / mins')
            self.TEXT_BOX_R.setPlainText('')
            self.canvas1R.draw_idle()
        except:
            pass

    def OverlayMode(self):
        try:
            self.stacked_layout.setCurrentWidget(self.OverlayPage_widget)
        except:
            self.Overlay()
            self.stacked_layout.addWidget(self.OverlayPage_widget)
            self.stacked_layout.setCurrentWidget(self.OverlayPage_widget)
        self.BackButOV.setEnabled(True)
        self.Ov_fr_On.setEnabled(False)
            
    def Overlay(self):

        icon = QIcon(QPixmap('Media/close_bluei.png'))
        
        self.File1OV = QPushButton("Browse file 1")
        self.File1OV.clicked.connect(self.fileInputOV)

        self.File2OV = QPushButton("Browse file 2")
        self.File2OV.clicked.connect(self.fileInputOV2)

        self.File3OV = QPushButton("Browse file 3")
        self.File3OV.clicked.connect(self.fileInputOV3)
        
        self.File4OV = QPushButton("Browse file 4")
        self.File4OV.clicked.connect(self.fileInputOV4)

        self.File5OV = QPushButton("Browse file 5")
        self.File5OV.clicked.connect(self.fileInputOV5)
        
        self.ex1OV = QVBoxLayout()
        self.ex1grpOV = QGroupBox()
        
        for i in [self.File1OV, self.File2OV, self.File3OV, self.File4OV, self.File5OV]:
            self.ex1OV.addWidget(i) 
        
        self.ex1grpOV.setLayout(self.ex1OV)
        #self.ex1OV.addStretch(0.5)

        self.Group_OV = QGroupBox()
        self.tempF_OV = QGridLayout()

        self.Blu = QLabel('Blu')
        self.Blu_line = QLineEdit()
        self.Blu_line.setReadOnly(True)
        self.Blu_D = QPushButton('D')
        self.Blu_C = QPushButton()
        self.Blu_C.setIcon(icon)

        self.Gre = QLabel('Grn')
        self.Gre_line = QLineEdit()
        self.Gre_line.setReadOnly(True)
        self.Gre_D = QPushButton('D')
        self.Gre_C = QPushButton()
        self.Gre_C.setIcon(icon)

        self.Red = QLabel('Red')
        self.Red_line = QLineEdit()
        self.Red_line.setReadOnly(True)
        self.Red_D = QPushButton('D')
        self.Red_C = QPushButton()
        self.Red_C.setIcon(icon)

        self.Blc = QLabel('Blk')
        self.Blc_line = QLineEdit()
        self.Blc_line.setReadOnly(True)
        self.Blc_D = QPushButton('D')
        self.Blc_C = QPushButton()
        self.Blc_C.setIcon(icon)

        self.Org = QLabel('Org')
        self.Org_line = QLineEdit()
        self.Org_line.setReadOnly(True)
        self.Org_D = QPushButton('D')
        self.Org_C = QPushButton()
        self.Org_C.setIcon(icon)

        self.Text_OV = QPlainTextEdit()
        self.Text_OV.setReadOnly(True)

        for i,j in zip([self.Blu_line, self.Gre_line, self.Red_line, self.Blc_line, self.Org_line],
                     [self.Blu_D, self.Gre_D, self.Red_D, self.Blc_D, self.Org_D]):
            i.setMinimumWidth(70)
            j.setMaximumWidth(25)
            
            
        index = 0
        for i in [self.Blu, self.Gre, self.Red, self.Blc, self.Org]:
            self.tempF_OV.addWidget(i, index,0)
            index += 1

        index = 0
        for i in [self.Blu_line, self.Gre_line, self.Red_line, self.Blc_line, self.Org_line]:
            self.tempF_OV.addWidget(i, index,1,)
            index += 1

        index = 0
        for i, j in zip([self.Blu_D, self.Gre_D, self.Red_D, self.Blc_D, self.Org_D],
                        [self.det1, self.det2, self.det3, self.det4, self.det5]):
            self.tempF_OV.addWidget(i, index, 2)
            i.clicked.connect(j)
            i.resize(0.5,0.5)
            index += 1

        index = 0

        
        for i,j in zip([self.Blu_C, self.Gre_C, self.Red_C, self.Blc_C, self.Org_C],
                       [self.clr1, self.clr2, self.clr3, self.clr4, self.clr5]):
            self.tempF_OV.addWidget(i, index, 3)
            i.clicked.connect(j)
            index += 1

        
        self.Group_OV.setLayout(self.tempF_OV)

                
        self.BackButOV = QPushButton("Back")
        self.BackButOV.clicked.connect(self.Offline_Mode)
        #self.ReviewButOV = QPushButton("Review")
        #self.ReviewButOV.clicked.connect(self.ReviewMode)

        self.Ov_fr_On = QPushButton('Online')
        self.Ov_fr_On.clicked.connect(self.Ove_2_On)
        self.Ov_fr_On.setEnabled(False)
        
        self.ex3OV = QVBoxLayout()
        self.ex3grpOV = QGroupBox()

        for i in [self.BackButOV, self.Ov_fr_On]:
            self.ex3OV.addWidget(i)        
        
        
        self.ex3grpOV.setLayout(self.ex3OV)
        #self.ex3OV.addStretch(1)
                
        self.tempWidOV = QGroupBox()
        self.tempLay1OV = QVBoxLayout()

        for i in [self.ex1grpOV, self.Group_OV, self.Text_OV, self.ex3grpOV]:
            self.tempLay1OV.addWidget(i)

        self.tempWidOV.setMaximumWidth(200)
        self.tempWidOV.setLayout(self.tempLay1OV)
            
        self.tempWid2OV = QGroupBox()
        self.tempLay2OV = QVBoxLayout()
                
        self.canvas1OV = FigureCanvas(Figure(figsize=(20,20), dpi=100))
        self.tempLay2OV.addWidget(self.canvas1OV)
        self.Tb1OV = NavigationToolbar(self.canvas1OV, self)
        self.tempLay2OV.addWidget(self.Tb1OV,)

        self.ax1OV = self.canvas1OV.figure.subplots()
        self.ax1OV.set_title("CHROMATOGRAM")
        self.ax1OV.set_ylabel('k / uScm-1')
        self.ax1OV.set_xlabel('Time / mins')
        

        self.tempWid2OV.setLayout(self.tempLay2OV)
        #self.tempWid3OV.setLayout(self.tempLay3OV)

        self.Mode_layoutOV = QGridLayout()
            
        self.Mode_layoutOV.addWidget(self.tempWidOV, 1,1)
        self.Mode_layoutOV.addWidget(self.tempWid2OV, 1,3)
        #self.Mode_layoutOV.addWidget(self.tempWid3OV, 1,4)
                
         #defining widget for the stack:
        
        self.OverlayPage_widget = QWidget()
        self.OverlayPage_widget.setLayout(self.Mode_layoutOV)
        self.OverlayPage_widget.setGeometry(100,100,200,200)
        self.OverlayPage_widget.setWindowTitle("Overlay Mode")
        

    def fileInputOV(self):
        try:
            fileNameOV, _ = QFileDialog.getOpenFileName(self, 'Single File', QDir.rootPath() , '*.txt')
            self.canvas1OV.addedData = open(fileNameOV, 'r').read()
            dataList1OV = self.canvas1OV.addedData.split('\n')
            xlist1OV = []
            ylist1OV = []
            self.Details_1OV = fileNameOV+'\n\n\n'
            
            for eachLine in dataList1OV :
                    try:
                        x1OV, y1OV = eachLine.split()
                        xlist1OV.append(float(x1OV))
                        freq = float(y1OV)
                        k = (c1*freq*freq*freq + c2*freq*freq + c3*freq + c4)
                        ylist1OV.append(float(freq))
                    except:
                        self.Details_1OV += eachLine+'\n'
                        pass
            try:
                self.ln1.remove()
            except:
                pass

            self.ln1, = self.ax1OV.plot(xlist1OV, ylist1OV, 'blue',)
            self.Text_OV.setPlainText(str(self.Details_1OV))
            self.Blu_line.setText(fileNameOV)
            self.canvas1OV.draw_idle()
        except:
            pass
        
    def clr1(self):
        try:
            self.ln1.remove()
            self.Blu_line.setText('')
            self.Details_1OV = ''
            self.canvas1OV.draw_idle()
        except:
            pass

    def det1(self):
        try:
            self.Text_OV.setPlainText(str(self.Details_1OV))
        except:
            pass
        
    def det2(self):
        try:
            self.Text_OV.setPlainText(str(self.Details_2OV))
        except:
            pass
        
    def det3(self):
        try:
            self.Text_OV.setPlainText(str(self.Details_3OV))
        except:
            pass
        
    def det4(self):
        try:
            self.Text_OV.setPlainText(str(self.Details_4OV))
        except:
            pass
        
    def det5(self):
        try:
            self.Text_OV.setPlainText(str(self.Details_5OV))
        except:
            pass
    
    def fileInputOV2(self):
        try:
            fileName2OV, _ = QFileDialog.getOpenFileName(self, 'Single File', QDir.rootPath() , '*.txt')
            self.canvas1OV.addedData = open(fileName2OV, 'r').read()
            dataList2OV = self.canvas1OV.addedData.split('\n')
            xlist2OV = []
            ylist2OV = []
            self.Details_2OV = fileName2OV + '\n\n\n'
            for eachLine in dataList2OV :
                    try:
                        x2OV, y2OV = eachLine.split()
                        xlist2OV.append(float(x2OV))
                        freq = float(y2OV)
                        k = (c1*freq*freq*freq + c2*freq*freq + c3*freq + c4)
                        ylist2OV.append(float(freq))
                    except:
                        self.Details_2OV += eachLine+'\n'
                        pass
            try:
                self.ln2.remove()
            except:
                pass
            
            self.ln2, = self.ax1OV.plot(xlist2OV, ylist2OV, 'green',)
            self.Gre_line.setText(fileName2OV)
            self.canvas1OV.draw_idle()
        except:
            pass

    def clr2(self):
        try:
            self.ln2.remove()
            self.Gre_line.setText('')
            self.Details_2OV = ''
            self.canvas1OV.draw_idle()
        except:
            pass
        
    def fileInputOV3(self):
        try:
            fileName3OV, _ = QFileDialog.getOpenFileName(self, 'Single File', QDir.rootPath() , '*.txt')
            self.canvas1OV.addedData = open(fileName3OV, 'r').read()
            dataList3OV = self.canvas1OV.addedData.split('\n')
            xlist3OV = []
            ylist3OV = []
            self.Details_3OV = fileName3OV+'\n\n\n'
            for eachLine in dataList3OV :
                    try:
                        x3OV, y3OV = eachLine.split()
                        xlist3OV.append(float(x3OV))
                        freq = float(y3OV)
                        k = (c1*freq*freq*freq + c2*freq*freq + c3*freq + c4)
                        ylist3OV.append(float(freq))
                    except:
                        self.Details_3OV += eachLine+'\n'
                        pass
            try:
                self.ln3.remove()
            except:
                pass
            self.Red_line.setText(fileName3OV)
            self.ln3, = self.ax1OV.plot(xlist3OV, ylist3OV, 'red',)
            self.canvas1OV.draw_idle()
        except:
            pass
        
    
    def clr3(self):
        try:
            self.ln3.remove()
            self.Red_line.setText('')
            self.Details_3OV = ''
            self.canvas1OV.draw_idle()
        except:
            pass

            
    def fileInputOV4(self):
        try:
            fileName4OV, _ = QFileDialog.getOpenFileName(self, 'Single File', QDir.rootPath() , '*.txt')
            self.canvas1OV.addedData = open(fileName4OV, 'r').read()
            dataList4OV = self.canvas1OV.addedData.split('\n')
            xlist4OV = []
            ylist4OV = []
            self.Details_4OV = fileName4OV+'\n\n\n'
            for eachLine in dataList4OV :
                    try:
                        x4OV, y4OV = eachLine.split()
                        xlist4OV.append(float(x4OV))
                        freq = float(y4OV)
                        k = (c1*freq*freq*freq + c2*freq*freq + c3*freq + c4)
                        ylist4OV.append(float(freq))
                    except:
                        self.Details_4OV += eachLine+'\n'
                        pass
            try:
                self.ln4.remove()
            except:
                pass
            
            self.ln4, = self.ax1OV.plot(xlist4OV, ylist4OV, 'black',)
            self.Blc_line.setText(fileName4OV)
            self.canvas1OV.draw_idle()
        except:
            pass
        
    def clr4(self):
        try:
            self.ln4.remove()
            self.Blc_line.setText('')
            self.Details_4OV = ''
            self.canvas1OV.draw_idle()
        except:
            pass

    def fileInputOV5(self):
        try:
            fileName5OV, _ = QFileDialog.getOpenFileName(self, 'Single File', QDir.rootPath() , '*.txt')
            self.canvas1OV.addedData = open(fileName5OV, 'r').read()
            dataList5OV = self.canvas1OV.addedData.split('\n')
            xlist5OV = []
            ylist5OV = []
            self.Details_5OV = fileName5OV+'\n\n\n'
            for eachLine in dataList5OV :
                    try:
                        x5OV, y5OV = eachLine.split()
                        xlist5OV.append(float(x5OV))
                        freq = float(y5OV)
                        k = (c1*freq*freq*freq + c2*freq*freq + c3*freq + c4)
                        ylist5OV.append(float(k))
                    except:
                        self.Details_5OV += eachLine+'\n'
                        pass
            try:
                self.ln5.remove()
            except:
                pass
            
            self.ln5, = self.ax1OV.plot(xlist5OV, ylist5OV, 'orange',)
            self.Org_line.setText(fileName5OV)
            self.canvas1OV.draw_idle()
        except:
            pass
        
    def clr5(self):
        try:
            self.ln5.remove()
            self.Org_line.setText('')
            self.Details_5OV = ''
            self.canvas1OV.draw_idle()
        except:
            pass


    def Calib_Mode(self):
        try:
            self.stacked_layout.setCurrentWidget(self.CalibPage_widget)
        except:
            self.Cal_Page()
            self.stacked_layout.addWidget(self.CalibPage_widget)
            self.stacked_layout.setCurrentWidget(self.CalibPage_widget)
            
    def Cal_Page(self):
        
        self.table = QTableWidget(14,10)
        self.slopes = []
        index = 1
        for i in range(0,10):
            if(i%2!=0):
                self.table.setCellWidget(0,i, QPushButton('Area'))
                self.table.setCellWidget(11,i, QLineEdit())
                self.table.setCellWidget(12,i, QLineEdit())
                uni = self.table.cellWidget(11,i)
                uni.setReadOnly(True)
                self.table.setCellWidget(13,i, QPushButton('Details'))
                det = self.table.cellWidget(13,i)
                det.clicked.connect(self.details_cal)
            else:
                self.table.setCellWidget(0,i, QPushButton('Analyte'+ str(index)))
                Ana = self.table.cellWidget(0,i)
                Ana.clicked.connect(self.AnalyteName)

                self.table.setCellWidget(11,i, QPushButton('Unit'))
                self.table.setCellWidget(12,i, QPushButton('Calibrate'))
                self.table.setCellWidget(13,i, QPushButton('Plot'))
                
                index = index+1
                Cal = self.table.cellWidget(12,i)
                Cal.clicked.connect(self.Line_Reg)
                uni = self.table.cellWidget(11,i)
                uni.clicked.connect(self.Units_cal)
                plo = self.table.cellWidget(13,i)
                plo.clicked.connect(self.Plot_cal)
        #index = 0       
        for i in range(1,11):
            for j in range(0,10):
                self.table.setCellWidget(i,j, QLineEdit())
                if(j%2!=0):
                    cel = self.table.cellWidget(i,j)
                    cel.returnPressed.connect(self.Cell_activated)
            #index = index + 1

        ver = self.table.horizontalHeader()
        ver.setVisible(False)
        ver2 = self.table.verticalHeader()
        ver2.setVisible(True)
        
        self.grp1_cal = QGroupBox()
        self.temp1_cal = QVBoxLayout()

        self.temp1_cal.addWidget(self.table)
        self.canvas1_cal = FigureCanvas(Figure(figsize=(11,4), dpi=100))
        self.canvas1_cal.setMaximumHeight(400)
        self.temp1_cal.addWidget(self.canvas1_cal)
        self.Tb1_cal = NavigationToolbar(self.canvas1_cal, self)
        self.temp1_cal.addWidget(self.Tb1_cal,)

        self.ax2_cal = self.canvas1_cal.figure.subplots()
        
        self.grp1_cal.setLayout(self.temp1_cal)

        self.grp2_cal = QGroupBox()
        self.temp2_cal = QVBoxLayout()

        self.Review_cal = QPushButton('Review')
        self.Review_cal.clicked.connect(self.ReviewMode)
        self.Note_cal = QLabel('Notes :')
        self.Note_text_cal = QPlainTextEdit()
        self.Save_cal = QPushButton('Save')
        self.Save_cal.clicked.connect(self.SaveData)
        self.Back_cal = QPushButton('Back')
        self.Back_cal.clicked.connect(self.Offline_Mode)

        for i in [self.Review_cal, self.Note_cal, self.Note_text_cal, self.Save_cal, self.Back_cal]:
            self.temp2_cal.addWidget(i)

        self.grp2_cal.setMaximumWidth(190)
        self.grp2_cal.setLayout(self.temp2_cal)

        self.Page_Layout = QHBoxLayout()
        self.Page_Layout.addWidget(self.grp1_cal)
        self.Page_Layout.addWidget(self.grp2_cal)

        self.CalibPage_widget = QWidget()
        self.CalibPage_widget.setLayout(self.Page_Layout)
        self.CalibPage_widget.setGeometry(100,100,200,200)
        self.CalibPage_widget.setWindowTitle("Calibration")

    def AnalyteName(self):
        try:
            column = self.table.currentColumn()
            text, ok = QInputDialog.getText(self, 'Analyte Name', 'Enter Analyte Name :')
            if(text and ok):
                col = self.table.cellWidget(0,column)
                col.setText(text)
        except:
            pass
        
    def Units_cal(self):
        try:
            column = self.table.currentColumn()
            text, ok = QInputDialog.getText(self, 'Uints', 'Enter Units of Concentration :')
            if(text and ok):
                col = self.table.cellWidget(11,column+1)
                col.setText(text)
        except:
            pass
        
    def Line_Reg(self):
        x_data_cal = []
        y_data_cal = []
        column = self.table.currentColumn()
        for eachElement in self.slopes:
            try:
                a, b, c, d, e, f = eachElement.split()
                if(int(a)==int(column)):
                    self.slopes.remove(eachElement)
            except:
                pass

        for i in range(1,11):
            try:
                x = self.table.cellWidget(i,column)
                x1 = x.text()
                x_data_cal.append(float(x1))
                y = self.table.cellWidget(i,(column+1))
                y1 = y.text()
                y_data_cal.append(float(y1))
            except:
                pass
            #print(y, x)
        self.x_arr_cal = np.asarray(x_data_cal)
        self.y_arr_cal = np.asarray(y_data_cal)
        slope, intercept, r_value, p_value, std_err = stats.linregress(self.x_arr_cal, self.y_arr_cal)
        string = str(column)+" "+str("%.3f"%slope)+" "+str("%.3f"%intercept)+" "+str("%.3f"%r_value)+" "+str("%.3f"%p_value)+" "+str("%.3f"%std_err)
        self.slopes.append(string)
        col = self.table.cellWidget(12,(column+1))
        col.setText('x *'+str("%.3f"%slope)+' + '+'('+str("%.3f"%intercept)+')')
        
    
    def Plot_cal(self):
        column = self.table.currentColumn()
        x_data = []
        y_data = []

        Name = self.table.cellWidget(0,column)
        Name_analyte = Name.text()
        
        Uni = self.table.cellWidget(11,column+1)
        Unit = Uni.text()

        Equ = self.table.cellWidget(12,column+1)
        Equa = Equ.text()
        for eachElement in self.slopes:
            try:
                a, b, c, d, e, f = eachElement.split()
                if(int(a)==int(column)):
                    try:
                        self.ax2_cal.clear()
                    except:
                        pass
                    for i in range(1,11):
                        try:
                            x = self.table.cellWidget(i,column)
                            x1 = x.text()
                            x_data.append(float(x1))
                            y = self.table.cellWidget(i,(column+1))
                            y1 = y.text()
                            y_data.append(float(y1))
                        except:
                            pass
                    x_arr = np.asarray(x_data)
                    y_arr = np.asarray(y_data)

                    self.ax2_cal.set_ylabel('AREA')
                    self.ax2_cal.set_xlabel(Name_analyte +'/ '+Unit)

                    label_legend = 'R2: '+str("%.3f"%(float(d)**2))+'\nEq.:'+Equa
                    self.ln, = self.ax2_cal.plot(x_arr,x_arr*float(b)+float(c), label = label_legend)
                    self.ax2_cal.legend(loc= 'right', bbox_to_anchor=(1,.5), ncol=3, fancybox=True, shadow=True)
                    self.canvas1_cal.draw_idle()
                    self.Scatter, = self.ax2_cal.scatter(x_arr,y_arr)
                    self.canvas1_cal.draw_idle()
            except:
                pass
    def details_cal(self):
        column = self.table.currentColumn()
        column = column-1
        col = self.table.cellWidget(0,column)
        Name = col.text()
        Uni = self.table.cellWidget(11,column+1)
        Unit = Uni.text()
        data_used = ''
        for eachElement in self.slopes:
            try:
                a, b, c, d, e, f = eachElement.split()
                if(int(a)==int(column)):
                    try:
                        Det =" "+Name+"\n Slope = " +b+"\n intercept = "+c+"\n r_value = "+d+"\n R_squared = "+str("%.3f"%(float(d)**2))+"\n p_value = "+e+ "\n std_err = "+f
                        Det = Det + '\n Equation: '+'x *'+b+' + '+'('+c+')' +"\n\n\n"
                        try:
                            for i, j in zip(self.x_arr_cal, self.y_arr_cal):
                                data_used = data_used + str(i)+ "    "+ str(j)+ '\n'
                        except:
                            pass
                        Det = Det + 'Data Used:\n Con.('+Unit+') ' + 'Area\n\n' + data_used
                        self.Note_text_cal.setPlainText(Det)
                    except:
                        pass
            except:
                pass       

    def Cell_activated(self):
        column = self.table.currentColumn()
        row = self.table.currentRow()
        
        for eachElement in self.slopes:
            try:
                a, b, c, d, e, f = eachElement.split()
                if(int(a)==(column-1)):
                    try:
                        y = self.table.cellWidget(row,(column))
                        y1 = float(y.text())
                        x = "%.3f"%((y1-float(c))/(float(b)))
                        
                        x1 = self.table.cellWidget(row, (column-1))
                        x1.setText(str(x))
                    except:
                        pass
            except:
                pass
            
    def SaveData(self):
        try:
            fileNameCal,_ = QFileDialog.getSaveFileName(self, 'Save', '', '*.txt')
            if(fileNameSA):
                file = open(fileNameCal, 'w+')
                details = self.Note_text_cal.toPlainText()
                if(details):
                    file.write(details)
                file.close()
        except:
            pass 
        
               
def main():
    IonSim = QApplication(sys.argv)
    ionWind = IonWindow()
    ionWind.showMaximized()
    ionWind.raise_()
    IonSim.exec_()

main()
