from VP_function import *
import time
from datetime import datetime

print("Test starting ...")
con_state=connect("192.168.214.9",5025)
reset()
configure((1,2,3,4),(2,2,2,2),(2,2,2,2))

now = datetime.now()
dt_string = str(now.strftime("%d-%m-%Y-%H-%M-%S "))
f = open(dt_string+".txt", "w")

fn_check=True
fn_number=0
percent=0

for fn in range(2):
    if fn_check==True:
        fn_number=fn_number+1
    else:
        f.write('%s' % "connect() :"+con_state+"\n\n")
        percent=percent+percentage
        print("%",round(percent,2))
        
    if fn_check==True:
        fn_number=fn_number+1
    else:
        idn=get_IDN()
        err=errorcheck()
        f.write('%s' % "get_IDN() :"+idn+"|Error responce from device :"+str(err)+"\n\n")
        percent=percent+percentage
        print("%",round(percent,2))
        
    if fn_check==True:
        fn_number=fn_number+1
    else:
        sftest=selfTest()
        err=errorcheck()
        if int(sftest)==0:
            f.write('%s' % "selfTest() : self test was successful = "+sftest+"|Error responce from device :"+str(err)+"\n\n")
        else:
            f.write('%s' % "selfTest() : error occur when self test = "+sftest+"|Error responce from device :"+str(err)+"\n\n")
        percent=percent+percentage
        print("%",round(percent,2))
    if fn_check== False:
        power_on()
    if fn_check==True:
        fn_number=fn_number+1
    else:
        chnumber=get_ch_number()
        err=errorcheck()
        f.write('%s' % "get_ch_number() :"+str(chnumber)+"|Error responce from device :"+str(err)+"\n\n")
        percent=percent+percentage
        print("%",round(percent,2))
        

    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            chmodel=get_ch_Model(x)
            err=errorcheck()
            f.write('%s' % "get_ch_model() : ch"+str(x)+"="+str(chmodel)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
        
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            chopt=get_ch_Option(x)
            err=errorcheck()
            f.write('%s' % "\n"+"get_ch_Option() : ch"+str(x)+":"+str(chopt)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))        
    """for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            chsr=get_ch_serial(x)
            err=errorcheck()
            f.write('%s' % "\n"+"get_ch_serial() : ch"+str(x)+":"+str(chsr)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))"""
    #*********************************************************************************************************           
    if fn_check==True:
        fn_number=fn_number+1
    else:    
        comst=com_state_check()
        err=errorcheck()
        f.write('%s' % "com_state_check() :"+str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        percent=percent+percentage
        print("%",round(percent,2))
        
     
    if fn_check==True:
        fn_number=fn_number+1
    else:
        set_com_state("REMote")
        err=errorcheck()
        percent=percent+percentage
        print("%",round(percent,2))
        f.write('%s' % "set_com_state() : setting the state to remote"+"|Error responce from device :"+str(err)+"\n\n")
    if fn_check==True:
        fn_number=fn_number+1
    else:
        comst=com_state_check().strip("\n") 
        err=errorcheck()
        percent=percent+percentage
        print("%",round(percent,2))
        if comst=="REM":
            f.write('%s' % "com_state_check() :"+str(comst)+" com state changing successful"+"\n")
        else:
            f.write('%s' % "com_state_check() : com state change not successful = " +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
    if fn_check==True:
        fn_number=fn_number+1
    else:
        set_com_state("LOCal")
        err=errorcheck()
        percent=percent+percentage
        print("%",round(percent,2))
    #***************************************************************************************************
    if fn_check==True:
        fn_number=fn_number+1
    else:
        tcpnum=get_Tcp_portnum()
        err=errorcheck()
        f.write('%s' % "get_Tcp_portnum() :"+str(tcpnum)+"|Error responce from device :"+str(err)+"\n\n")
        percent=percent+percentage
        print("%",round(percent,2))
        
    if fn_check==True:
        fn_number=fn_number+1
    else:
        sysver=get_sys_version()
        err=errorcheck()
        f.write('%s' % "get_sys_version() :"+str(sysver)+"|Error responce from device :"+str(err)+"\n\n")
        percent=percent+percentage
        print("%",round(percent,2))
        
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            rmscur=get_RMS_current(x)
            err=errorcheck()
            f.write('%s' % "\n"+"get_RMS_current() : ch"+str(x)+"="+str(rmscur)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
        
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            curh=get_current_high(x)
            err=errorcheck()
            f.write('%s' % "\n"+"get_current_high() : ch"+str(x)+":"+str(curh)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
        

    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            curl=get_current_low(x)
            err=errorcheck()
            f.write('%s' % "\n""get_current_low() : ch"+str(x)+":"+str(curl)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            

    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            curm=get_current_max(x)
            f.write('%s' % "\n"+"get_current_max() : ch"+str(x)+":"+str(curm)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            

    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            curmin=get_current_min(x)
            err=errorcheck()
            f.write('%s' % "\n"+"get_current_min() : ch"+str(x)+":"+str(curmin)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            

    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            rmsv=get_RMS_voltage(x)
            err=errorcheck()
            f.write('%s' % "\n"+"get_RMS_voltage() : ch"+str(x)+":"+str(rmsv)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            

    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            vh=get_voltage_high(x)
            err=errorcheck()
            f.write('%s' % "\n"+"get_voltage_high() : ch"+str(x)+":"+str(vh)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
        
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            vl=get_voltage_low(x)
            err=errorcheck()
            f.write('%s' % "\n"+"get_voltage_low() : ch"+str(x)+":"+str(vl)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            vm=get_current_max(x)
            err=errorcheck()
            f.write('%s' % "\n"+"get_voltage_max() : ch"+str(x)+":"+str(vm)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
             
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            vmin=get_voltage_min(x)
            err=errorcheck()
            f.write('%s' % "\n""get_voltage_min() : ch"+str(x)+":"+str(vmin)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            val=get_avg_pow(x)
            err=errorcheck()
            f.write('%s' % "\n"+"get_avg_pow() : ch"+str(x)+":"+str(val)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))    

    #*********************************************************************************************************       
    if fn_check==True:
        fn_number=fn_number+1
    else:    
        comst=calibration_state().strip("\n")
        err=errorcheck()
        f.write('%s' % "calibration_state() :"+str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        percent=percent+percentage
        print("%",round(percent,2))
        
    if fn_check==True:
        fn_number=fn_number+1
    else:
        calibration("ON")
        err=errorcheck()
        percent=percent+percentage
        print("%",round(percent,2))
        f.write('%s' % "calibration() : setting the state to ON"+"|Error responce from device :"+str(err)+"\n")
    if fn_check==True:
        fn_number=fn_number+1
    else:
        comst=calibration_state()
        err=errorcheck()
        percent=percent+percentage
        print("%",round(percent,2))
        if int(comst)==1:
            f.write('%s' % "calibration_state() :"+str(comst)+" calibration state changing successful"+"\n\n")
        else:
            f.write('%s' % "calibration_state() :" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
    if fn_check==True:
        fn_number=fn_number+1
    else:
        calibration("OFF")
        err=errorcheck()
        percent=percent+percentage
        print("%",round(percent,2))
    #***************************************************************************************************
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            val=get_voltage(x)
            err=errorcheck()
            f.write('%s' % "\n"+"get_voltage() : ch"+str(x)+":"+str(val)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))      

    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            val=get_current(x)
            err=errorcheck()
            f.write('%s' % "\n"+"get_current() : ch"+str(x)+":"+str(val)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))

    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            val=get_preset_voltage(x)
            err=errorcheck()
            if int(val)==2:
                f.write('%s' % "\n"+"get_preset_voltage() : ch"+str(x)+":"+str(val)+"|setting the voltage was successful"+"\n")
            else:
                f.write('%s' % "\n"+"get_preset_voltage() : ch"+str(x)+":"+str(val)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
     
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            val=get_preset_current(x)
            err=errorcheck()
            if int(val)==2:
                f.write('%s' % "\n"+"get_preset_current() : ch"+str(x)+":"+str(val)+"|setting the current was successful"+"\n")
            else:
                f.write('%s' % "\n"+"get_preset_current() : ch"+str(x)+":"+str(val)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))

    """for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            val=get_output_state(x)
            err=errorcheck()
            if int(val)==1:
                f.write('%s' % "\n"+"get_output_state() : ch"+str(x)+":"+str(val)+"|setting the output ON was successful"+"\n")
            else:
                f.write('%s' % "\n"+"get_output_state() : ch"+str(x)+":"+str(val)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2),fn_number)"""
    f.flush() 
    """for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            val=get_output_off_delay("MAX",x)
            err=errorcheck()
            f.write('%s' % "\n"+"get_output_off_delay() : ch"+str(x)+":"+str(val)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))

    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            val=set_output_off_delay(0.5,x)
            time.sleep(1)
            val1=get_output_state(x)
            err=errorcheck()
            if int(val1)==0:
                f.write('%s' % "\n"+"set_output_off_delay() : ch"+str(x)+":"+str(val)+"|setting the output OFF after 0.5 s was successful"+"\n")
            else:
                f.write('%s' % "\n"+"set_output_off_delay() : ch"+str(x)+":"+str(val)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))   
            
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            val=get_output_on_delay("MAX",x)
            err=errorcheck()
            f.write('%s' % "\n"+"get_output_on_delay() : ch"+str(x)+":"+str(val)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))

    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            val=set_output_on_delay(0.5,x)
            time.sleep(1)
            val1=get_output_state(x)
            err=errorcheck()
            if int(val1)==1:
                f.write('%s' % "\n"+"set_output_on_delay() : ch"+str(x)+":"+str(val)+"|setting the output ON after 0.5 s was successful"+"\n")
            else:
                f.write('%s' % "\n"+"set_output_on_delay() : ch"+str(x)+":"+str(val)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))"""       
    """for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            val=set_output_off(x)
            time.sleep(0.1)
            val1=get_output_state(x)
            err=errorcheck()
            if str(val1)==0:
                f.write('%s' % "\n"+"set_output_off() : ch"+str(x)+":"+str(val)+"|setting the output OFF was successful"+"\n")
            else:
                f.write('%s' % "\n"+"set_output_off() : ch"+str(x)+":"+str(val)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))    

    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            val=set_output_on(x)
            time.sleep(0.1)
            val1=get_output_state(x).strip("\n")
            err=errorcheck()
            if val1==1:
                f.write('%s' % "\n"+"set_output_on() : ch"+str(x)+"="+str(val)+"|setting the output ON was successful"+"\n")
            else:
                f.write('%s' % "\n"+"set_output_on() : ch"+str(x)+"="+str(val)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))"""  

#*********************************************************************************************************           
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_output_pmode(x)
            err=errorcheck()
            f.write('%s' % "get_output_pmode() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_output_pmode("CURR",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "calibration() : setting the mode to CURRent | value/error: ch "+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_output_pmode(x).strip("\n")
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if str(comst)=="CURR":
                f.write('%s' % "calibration_state() | value/error : ch"+str(x)+"="+str(comst)+" output mode was changed successfully"+"\n\n")
            else:
                f.write('%s' % "calibration_state() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_output_pmode("VOLT",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #***************************************************************************************************  
#*********************************************************************************************************           
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_trig_voltage(3,x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_trig_voltage() : setting the trigger voltage | value/error: ch "+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_set_trig_voltage(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if int(comst)==3:
                f.write('%s' % "get_set_trig_voltage() | value/error : ch"+str(x)+"="+str(comst)+" the trigger voltage was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_set_trig_voltage() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_trig_voltage("MIN",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #***************************************************************************************************
#*********************************************************************************************************           
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_voltage_bwid(x)
            err=errorcheck()
            f.write('%s' % "get_voltage_bwid() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_voltage_bwid("HIGH1",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_voltage_bwid() : setting the trigger voltage | value/error: ch "+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_voltage_bwid(x).strip("\n")
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if str(comst)=="HIGH1":
                f.write('%s' % "get_voltage_bwid() | value/error : ch"+str(x)+"="+str(comst)+" the voltage bandwidth was  set successfully"+"\n\n")
            else:
                f.write('%s' % "get_voltage_bwid() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_voltage_bwid("LOW",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #*************************************************************************************************** 
#*********************************************************************************************************           
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_voltagelimit_tracking_state(x)
            err=errorcheck()
            f.write('%s' % "get_voltagelimit_tracking_state() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_voltagelimit_tracking_state("ON",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_voltagelimit_tracking_state() : setting the voltage limit state | value/error: ch "+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_voltagelimit_tracking_state(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if comst==1:
                f.write('%s' % "get_voltagelimit_tracking_state() | value/error : ch"+str(x)+"="+str(comst)+" the voltage limit tracking state was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_voltagelimit_tracking_state() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_voltagelimit_tracking_state("OFF",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #*************************************************************************************************** 
    f.flush() 

#*********************************************************************************************************           
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_positive_voltage_limit(x)
            err=errorcheck()
            f.write('%s' % "get_positive_voltage_limit() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_positive_voltage_limit(2,x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_positive_voltage_limit() : setting the positive voltage limit | value/error: ch "+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_positive_voltage_limit(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if comst==2:
                f.write('%s' % "get_positive_voltage_limit() | value/error : ch"+str(x)+"="+str(comst)+" the positive voltage limit was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_positive_voltage_limit() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_positive_voltage_limit("MAX",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #*************************************************************************************************** 
#*********************************************************************************************************           
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_negative_voltage_limit(x)
            err=errorcheck()
            f.write('%s' % "get_negative_voltage_limit() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_negative_voltage_limit(-2,x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_negative_voltage_limit() : setting the negative voltage limit | value/error: ch "+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_negative_voltage_limit(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if comst==-2:
                f.write('%s' % "get_negative_voltage_limit() | value/error : ch"+str(x)+"="+str(comst)+" the negative voltage limit was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_negative_voltage_limit() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_negative_voltage_limit("MIN",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #***************************************************************************************************
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_voltage_mode(x)
            err=errorcheck()
            f.write('%s' % "get_voltage_mode() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_voltage_mode("STEP",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_voltage_mode() : setting the voltage mode to step | value/error: ch "+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_voltage_mode(x).strip("\n")
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if str(comst)=="STEP":
                f.write('%s' % "get_voltage_mode() | value/error : ch"+str(x)+"="+str(comst)+" the voltage mode was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_voltage_mode() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_voltage_mode("FIXed",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #***************************************************************************************************
    #***************************************************************************************************
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_voltage_protection_level(x)
            err=errorcheck()
            f.write('%s' % "get_voltage_protection_level() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_voltage_protection_level(10,x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_voltage_protection_level() : setting the voltage protection level | value/error: ch "+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_voltage_protection_level(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if comst==10:
                f.write('%s' % "get_voltage_protection_level() | value/error : ch"+str(x)+"="+str(comst)+" the voltage protection level was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_voltage_protection_level() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_voltage_protection_level("MAX",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #***************************************************************************************************
        #***************************************************************************************************
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_voltage_remote_protection_level_positive(x)
            err=errorcheck()
            f.write('%s' % "get_voltage_remote_protection_level_positive() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_voltage_remote_protection_level_positive(10,x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_voltage_remote_protection_level_positive() : setting the voltage remote protection positive level | value/error: ch "+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_voltage_remote_protection_level_positive(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if str(comst).strip("\n")=="10":
                f.write('%s' % "get_voltage_remote_protection_level_positive() | value/error : ch"+str(x)+"="+str(comst)+" the voltage remote protection positive level was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_voltage_remote_protection_level_positive() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_voltage_remote_protection_level_positive("MAX",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #***************************************************************************************************
    
        #***************************************************************************************************
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_voltage_remote_protection_level_negative(x)
            err=errorcheck()
            f.write('%s' % "get_voltage_remote_protection_level_negative() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_voltage_remote_protection_level_negative(-10,x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_voltage_remote_protection_level_negative() : setting the voltage remote protection negative level | value/error: ch "+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_voltage_remote_protection_level_negative(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if comst==-10:
                f.write('%s' % "get_voltage_remote_protection_level_negative() | value/error : ch"+str(x)+"="+str(comst)+" the voltage remote protection negative level was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_voltage_remote_protection_level_negative() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_voltage_remote_protection_level_negative("MIN",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #***************************************************************************************************

        #***************************************************************************************************
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_voltage_range(x)
            err=errorcheck()
            f.write('%s' % "get_voltage_range() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_voltage_range(10,x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_voltage_range() : setting the voltage range | value/error: ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_voltage_range(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if comst==10:
                f.write('%s' % "get_voltage_range() | value/error : ch"+str(x)+"="+str(comst)+" the voltage range was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_voltage_range() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_voltage_range("MAX",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #***************************************************************************************************    
        #***************************************************************************************************
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_voltage_sense_source(x)
            err=errorcheck()
            f.write('%s' % "get_voltage_sense_source() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_voltage_sense_source("EXT",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_voltage_sence_source() : setting the voltage sence source to external | value/error: ch "+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_voltage_sense_source(x).strip("\n")
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if str(comst)=="EXT":
                f.write('%s' % "get_voltage_sense_source() | value/error : ch"+str(x)+"="+str(comst)+" the voltage sence source was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_voltage_sense_source() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_voltage_sense_source("INT",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #***************************************************************************************************     
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_voltage_slewrate(x)
            err=errorcheck()
            f.write('%s' % "get_voltage_slewrate() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_voltage_slewrate(0,x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_voltage_sence_source() : setting the voltage slew rate | value/error: ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_voltage_slewrate(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if comst==0:
                f.write('%s' % "get_voltage_slewrate() | value/error : ch"+str(x)+"="+str(comst)+" the voltage slew rate was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_voltage_slewrate() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_voltage_slewrate(9.9E+37,x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #*************************************************************************************************** 

#*********************************************************************************************************           
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_set_trig_current(x)
            err=errorcheck()
            f.write('%s' % "get_set_trig_current() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_trig_current(2,x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_trig_current() : setting the trigger current | value/error: ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_set_trig_current(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if comst==2:
                f.write('%s' % "get_set_trig_current() | value/error : ch"+str(x)+"="+str(comst)+" the trigger current was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_set_trig_current() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_trig_current("MIN",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #*************************************************************************************************** 

#*********************************************************************************************************           
    """for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_current_limit_tracking_state(x)
            err=errorcheck()
            f.write('%s' % "get_current_limit_tracking_state() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_current_limit_tracking_state("ON",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_current_limit_tracking_state() : setting the current limit state | value/error: ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_current_limit_tracking_state(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if comst==1:
                f.write('%s' % "get_current_limit_tracking_state() | value/error : ch"+str(x)+"="+str(comst)+" the current limit tracking state was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_current_limit_tracking_state() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_current_limit_tracking_state("OFF",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #*************************************************************************************************** 

#*********************************************************************************************************           
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_positive_current_limit(x)
            err=errorcheck()
            f.write('%s' % "get_positive_current_limit() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_positive_current_limit(2,x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_positive_current_limit() : setting the positive current limit | value/error: ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_positive_current_limit(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if comst==2:
                f.write('%s' % "get_positive_current_limit() | value/error : ch"+str(x)+"="+str(comst)+" the positive current limit was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_positive_current_limit() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_positive_current_limit("MAX",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #*************************************************************************************************** 
#*********************************************************************************************************           
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_negative_current_limit(x)
            err=errorcheck()
            f.write('%s' % "get_negative_current_limit() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_negative_current_limit(-2,x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_negative_current_limit() : setting the negative current limit | value/error: ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_negative_current_limit(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if comst==-2:
                f.write('%s' % "get_negative_current_limit() | value/error : ch"+str(x)+"="+str(comst)+" the negative current limit was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_negative_current_limit() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_negative_current_limit("MIN",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #***************************************************************************************************
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_current_mode(x)
            err=errorcheck()
            f.write('%s' % "get_current_mode() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_current_mode("STEP",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_current_mode() : setting the current mode to step | value/error: ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_current_mode(x).strip("\n")
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if str(comst)=="STEP":
                f.write('%s' % "get_current_mode() | value/error : ch"+str(x)+"="+str(comst)+" the current mode was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_current_mode() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_current_mode("FIX",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #***************************************************************************************************   
        #***************************************************************************************************
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_current_range(x)
            err=errorcheck()
            f.write('%s' % "get_current_range() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_current_range(10,x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_current_range() : setting the current range | value/error: ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_current_range(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if comst==10:
                f.write('%s' % "get_current_range() | value/error : ch"+str(x)+"="+str(comst)+" the current range was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_current_range() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_current_range("MAX",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #***************************************************************************************************   

#***************************************************************************************************     
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_current_slewrate(x)
            err=errorcheck()
            f.write('%s' % "get_current_slewrate() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_current_slewrate(0,x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_current_sence_source() : setting the current slew rate | value/error: ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_current_slewrate(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if comst==0:
                f.write('%s' % "get_current_slewrate() | value/error : ch"+str(x)+"="+str(comst)+" the current slew rate was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_current_slewrate() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_current_slewrate(9.9E+37,x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #***************************************************************************************************

#***************************************************************************************************     
    for x in range(1,5):
        if fn_check==True:
            fn_number=fn_number+1
        else:    
            comst=get_current_protection_state(x)
            err=errorcheck()
            f.write('%s' % "get_current_protection_state() | value/error ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
            percent=percent+percentage
            print("%",round(percent,2))
            
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=set_current_protection_state("ON",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            f.write('%s' % "set_current_protection_state() : setting the current protection | value/error: ch"+str(x)+"="+str(comst)+"|Error responce from device :"+str(err)+"\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            comst=get_current_protection_state(x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
            if comst==1:
                f.write('%s' % "get_current_protection_state() | value/error : ch"+str(x)+"="+str(comst)+" the current protection was set successfully"+"\n\n")
            else:
                f.write('%s' % "get_current_protection_state() | value/error : ch"+str(x)+"=" +str(comst)+"|Error responce from device :"+str(err)+"\n\n")
        if fn_check==True:
            fn_number=fn_number+1
        else:
            set_current_protection_state("OFF",x)
            err=errorcheck()
            percent=percent+percentage
            print("%",round(percent,2))
    #***************************************************************************************************"""     
    
    

        
    fn_check=False
    percentage=100/fn_number 
f.flush()