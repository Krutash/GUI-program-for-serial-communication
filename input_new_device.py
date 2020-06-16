import threading 
import ctypes 
import time
import serial
import string
   
class thread_with_exception(threading.Thread): 
    def __init__(self, num, index): 
        threading.Thread.__init__(self) 
        self.num = num
        self.index = index
              
    def run(self):        
        Cof_file=open('Input_Coeff.txt').read()
        DataInList = Cof_file.split('\n')
        list_of_data = []
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
        line=''
        line3 = ''
        b=''
        k = 0.0
        nd=1   
        running = True
        timed = self.num*60
        while (running):
            COM4=serial.Serial('COM3',57600,timeout=1)
            try:
                ts1=time.time()
                while nd:
                    a=open("SampleText3.txt","a+")
                    if(self.index):
                        blog=open("Log.txt", 'a+')
                    COM4.write(b'A')
                    COM4.write(b'1000')
                    COM4.write(b'\r')
                    
                    line=COM4.readline()
                    line2=line.decode()
                    for s in line2.split():
                        if s.isdigit():
                            line3 = str(s)
                            
                    try:
                        line4 = line3.strip()
                        freq = int(line4)
                        k = (c1*freq*freq*freq + c2*freq*freq + c3*freq + c4)
                    except:
                        pass
                    dts=0.0
                    try:
                        if (line4):
                            ts2=time.time()
                            dts=ts2-ts1
                            if dts:
                                b=str("%.2f"%(float(dts/60)))+"  "+str("%.2f"%(float(k)))
                                data = str("%.3f"%(float(dts/60)))+"  "+str("%.3f"%(float(freq)))
                                a.write(b+"\n")
                                if(self.index):
                                    blog.write(data+"\n")
                                time.sleep(0.001)
                                   
                        if (dts>timed):
                            nd=0
                            break
                    except KeyboardInterrupt:
                        COM4.close()
                        break
                        
            except KeyboardInterrupt:
                running = False
                COM4.close()
                break
           
    def get_id(self): 
  
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id
   
    def raise_exception(self):
        
        thread_id = self.get_id() 
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
              ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure') 

