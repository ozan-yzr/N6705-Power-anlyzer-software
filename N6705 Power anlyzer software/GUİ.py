# AUTHOR: OZAN YAZAR
# SFW VERSİON: 1.1
# 12.02.2021
from PyQt5 import QtWidgets,uic, QtGui,QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys,os
from PyQt5.QtWidgets import QMessageBox,QFileDialog,QLabel,QLineEdit
from timeit import default_timer as tim
from datetime import datetime
import threading
from VP_function import ch_queue,time_elapsed

ConfigurationGUİ=True # if false turn off the configuration gui
# Make chanel selection here if the configurationGUİ is set false
ch1=True
ch2=True
ch3=False
ch4=False
#----------------
GraphUpdateFreq=1000 # in millisecond 
pg.setConfigOptions(antialias=True,useWeave=True) # For more fps set antialias to false
PG_state="stand-by" # working/stand-by
Pop_number=80 # Default number of point to be shown
page_load="0"
stt=False
ch1Vdata=[]
ch1Adata=[]
ch2Vdata=[]
ch2Adata=[]
ch3Vdata=[]
ch3Adata=[]
ch4Vdata=[]
ch4Adata=[]
incom_message=[]      
timearray=[]
timer=0




class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        
        if page_load=="1": # Gui for 4 chanel
            uic.loadUi('vp_n6705b.ui', self)
            self.ui_init_1()
            self.ui_init_2()
            self.ui_init_3()
            self.ui_init_4()

        elif page_load=="2": #Gui for 1 chanel
            uic.loadUi('vp_n6705bp2.ui', self)
            self.ui_init_1()
        elif page_load=="3": #Gui for 2 chanel
            uic.loadUi('vp_n6705bp3.ui', self)    
            self.ui_init_1()
            self.ui_init_2()
            
        elif page_load=="4": #Gui for 3 chanel
            uic.loadUi('vp_n6705bp4.ui', self)
            self.ui_init_1()
            self.ui_init_2()
            self.ui_init_3()
            
        self.setWindowIcon(QtGui.QIcon('particle.png')) # the logo of the page can be changed prom there
        self.setWindowTitle("VP_n6705b") # the name of the page can be changed prom there
        self.show()
        #self.widget.addLine(x=None, y=0.8) #endless horizontal line
        self.pushButton_2.clicked.connect(self.connect_mainfn) # start button
        self.pushButton.clicked.connect(self.stop) # stop button
        self.spinBox.setValue(Pop_number) # spin box for changing the number data shown
        self.spinBox.valueChanged.connect(self.spinbox_check)
        
        self.spinBox_2.setValue(GraphUpdateFreq) # spin box for changing the update frequency
        self.spinBox_2.valueChanged.connect(self.spinbox_2_check)

        
        
    def ui_init_1(self):# plot configuration for the first plot
        global ch1,ch2,ch3,ch4
        self.ch1Vplot.showGrid(x=True, y=True,alpha=0.8) 
        self.ch1Aplot.showGrid(x=True, y=True,alpha=0.8)
        self.ch1Vplot.setLabel('left', 'Voltage (V)')
        self.ch1Vplot.setLabel('bottom', 'second (s)')
        self.ch1Aplot.setLabel('left', 'Current (A)')
        self.ch1Aplot.setLabel('bottom', 'second (s)')
        self.ch1Vplot_item=self.ch1Vplot.plot(pen = pg.mkPen(color=(0,128,128),width=2))
        self.ch1Aplot_item=self.ch1Aplot.plot(pen = pg.mkPen(color=(0,128,128),width=2))
        if ch1==True: # checking wich channel is set true and changing the plot label according to that
            self.label_3.setText("CH1") 
            ch1=False
        elif ch2==True:
            self.label_3.setText("CH2")
            ch2=False
        elif ch3==True:
            self.label_3.setText("CH3")
            ch3=False
        elif ch4==True:
            self.label_3.setText("CH4")
            ch4=False

    def ui_init_2(self):# plot configuration for the second plot
        global ch2,ch3,ch4
        self.ch2Vplot.showGrid(x=True, y=True,alpha=0.8)
        self.ch2Aplot.showGrid(x=True, y=True,alpha=0.8)
        self.ch2Vplot.setLabel('left', 'Voltage (V)')
        self.ch2Vplot.setLabel('bottom', 'second (s)')
        self.ch2Aplot.setLabel('left', 'Current (A)')
        self.ch2Aplot.setLabel('bottom', 'second (s)')
        self.ch2Vplot_item=self.ch2Vplot.plot(pen = pg.mkPen(color=(0,128,128),width=2))
        self.ch2Aplot_item=self.ch2Aplot.plot(pen = pg.mkPen(color=(0,128,128),width=2))
        if ch2==True:
            self.label_2.setText("CH2")
            ch2=False
        elif ch3==True:
            self.label_2.setText("CH3")
            ch3=False
        elif ch4==True:
            self.label_2.setText("CH4")
            ch4=False

    def ui_init_3(self):# plot configuration for the third plot
        global ch3,ch4
        self.ch3Vplot.showGrid(x=True, y=True,alpha=0.8)
        self.ch3Aplot.showGrid(x=True, y=True,alpha=0.8)
        self.ch3Vplot.setLabel('left', 'Voltage (V)')
        self.ch3Vplot.setLabel('bottom', 'second (s)')
        self.ch3Aplot.setLabel('left', 'Current (A)')
        self.ch3Aplot.setLabel('bottom', 'second (s)')
        self.ch3Vplot_item=self.ch3Vplot.plot(pen = pg.mkPen(color=(0,128,128),width=2))
        self.ch3Aplot_item=self.ch3Aplot.plot(pen = pg.mkPen(color=(0,128,128),width=2))
        if ch3==True:
            self.label.setText("CH3")
            ch3=False
        elif ch4==True:
            self.label.setText("CH4")
            ch4=False

    def ui_init_4(self):# plot configuration for the fourth plot
        self.ch4Vplot.showGrid(x=True, y=True,alpha=0.8)
        self.ch4Aplot.showGrid(x=True, y=True,alpha=0.8)
        self.ch4Vplot.setLabel('left', 'Voltage (V)')
        self.ch4Vplot.setLabel('bottom', 'second (s)')
        self.ch4Aplot.setLabel('left', 'Current (A)')
        self.ch4Aplot.setLabel('bottom', 'second (s)')
        self.ch4Vplot_item=self.ch4Vplot.plot(pen = pg.mkPen(color=(0,128,128),width=2))
        self.ch4Aplot_item=self.ch4Aplot.plot(pen = pg.mkPen(color=(0,128,128),width=2))
        
    def connect_mainfn(self): #This function is activated from the start button. İts checking which plotting/refresh function will be activated with the timer according the channel selection
        global PG_state
        if PG_state=="stand-by":
            PG_state="working"
            if page_load=="1":
                self.timer = QtCore.QTimer() # creating timer
                self.timer.setInterval(GraphUpdateFreq) # setting the timer frequency
                self.timer.timeout.connect(self.mainfn) # connecting the timer to a function
                self.timer.start() # starting the timer
            elif page_load=="2":
                self.timer = QtCore.QTimer()
                self.timer.setInterval(GraphUpdateFreq)
                self.timer.timeout.connect(self.mainfn1)
                self.timer.start()
            elif page_load=="3":
                self.timer = QtCore.QTimer()
                self.timer.setInterval(GraphUpdateFreq)
                self.timer.timeout.connect(self.mainfn2)
                self.timer.start()
            elif page_load=="4":
                self.timer = QtCore.QTimer()
                self.timer.setInterval(GraphUpdateFreq)
                self.timer.timeout.connect(self.mainfn3)
                self.timer.start()                
            
    def spinbox_check(self): # checking if the spinbox for changing the number of data show is changed or not
        global Pop_number
        Pop_number = self.spinBox.value()
        
    def spinbox_2_check(self): # checking if the spinbox for setting the update frequency is changed or not
        global GraphUpdateFreq
        GraphUpdateFreq = self.spinBox_2.value()
        self.timer.setInterval(GraphUpdateFreq) # upfating the update frequency accroding to the value taken from the spinbox
            
   
    def mainfn(self):
        global ch1Vdata,ch1Adata,ch2Vdata,ch2Adata,ch3Vdata,ch3Adata,ch4Vdata,ch4Adata,stt 
        start=tim() # starting a timer for calculate the time elapsed for refreshing the plot
        self.lineEdit.setText(str(round(time_elapsed[0]*1000,5))+" ms") # setting the the value of the line edit for represent the elapsed time of VP_function script for acquiring and creating a mesaage
        for x in range(len(ch_queue.queue)): # Reading the queue according to the number of message and decoding it
            incom_message=(ch_queue.get_nowait().split(";"))
            ch1Vdata.append(float(incom_message[1].split(",")[0]))
            ch1Adata.append(float(incom_message[1].split(",")[1]))
            ch2Vdata.append(float(incom_message[2].split(",")[0]))
            ch2Adata.append(float(incom_message[2].split(",")[1]))
            ch3Vdata.append(float(incom_message[3].split(",")[0]))
            ch3Adata.append(float(incom_message[3].split(",")[1]))
            ch4Vdata.append(float(incom_message[4].split(",")[0]))
            ch4Adata.append(float(incom_message[4].split(",")[1]))
            timearray.append(int(incom_message[0]))
            #-------------------------------------------------------- Data storage
            if stt==False:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                filehandle.writelines('%s' % "dd/mm/YY H:M:S"+";"+dt_string+"\n")
                filehandle.write('%s' % "Data number;Channel1:A;Channel1:V;Channel2:A;Channel2:V;Channel3:A;Channel3:V;Channel4:A;Channel4:V\n")
                stt=True   
            filehandle.write('%s' % str(timearray[-1])+";"+str(ch1Adata[-1])+";"+str(ch1Vdata[-1])+";"+str(ch2Adata[-1])+";"+str(ch2Vdata[-1])+";"+str(ch3Adata[-1])+";"+str(ch3Vdata[-1])+";"+str(ch4Adata[-1])+";"+str(ch4Vdata[-1])+"\n")
            filehandle.flush()
            #--------------------------------------------------------
                  
        self.ch1Vplot_item.setData(timearray,ch1Vdata) # updating the plot with new data
        self.ch2Vplot_item.setData(timearray,ch2Vdata)
        self.ch3Vplot_item.setData(timearray,ch3Vdata)
        self.ch4Vplot_item.setData(timearray,ch4Vdata)
        self.ch1Aplot_item.setData(timearray,ch1Adata)
        self.ch2Aplot_item.setData(timearray,ch2Adata)
        self.ch3Aplot_item.setData(timearray,ch3Adata)
        self.ch4Aplot_item.setData(timearray,ch4Adata)
        if len(ch1Vdata)>Pop_number: # if the length exceed the number maximal of the data to be shown then we delete the first item of all array
            ret=len(ch1Vdata)-Pop_number
            del ch1Vdata[0:ret]
            del ch1Adata[0:ret]
            del ch2Vdata[0:ret]
            del ch2Adata[0:ret]
            del ch3Vdata[0:ret]
            del ch3Adata[0:ret]
            del ch4Vdata[0:ret]
            del ch4Adata[0:ret]
            del timearray[0:ret]
        end=tim() # end the timer for the elapsed time calculation
        time_elapsedgui=end-start
        self.lineEdit_2.setText(str(round(time_elapsedgui*1000,5))+" ms")# setting the the value of the line edit for represent the elapsed time for refreshing the plot

    def mainfn1(self):
        global ch1Vdata,ch1Adata,filehandle,stt
        start=tim()
        self.lineEdit.setText(str(round(time_elapsed[0]*1000,5))+" ms")
        for x in range(len(ch_queue.queue)):
            incom_message=(ch_queue.get_nowait().split(";"))
            ch1Vdata.append(float(incom_message[1].split(",")[0]))
            ch1Adata.append(float(incom_message[1].split(",")[1]))
            timearray.append(int(incom_message[0]))
            #-------------------------------------------------------- Data storage
            if stt==False:
                chc=self.label_3.text()
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                filehandle.writelines('%s' % "dd/mm/YY H:M:S"+";"+dt_string+"\n")
                filehandle.write('%s' % "Data number;Channel"+chc[2]+":A;Channel"+chc[2]+":V\n")
                stt=True   
            filehandle.write('%s' % str(timearray[-1])+";"+str(ch1Adata[-1])+";"+str(ch1Vdata[-1])+"\n")
            filehandle.flush()
            #--------------------------------------------------------     
                     
        self.ch1Vplot_item.setData(timearray,ch1Vdata)
        self.ch1Aplot_item.setData(timearray,ch1Adata)
        if len(ch1Vdata)>Pop_number:
            ret=len(ch1Vdata)-Pop_number
            del ch1Vdata[0:ret]
            del ch1Adata[0:ret]
            del timearray[0:ret]
        end=tim()
        time_elapsedgui=end-start
        self.lineEdit_2.setText(str(round(time_elapsedgui*1000,5))+" ms")


    def mainfn2(self):
        global ch1Vdata,ch1Adata,ch2Vdata,ch2Adata,stt,filehandle
        #self.ch1Vplot.setYRange(1.99, 2.01, padding=0)
        start=tim()
        self.lineEdit.setText(str(round(time_elapsed[0]*1000,5))+" ms")
        for x in range(len(ch_queue.queue)):
            incom_message=(ch_queue.get_nowait().split(";"))
            ch1Vdata.append(float(incom_message[1].split(",")[0]))
            ch1Adata.append(float(incom_message[1].split(",")[1]))
            ch2Vdata.append(float(incom_message[2].split(",")[0]))
            ch2Adata.append(float(incom_message[2].split(",")[1]))
            timearray.append(int(incom_message[0]))        
            #-------------------------------------------------------- Data storage
            if stt==False:
                chc=self.label_3.text()
                chc1=self.label_2.text()
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                filehandle.writelines('%s' % "dd/mm/YY H:M:S"+";"+dt_string+"\n")
                filehandle.write('%s' % "Data number;Channel"+chc[2]+":A;Channel"+chc[2]+":V;Channel"+chc1[2]+":A;Channel"+chc1[2]+":V\n")
                stt=True   
            filehandle.write('%s' % str(timearray[-1])+";"+str(ch1Adata[-1])+";"+str(ch1Vdata[-1])+";"+str(ch2Adata[-1])+";"+str(ch2Vdata[-1])+"\n")
            filehandle.flush()
            #--------------------------------------------------------
        
        self.ch1Vplot_item.setData(timearray,ch1Vdata)
        self.ch1Aplot_item.setData(timearray,ch1Adata)
        self.ch2Vplot_item.setData(timearray,ch2Vdata)
        self.ch2Aplot_item.setData(timearray,ch2Adata)
        

        if len(ch1Vdata)>Pop_number:
            ret=len(ch1Vdata)-Pop_number
            del ch1Vdata[0:ret]
            del ch1Adata[0:ret]
            del ch2Vdata[0:ret]
            del ch2Adata[0:ret]
            del timearray[0:ret]
        end=tim()
        time_elapsedgui=end-start
        self.lineEdit_2.setText(str(round(time_elapsedgui*1000,5))+" ms")

    def mainfn3(self):
        global ch1Vdata,ch1Adata,ch2Vdata,ch2Adata,ch3Vdata,ch3Adata,ch4Vdata,ch4Adata,stt,filehandle,k_array,data_fn
        start=tim()
        self.lineEdit.setText(str(round(time_elapsed[0]*1000,5))+" ms")
        for x in range(len(ch_queue.queue)):
            incom_message=(ch_queue.get_nowait().split(";"))
            ch1Vdata.append(float(incom_message[1].split(",")[0]))
            ch1Adata.append(float(incom_message[1].split(",")[1]))
            ch2Vdata.append(float(incom_message[2].split(",")[0]))
            ch2Adata.append(float(incom_message[2].split(",")[1]))
            ch3Vdata.append(float(incom_message[3].split(",")[0]))
            ch3Adata.append(float(incom_message[3].split(",")[1]))
            timearray.append(int(incom_message[0]))
            #-------------------------------------------------------- Data storage
            if stt==False:
                chc=self.label_3.text()
                chc1=self.label_2.text()
                chc2=self.label.text()
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                filehandle.writelines('%s' % "dd/mm/YY H:M:S"+";"+dt_string+"\n")
                filehandle.write('%s' % "Data number;Channel"+chc[2]+":A;Channel"+chc[2]+":V;Channel"+chc1[2]+":A;Channel"+chc1[2]+":V;Channel"+chc2[2]+":A;Channel"+chc2[2]+":V\n")
                stt=True   
            filehandle.write('%s' % str(timearray[-1])+";"+str(ch1Adata[-1])+";"+str(ch1Vdata[-1])+";"+str(ch2Adata[-1])+";"+str(ch2Vdata[-1])+";"+str(ch3Adata[-1])+";"+str(ch3Vdata[-1])+"\n")
            filehandle.flush()
            #--------------------------------------------------------
             
        self.ch1Vplot_item.setData(timearray,ch1Vdata)
        self.ch2Vplot_item.setData(timearray,ch2Vdata)
        self.ch3Vplot_item.setData(timearray,ch3Vdata)
        self.ch1Aplot_item.setData(timearray,ch1Adata)
        self.ch2Aplot_item.setData(timearray,ch2Adata)
        self.ch3Aplot_item.setData(timearray,ch3Adata)
        if len(ch1Vdata)>Pop_number:
            ret=len(ch1Vdata)-Pop_number
            del ch1Vdata[0:ret]
            del ch1Adata[0:ret]
            del ch2Vdata[0:ret]
            del ch2Adata[0:ret]
            del ch3Vdata[0:ret]
            del ch3Adata[0:ret]
            del timearray[0:ret]
        end=tim()
        time_elapsedgui=end-start
        self.lineEdit_2.setText(str(round(time_elapsedgui*1000,5))+" ms")

        
    def stop(self):
        global PG_state
        self.timer.stop()
        PG_state="stand-by"
        
class Window2(QtWidgets.QMainWindow): # its the Configuration GUİ for setting the chanel and the save directory
    def __init__(self):
        super().__init__()
        uic.loadUi('vp_main.ui', self)
        self.setWindowTitle("CHANNEL SELECTİON") # the name of the page can be changed prom there
        self.setWindowIcon(QtGui.QIcon('particle.png'))# the logo of the page can be changed prom there
        self.show()
        
        self.pushButton.clicked.connect(self.graphpage) # continue button
        self.pushButton_2.clicked.connect(self.saveFileDialog) # the button for setting the file directory
        self.checkBox.stateChanged.connect(self.clickBox) # the checkbox of the channels
        self.checkBox_2.stateChanged.connect(self.clickBox_2)
        self.checkBox_3.stateChanged.connect(self.clickBox_3)
        self.checkBox_4.stateChanged.connect(self.clickBox_4)
        global canal1
        canal1=0
        
    def saveFileDialog(self): # the function for setting the file directory
        global save_path
        save_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if save_path:
            self.lineEdit_2.setText(save_path)  # showing the file directory in the line edit

    
    def clickBox(self,checked): # checking if the checkbox for the channels are clicked or not
        global canal1,ch1
        if QtCore.Qt.Checked == checked:
            canal1=canal1+1
            ch1=True
        else:
            canal1=canal1-1

    def clickBox_2(self,checked):
        global canal1,ch2
        if QtCore.Qt.Checked == checked:
            canal1=canal1+1
            ch2=True
        else:
            canal1=canal1-1

    def clickBox_3(self,checked):
        global canal1,ch3
        if QtCore.Qt.Checked == checked:
            canal1=canal1+1
            ch3=True
        else:
            canal1=canal1-1

    def clickBox_4(self,checked):
        global canal1,ch4
        if QtCore.Qt.Checked == checked:
            canal1=canal1+1
            ch4=True
        else:
            canal1=canal1-1


        
    def graphpage(self):
        global page_load,name_of_file,filehandle
        name_of_file =self.lineEdit.text()
        filepath =self.lineEdit_2.text()
        if canal1==4:
            page_load="1"
            ok=True
        elif canal1==1:
            page_load="2"
            ok=True
        elif canal1==2:
            page_load="3"
            ok=True
        elif canal1==3:
            page_load="4"
            ok=True
        if canal1==0 or bool(name_of_file=="")or bool(filepath=="") :
            ok=False
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('particle.png'))
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Channel, name or file directory selection is empty")
            msg.setWindowTitle("Error")
            msg.exec_()
        if ok==True:    
            self.w = Ui()
            self.w.show()
            self.hide()
            completeName = os.path.join(filepath, name_of_file+".csv")
            filehandle = open(completeName, 'a')   
              
def thread_function():
    global filehandle,page_load,ch1,ch2,ch3,ch4
    print(threading.current_thread())
    app = QtWidgets.QApplication(sys.argv)
    if ConfigurationGUİ== True:
        ch1=False
        ch2=False
        ch3=False
        ch4=False
        window = Window2()
    else:
        
        canal1=0
        if ch1==True:
            canal1=canal1+1
        if ch2==True:
            canal1=canal1+1
        if ch3==True:
            canal1=canal1+1
        if ch4==True:
            canal1=canal1+1
        if canal1==4:
            page_load="1"
        elif canal1==1:
            page_load="2"
        elif canal1==2:
            page_load="3"
        elif canal1==3:
            page_load="4"
        window = Ui()
        now = datetime.now()
        dt_string = str(now.strftime("%d-%m-%Y-%H-%M-%S "))
        filehandle = open(dt_string+".csv", 'w')
        
    app.exec_()

def startGUİ():
    x = threading.Thread(target=thread_function, args=(), daemon=True)
    x.name = "GUİ"
    print(threading.current_thread())
    
    x.start()