import logging
import threading
import os
import socket
import time
import random
import queue
from timeit import default_timer as timer

# TestMode1 must be set False for connect to the device and get real data
TestMode1=True #True/False 
sleeptime_GN_FN=0.02 # sleep time for general function like get voltage
sleeptime_SYS_FN=1 # sleep time for function like reset
connected = False
ch_queue=queue.Queue()
channels = list()
cfg_voltages = list()
cfg_currents = list()
headers = list()
k = 0
time_elapsed=[0]


def get_IDN(): # Return instrument identification
    try:
        err=eth_write("*IDN?")
        if err==None:
            time.sleep(sleeptime_GN_FN)
            IDN = eth_read()
            return IDN
        else:
            return err
    except:
        return "error while getting IDN"

def selfTest(): # Performs self-test, then returns result 0/1 The command returns 0 (all tests passed) or 1 (one or more tests failed)
    try:
        err=eth_write("*TST?")
        if err==None:
            time.sleep(sleeptime_SYS_FN)
            test=eth_read()
            return test
        else:
            return err
    except:
        return "error in self test"
    
def get_ch_number(): # returns the number of channels
        try:
            err=eth_write("SYST:CHAN?")
            if err==None:
                time.sleep(sleeptime_GN_FN)
                chn= eth_read() # ex +4
                try:
                    chn=int(chn)
                    return chn
                except:
                    return chn
            else:
                return err
        except: 
            return "error while getting channel number"

def get_ch_Model(channel): #  returns the model number of all output channels in a list. 
    try:
        err=eth_write_to_channel("SYST:CHAN:MOD? ",channel,False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            chmodel= eth_read()
            return chmodel
        else:
            return err
    except:
        return "error while getting channel model"

def get_ch_Option(channel): #  returns a list of options installed in each channel specified in the channel list.  
    try:
        err=eth_write_to_channel("SYST:CHAN:OPT? ",channel,False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            choption= eth_read()
            return choption
        else:
            return err
    except:
        return "error while getting channel option"

def get_ch_serial(channel): #  Returns the serial number of the specified output channels in a list.  
    try:
        err=eth_write_to_channel("CHAN:SER? ",channel,False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            chserial= eth_read()
            return chserial
        else:
            return err
    except:
        return "error while getting channel serial"

def set_com_state(choice): #  This command configures the remote/local state of the instrument choice can be LOCal | REMote | RWLock 
                      #  Default Value choice = LOCal (set at power-on)
    try:
        err=eth_write("SYST:COMM:RLST "+ str(choice))
        return err
    except:
        return err

def com_state_check(): #  This command returns the remote/local state of the instrument
    try:
        err=eth_write("SYST:COMM:RLST?")
        if err==None:
            time.sleep(sleeptime_GN_FN)
            chstatecheck=eth_read()
            return chstatecheck
        else:
            return err
    except:
        return "error while checking com state"

def get_Tcp_portnum(): #  This command returns the Control connection port number.
    try:
        err=eth_write("SYST:COMM:TCP:CONT?")
        if err==None:
            time.sleep(sleeptime_GN_FN)
            portnum= eth_read()
            return portnum
        else:
            return err
    except:
        return "error while getting port number"

def get_sys_version(): #  This command returns the version of the SCPI
    try:
        err=eth_write("SYST:VERS?")
        if err==None:
            time.sleep(sleeptime_GN_FN)
            version= eth_read()
            return version
        else:
            return err
    except:
        return "error while getting sys version"
    
def errorcheck(): # reads and clears all error / error list page 574
    global eth_socket
    try:
        error =[]
        eth_write("SYST:ERR?")
        time.sleep(sleeptime_GN_FN)
        responce=eth_read().split(",")
        #responce=-100,"o error"
        responce1=responce[1].strip("\n")       
        error.append(responce1)
        return error
                
    except:
        return "error checking problem"

def cal_current_limit_positive(current_limit,channel): # calibrates the positive current limit
    try:
        if calibration_state()=="0":
            calibration("ON")
        model =get_ch_Model(channel)
        if model[0:4]+model[-1]=="N678A": # N678xA SMU
            err=eth_write_to_channel("CAL:CURR:LIM:POS "+ str(current_limit), channel)
        else:
            return "This commaand only applies to models N678XA"
    except:
        return err  
    
def cal_current_limit_negative(current_limit,channel): # calibrates the negative current limit
    try: 
        if calibration_state()=="0":
            calibration("ON")
        model =get_ch_Model(channel)
        if model=="N6783A":
            err=eth_write_to_channel("CAL:CURR:LIM:POS "+ str(current_limit), channel)
        else:
            return "This command only applies to models N6783A"
    except:
        return err    
def cal_current_meas(current_max,channel): # calibrates the current measurement range. 
    try:
        if calibration_state()=="0":
            calibration("ON")
        err=eth_write_to_channel("CAL:CURR:MEAS "+ str(current_max), channel) 
    except:
        return err
    
def cal_voltage_limit_positive(voltage_limit,channel): # calibrates the positive voltage limit
    try:
        if calibration_state()=="0":
            calibration("ON")
        model =get_ch_Model(channel)
        if model[0:4]+model[-1]=="N678A": # N678xA SMU
            err=eth_write_to_channel("CAL:VOLT:LIM:POS "+ str(voltage_limit), channel)
        else:
            return "This commaand only applies to models N678XA"
    except:
        return err

def cal_voltage_meas(voltage_max,channel): # calibrates the current measurement range.
    try: 
        if calibration_state()=="0":
            calibration("ON")
        err=eth_write_to_channel("CAL:VOLT:MEAS "+ str(voltage_max), channel) 
    except:
        return err
    
def get_RMS_current(channel): # returns the total RMS current (AC + DC) in amperes
    try:
        err=eth_write_to_channel("MEAS:CURR:HIGH? ", channel, False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            highcurrent = eth_read()
            try:
                highcurrent=float(highcurrent)
                return highcurrent
            except:
                return highcurrent
        else:
            return err
    except:
        return "error while getting rms of current"

def get_current_high(channel): # This query initiates and triggers a measurement, and returns the High level of a current pulse waveform in amperes. 
    try:
        err= eth_write_to_channel("MEAS:CURR:HIGH? ", channel, False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            highcurrent = eth_read()
            try:
                highcurrent=float(highcurrent)
                return highcurrent
            except:
                return highcurrent
        else:
            return err
    except:
        return "error while getting hight level of current"
    
def get_current_low(channel): # This query initiates and triggers a measurement, and returns the Low level of a current pulse waveform in amperes. 
    try:
        err=eth_write_to_channel("MEAS:CURR:LOW? ", channel, False)
        if err== None:
            time.sleep(sleeptime_GN_FN)
            lowcurrent = eth_read()
            try:
                lowcurrent = float(lowcurrent)
                return lowcurrent
            except:
                return lowcurrent
        else:
            return err
    except:
        return "error while getting low level of current"

def get_current_max(channel): # This query initiates and triggers a measurement, and returns the max of a current pulse waveform in amperes. 
    try:
        err=eth_write_to_channel("MEAS:CURR:MAX? ", channel, False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            maxcurrent =eth_read()
            try:
                maxcurrent = float(maxcurrent)
                return maxcurrent
            except:
                return maxcurrent
        else:
            return err
    except:
        return "error while getting max level of current"
    
def get_current_min(channel): # This query initiates and triggers a measurement, and returns the max of a current pulse waveform in amperes. 
    try:
        err=eth_write_to_channel("MEAS:CURR:MIN? ", channel, False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            mincurrent = eth_read()
            try:
                mincurrent = float(mincurrent)
                return mincurrent
            except:
                return mincurrent
        else:
            return err
    except:
        return "error while getting min level of current"
    
def get_RMS_voltage(channel): # d returns the total RMS voltage (AC + DC) in volts.
    try:
        err=eth_write_to_channel("MEAS:VOLT:ACDC? ", channel, False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            rmsvoltage = eth_read()
            try:
                rmsvoltage = float(rmsvoltage)
                return rmsvoltage
            except:
                return rmsvoltage
        else:
            return err
    except:
        return "error while getting RMS of voltage"
    
def get_voltage_high(channel): # This query initiates and triggers a measurement, and returns the High level of a voltage pulse waveform in amperes. 
    try:
        err=eth_write_to_channel("MEAS:VOLT:HIGH? ", channel, False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            highvoltage =eth_read()
            try:
                highvoltage = float(highvoltage)
                return highvoltage
            except:
                return highvoltage
        else:
            return err
    except:
        return "error while getting high level of voltage"
    
def get_voltage_low(channel): # This query initiates and triggers a measurement, and returns the Low level of a voltage pulse waveform in amperes. 
    try:
        err=eth_write_to_channel("MEAS:VOLT:LOW? ", channel, False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            lowvoltage =eth_read()
            try:
                lowvoltage = float(lowvoltage)
                return lowvoltage
            except:
                return lowvoltage
        else:
            return err
    except:
        return "error while getting low level of voltage"

def get_voltage_max(channel): # This query initiates and triggers a measurement, and returns the max of a voltage pulse waveform in amperes. 
    try:
        err=eth_write_to_channel("MEAS:VOLT:MAX? ", channel, False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            maxvoltage = eth_read()
            try:
                maxvoltage = float(maxvoltage)
                return maxvoltage
            except:
                return maxvoltage
        else:
            return err
    except:
        return "error while getting max level of voltage"
    
def get_voltage_min(channel): # This query initiates and triggers a measurement, and returns the max of a voltage pulse waveform in amperes. 
    try:
        err=eth_write_to_channel("MEAS:VOLT:MIN? ", channel, False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            minvoltage =eth_read()
            try:
                minvoltage = float(minvoltage)
                return minvoltage
            except:
                return minvoltage
        else:
            return err   
    except:
        return "error while getting min level of voltage"


def get_avg_pow(channel): # 
    try:
        err=eth_write_to_channel("MEAS:POW? ", channel, False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            avg_pov = eth_read()
            try:
                avg_pov = float(avg_pov)
                return avg_pov
            except:
                return avg_pov
        else:
            return err
    except:
        return "error while getting average power"
    
def reset():
    try:
        err=eth_write("*RST")
        time.sleep(sleeptime_SYS_FN)
        return err
    except:
        return err

def reboot():  # reboots the instrument. 
    try:
        err=eth_write("SYST:REB")
        time.sleep(sleeptime_SYS_FN)
        return err
    except:
        return err
    
def calibration(state): # enables or disable calibration mode, state = ON/OFF
    try:
        err=eth_write("CAL:STAT "+ state)
        return err
    except:
        return err

        
def calibration_state(): # returns the calibration state
    try:
        err=eth_write("CAL:STAT?")
        if err==None:
            time.sleep(sleeptime_GN_FN)
            state= eth_read()
            return state
        else:
            return err
    except:
        return "error while getting the calibration state"
    
def get_voltage(channel):
    try:
        err=eth_write_to_channel("MEAS:VOLT? ", channel, False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            voltage = eth_read()
            try:
                voltage = float(voltage)
                return voltage
            except:
                return voltage
        else:
            if TestMode1==True:
                return random.uniform(0,24)
            else:
                return err
    except:
        return "error while getting voltage"
    
def get_current(channel):
    try:
        err=eth_write_to_channel("MEAS:CURR? ", channel, False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            current = eth_read()
            try:
                current = float(current) 
                return current   
            except:
                return current
        else:
            if TestMode1==True:
                return random.uniform(0,10)
            else:
                return err                
    except:
        return "error while getting current"

def eth_read():
    global eth_socket
    response = ""
    try:
        while True:
            buf = eth_socket.recv(1024)
            rcv = buf.decode("utf-8")
            response = response + rcv
            if response.endswith("\n"):
                break
    except:
        return "reading error"

    return response

def eth_write(command):
    global eth_socket
    try:
        str_command = (command + '\n').encode('utf-8')
        eth_socket.sendall(str_command)
    except:
        return "command sending error"   
    
def eth_write_to_channel(command,channel,comma = True):
    try:
        if comma:
            str_command = command + ", (@{0})".format(channel)
        else:
            str_command = command + " (@{0})".format(channel)
        commandto = (str_command + '\n').encode('utf-8')
        eth_socket.sendall(commandto)
    except:
        return "command sending error" 
    
def configure(_channels, voltages, currents):
    global channels
    global cfg_voltages
    global cfg_currents
    if len(_channels) == len(voltages) and len(_channels) == len(currents):
        channels = _channels
        cfg_voltages = voltages
        cfg_currents = currents
    else:
        print('Error: number of channels and voltages/currents should be the same')    
        
def power_on():
    if connected:
        for k, channel in list(enumerate(channels)):
            set_voltage(cfg_voltages[k], channel)
            time.sleep(0.5)
            set_current(cfg_currents[k], channel)
            time.sleep(0.5)

        for k, channel in list(enumerate(channels)):
            set_output_on(channel)
            time.sleep(0.5)     
            
def power_off():
    if connected:
        for k, channel in list(enumerate(channels)):
            set_output_off(channel)
            
def set_voltage(voltage,channel):
    try:
        err=eth_write_to_channel("VOLT " + str(voltage), channel)
        return err
    except:
        return err
    
def get_preset_voltage(channel):
    try:
        err=eth_write_to_channel("VOLT? ", channel,False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            setvoltage =eth_read()
            try:
                setvoltage = float(setvoltage)
                return setvoltage
            except:
                return setvoltage
        else:
            return err
    except:
        return "error while getting preset voltage"

def set_current(current,channel):
    try:
        err=eth_write_to_channel("CURR " + str(current), channel)
        return err
    except:
        return err
    
def get_preset_current(channel):
    try:
        err=eth_write_to_channel("CURR? ", channel,False)      
        if err==None:
            time.sleep(sleeptime_GN_FN)
            setcurrent =eth_read()
            try:
                setcurrent = float(setcurrent)
                return setcurrent
            except:
                return setcurrent
        else:
            return err
    except:
        return "error while gettinf preset current"

def set_output_on(channel):
    try: 
        err=eth_write_to_channel("OUTP ON ", channel)
        return err
    except:
        return err

def get_output_state(channel): # get ouput state of the specific channel 0 or 1
    try:
        err=eth_write_to_channel("OUTP? ", channel)
        time.sleep(sleeptime_GN_FN)
        if err== None:
            state = eth_read()
            return state
        else:
            return err
    except:
        return "error while getting ouput state"
    
def set_output_off_delay(delay,channel): # This command sets the delay in seconds that the instrument waits before disabling the specified output
    try:
        err=eth_write_to_channel("OUTP:DEL:FALL "+str(delay), channel)
        return err
    except:
        return err
        

def get_output_off_delay(range,channel): # returns the allowable delay time of channel
    try:
        err=eth_write_to_channel("OUTP:DEL:FALL? "+str(range), channel)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            delay =eth_read()
            try:
                delay = float(delay)
                return delay
            except:
                return delay
        else:
            return err    
    except:
        return "error while getting ouput off delay"
    
def set_output_on_delay(delay,channel): # This command sets the delay in seconds that the instrument waits before enabling the specified output
    try:
        err=eth_write_to_channel("OUTP:DEL:RISE "+str(delay), channel)
        return err
    except:
        return err

def get_output_on_delay(range,channel): # This command returns the maximum allowable delay time of the channel for on
    try:
        err=eth_write_to_channel("OUTP:DEL:RISE? "+str(range),channel)
        if err==None:  
            time.sleep(sleeptime_GN_FN) 
            delay =eth_read()
            try:
                delay = float(delay)
                return delay
            except:
                return delay
        else:
            return err
    except:
        return "error while getting ouput on delay"

def set_output_off(channel):
    try:
        err=eth_write_to_channel("OUTP OFF ", channel)
        return err
    except:
        return err
    
def set_output_pmode(mode,channel): # This command sets the preferred mode for output on or output off transitions
    try:
        model =get_ch_Model(channel)
        if model=="N6762A" or model=="N6761A" : # mode = VOLTage | CURRent
            err=eth_write_to_channel("OUTP:PMOD "+ str(mode), channel)
        else:
            return "This command only applies to models N6762A and N6761A"
    except:
        return err
    
def get_output_pmode(channel): # This command get the preferred mode for output on or output off transitions
    try:
        model =get_ch_Model(channel)
        if model=="N6762A" or model=="N6761A" : # mode = VOLTage | CURRent
            err=eth_write_to_channel("OUTP:PMOD? ", channel)
            if err== None:
                time.sleep(sleeptime_GN_FN)
                mode = eth_read()
                return mode
            else:
                return err
        else:
            return "This command only applies to models N6762A and N6761A"
    except:
        return "error while getting output mode"
    
def set_trig_voltage(trgvoltage,channel): # This command sets the triggered voltage level of the specified output channel
    try:
        err=eth_write_to_channel("VOLT:TRIG "+ str(trgvoltage), channel)
        return err
    except:
        return err
    
def get_set_trig_voltage(channel): # returns the programmed triggered level on channels
    try:
        err=eth_write_to_channel("VOLT:TRIG? ", channel,False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            setvoltage = eth_read()
            try:
                setvoltage = float(setvoltage)
                return setvoltage
            except:
                return setvoltage
        else:
            return err
    except:
        return "error while getting preset trigger voltage"
    
def set_voltage_bwid(range,channel): # range :LOW | HIGH1 | HIGH2 | HIGH3 This command specifies a voltage bandwidth
    try:
        model =get_ch_Model(channel)
        if model[0:4]+model[-2]=="N678A": # N678xA SMU
            err=eth_write_to_channel("VOLT:BWID "+ str(range), channel)
        else:
            return "This command only applies to models N678XA"
    except:
        return err

def get_voltage_bwid(channel): # returns the bandwidth selection of channel
    try:
        model =get_ch_Model(channel)
        if model[0:4]+model[-2]=="N678A": # N678xA SMU
            err=eth_write_to_channel("VOLT:BWID? "+ str(range), channel,False)
            if err== None:
                time.sleep(sleeptime_GN_FN)
                bwidvoltage = eth_read()
                return bwidvoltage
            else:
                return err
        else:
            return "This command only applies to models N678XA"
    except:
        return "error while getting the voltage bandwidth"
    
def set_voltagelimit_tracking_state(state,channel): # state :OFF | 0 | ON | 1 This command sets the voltage limit tracking state
        try:
            model =get_ch_Model(channel)
            if model=="N6784A": 
                err=eth_write_to_channel("VOLT:LIM:COUP "+ str(state), channel)
            else:
                return "This command only applies to models N6762A and N6761A"
        except:
            return err
        
def get_voltagelimit_tracking_state(channel):
    try:
        model =get_ch_Model(channel)
        if model=="N6784A" :
            err=eth_write_to_channel("VOLT:LIM:COUP? ", channel,False)
            if err == None:
                time.sleep(sleeptime_GN_FN)
                limitvoltage = eth_read()#limitvoltage: 0/1
                return limitvoltage
            else:
                return err
        else:
            return "This command only applies to models N6784A"   
    except:
        return "error while getting the voltage limit tracking state" 
    
def set_positive_voltage_limit(limit,channel): # limit :0 - 20.4 | MIN | MAX This command sets the positive voltage limit of the specified output channel. 
    try:
        model =get_ch_Model(channel)
        if model[0:4]+model[-1]=="N678A": # N678xA SMU
            err=eth_write_to_channel("VOLT:LIM "+ str(limit), channel)
        else:
            return "This command only applies to models N678XA"
    except:
        return err

def get_positive_voltage_limit(channel): # returns the voltage limit on channels
    try:
        model =get_ch_Model(channel)
        if model[0:4]+model[-1]=="N678A": # N678xA SMU
            err=eth_write_to_channel("VOLT:LIM? "+ str(range), channel,False)
            if err==None: 
                time.sleep(sleeptime_GN_FN)
                limit = eth_read()
                try:
                    limit = float(limit)
                    return limit
                except:
                    return limit
            else:
                return err
        else:
            return "This command only applies to models N678XA"
    except:
        return "error while getting the positive voltage limit"

def set_negative_voltage_limit(limit,channel): # limit:-20.4 to 0 | MIN | MAX This command sets the negative voltage limit of the specified output channel. 
    try:
        model =get_ch_Model(channel)
        if model=="N6784A": 
            err=eth_write_to_channel("VOLT:LIM:NEG "+ str(limit), channel)
        else:
            return "This command only applies to models N6784A"
    except:
        err

def get_negative_voltage_limit(channel): # returns the voltage limit on channels
    try:
        model =get_ch_Model(channel)
        if model=="N6784A": 
            err=eth_write_to_channel("VOLT:LIM:NEG? "+ channel,False)
            if err ==None:
                time.sleep(sleeptime_GN_FN)
                limit =eth_read()
                try:
                    limit = float(limit)
                    return limit
                except:
                    return limit
            else:
                return err
        else:
            return "This command only applies to models N6784A"
    except:
        return "error while getting the negative voltage limit"
    
def set_voltage_mode(mode,channel): # mode: FIXed | STEP | LIST | ARB(default:fixed) This command determines what happens to the output voltage when the transient system is initiated and triggered.
    try:
        err=eth_write_to_channel("VOLT:MODE "+ str(mode), channel)
        return err
    except:
        return err
    
def get_voltage_mode(channel): # returns the voltage mode of channel
    try:
        err=eth_write_to_channel("VOLT:MODE? "+ channel,False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            mode = eth_read()
            return mode
        else:
            return err
    except:
        return "error while getting voltage mode"

def set_voltage_protection_level(level,channel): #This command sets the over-voltage protection (OVP) level of the output channel
    # level:0 - maximum | MIN | MAX(default:max) The maximum value dependent on the voltage rating of the power module
    try:
        model =get_ch_Model(channel)
        if model[0:4]+model[-1]!="N678A": # N678xA SMU
            err=eth_write_to_channel("VOLT:PROT "+ str(level), channel)
        else:
            return "This command does NOT apply to models N678xA"
    except:
        return err
    
def get_voltage_protection_level(channel): # returns the programmed voltage protection level on channel
    try:
        model =get_ch_Model(channel)
        if model[0:4]+model[-1]!="N678A": # N678xA SMU
            try:
                err=eth_write_to_channel("VOLT:PROT? "+ channel,False)
                if err == None:
                    time.sleep(sleeptime_GN_FN)
                    level = eth_read()
                    try:
                        level=float(level)
                        return level
                    except:
                        return level
            except:
                return err
        else:
            return "This command does NOT apply to models N678xA"
    except:
        return "error while getting voltage protection level"

def set_voltage_remote_protection_level_positive(level,channel): #This command sets the positive over-voltage protection (OVP) level of the output channel
    # level:0 - 22 | MIN | MAX(default:max)
    try:
        model =get_ch_Model(channel)
        if model[0:4]+model[-1]=="N678A": # N678xA SMU
            err=eth_write_to_channel("VOLT:PROT:REM "+ str(level), channel)
        else:
            return "This command only applies to models N678XA"
    except:
        return err
    
def get_voltage_remote_protection_level_positive(channel): # returns the programmed voltage protection level on channel
    try:
        model =get_ch_Model(channel)
        if model[0:4]+model[-1]=="N678A": # N678xA SMU
            err=eth_write_to_channel("VOLT:PROT:REM? "+ channel,False)
            if err== None:
                time.sleep(sleeptime_GN_FN)
                level=eth_read()
                try: 
                    level = float(level)
                    return level
                except:
                    return level
            else:
                return err
        else:
            return "This command only applies to models N678XA"
    except:
        return "error while getting positive protection level"
    
def set_voltage_remote_protection_level_negative(level,channel): #This command sets the negative over-voltage protection (OVP) level of the output channel
    # level:-22 to 0 | MIN | MAX (default:min)
    try:
        model =get_ch_Model(channel)
        if model=="N6784A": # N678xA SMU
            err=eth_write_to_channel("VOLT:PROT:REM:NEG "+ str(level), channel)
        else:
            return "This command only applies to models N6784A"
    except:
        return err
    
def get_voltage_remote_protection_level_negative(channel): # returns the programmed voltage protection level on channel
    try:
        model =get_ch_Model(channel)
        if model=="N6784A": # N678xA SMU
            err=eth_write_to_channel("VOLT:PROT:REM:NEG? ",channel,False)
            if err== None:
                time.sleep(sleeptime_GN_FN)
                level =eth_read()
                try:
                    level=float(level)
                    return level
                except:
                    return level
            else:
                return err
        else:
            return "This command only applies to models N6784A"
    except:
        return "error while getting negative protection level"
    
def set_voltage_range(range,channel): # This command sets the output voltage range on models that have multiple ranges
    #Range:0 - maximum | MIN | MAX (default:MAX) Values entered are model dependent.
    try:
        err=eth_write_to_channel("VOLT:RANG "+ str(range), channel)
        return err
    except:
        return err

def get_voltage_range(channel): # returns the programmed voltage range on channels
    try:
        err=eth_write_to_channel("VOLT:RANG? ", channel,False)
        if err== None:
            time.sleep(sleeptime_GN_FN)
            range =eth_read()
            try:
                range=float(range)
                return range
            except:
                return range
        else:
            return err
    except:
        return "error while getting voltage range"    

def set_voltage_sense_source(mode,channel): # This command sets the state of the remote sense relays
    #Mode :INTernal | EXTernal (default:internal) Values entered are model dependent.
    try:
        err=eth_write_to_channel("VOLT:SENS:SOUR "+ str(mode), channel)
        return err
    except:
        return err

def get_voltage_sense_source(channel): #  returns the remote sense relay state
    try:
        err=eth_write_to_channel("VOLT:SENS:SOUR? ", channel,False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            mode = eth_read()
            return mode
        else:
            return err
    except:
        return "error while getting voltage sensce source"
    
def set_voltage_slewrate(value,channel): # This command sets the voltage slew rate in volts per second
    #value :0 - 9.9E+37 | MIN | MAX | INFinity (default:9.9E+37) Values entered are model dependent.
    try:
        err=eth_write_to_channel("VOLT:SLEW "+ str(value), channel)
        return err
    except:
        return err
    
def get_voltage_slewrate(channel): #  returns the remote sense relay state
    try:
        err=eth_write_to_channel("VOLT:SLEW? ", channel,False)
        if err== None:                
            time.sleep(sleeptime_GN_FN)
            value = eth_read()
            try:
                value=float(value)
                return value
            except:
                return value
        else:
            return err
    except:
        return "error while getting voltage slew rate"

def set_voltage_slewrate_max(value,channel): # This command sets the voltage slew rate maximum override
    #value :OFF | 0 | ON | 1(default:OFF) Values entered are model dependent.
    try:
        err=eth_write_to_channel("VOLT:SLEW:MAX "+ str(value), channel)
        return err
    except:
        return err
    
def get_voltage_slewrate_max(channel): #  returns the remote sense relay state 
    try:
        err=eth_write_to_channel("VOLT:SLEW:MAX? ", channel,False)
        if err== None:                
            time.sleep(sleeptime_GN_FN)
            value = eth_read()
            try:
                value=float(value)
                return value
            except:
                return value
        else:
            return err
    except:
        return "error while getting max voltage slew rate"

def set_trig_current(trgcurrent,channel): # This command sets the triggered current level of the specified output channel
    try:
        err=eth_write_to_channel("CURR:TRIG "+ str(trgcurrent), channel)
        return err
    except:
        return err
    
def get_set_trig_current(channel): # returns the programmed triggered level on channels
    try:
        err=eth_write_to_channel("CURR:TRIG? ", channel,False)
        if err == None:
            time.sleep(sleeptime_GN_FN)
            setcurrent = eth_read()
            try:
                setcurrent = float(setcurrent)
                return setcurrent
            except:
                return setcurrent
        else:
            return err
    except:
        return "error while getting preset trigger current"

def set_positive_current_limit(limit,channel): # limit :0 - 20.4 | MIN | MAX This command sets the positive voltage limit of the specified output channel. 
    try:
        model =get_ch_Model(channel)
        if model[0:4]+model[-1]=="N678A"or model=="N6783A": # N678xA SMU
            err=eth_write_to_channel("CURR:LIM "+ str(limit), channel)
        else:
            return "This command only applies to models N678XA and N6783A"
    except:
        return err

def get_positive_current_limit(channel): # returns the voltage limit on channels
    try:
        model =get_ch_Model(channel)
        if model[0:4]+model[-1]=="N678A" or model=="N6783A": # N678xA SMU
            err=eth_write_to_channel("CURR:LIM? "+ str(range), channel,False)
            if err==None:
                time.sleep(sleeptime_GN_FN)
                limit = eth_read()
                try:
                    limit = float(limit)
                    return limit
                except:
                    return limit
        else:
            return "This command only applies to models N678XA and N6783A"
    except:
        return "error while getting positive curren limit"    
    
def set_current_limit_tracking_state(state,channel): # state :OFF | 0 | ON | 1 This command sets the current limit tracking state
    try:
        model =get_ch_Model(channel)
        if  model[0:4]+model[-1]=="N678A": 
            err=eth_write_to_channel("CURR:LIM:COUP "+ str(state), channel)
        else:
            return "This command only applies to models N678XA"
    except:
        return err
        
def get_current_limit_tracking_state(channel):
    try:
        model =get_ch_Model(channel)
        if model[0:4]+model[-1]=="N678A" :
            err=eth_write_to_channel("CURR:LIM:COUP? ", channel,False)
            if err== None:
                time.sleep(sleeptime_GN_FN)
                limitvoltage = eth_read() #limitvoltage: 0/1
                return limitvoltage
            else:
                return err    
        else:
            return "This command only applies to models N678XA"  
    except:
        return "error while gettng current limit track state "

def set_negative_current_limit(limit,channel): # This command sets the negative current limit of the specified output channel. 
    #-3.06 to 0 | MIN | MAX (N678xASMU) -2 to 0 | MIN | MAX (N6783A-BAT) (default:MIN)
    try:
        model =get_ch_Model(channel)
        if model[0:4]+model[-1]=="N678A" or model=="N6783A": 
            err=eth_write_to_channel("CURR:LIM:NEG "+ str(limit), channel)
        else:
            return "This command only applies to models N6784A"
    except:
        return err

def get_negative_current_limit(channel): # returns the voltage limit on channels
    try:
        model =get_ch_Model(channel)
        if model[0:4]+model[-1]=="N678A" or model=="N6783A": 
            err=eth_write_to_channel("CURR:LIM:NEG? "+ channel,False)
            if err==None:
                time.sleep(sleeptime_GN_FN)
                limit = eth_read()
                try:
                    limit = float(limit)
                    return limit
                except:
                    return limit
            else: 
                return err
        else:
            return "This command only applies to models N6784A"
    except:
        return "error while getting negatşve current limit"

def set_current_mode(mode,channel): # mode: FIXed | STEP | LIST | ARB(default:fixed) This command determines what happens to the output CURR when the transient system is initiated and triggered.
    try:
        err=eth_write_to_channel("CURR:MODE "+ str(mode), channel)
        return err
    except:
        return err
    
def get_current_mode(channel): # returns the voltage mode of channel
    try:
        err=eth_write_to_channel("CURR:MODE? "+ channel,False)
        if err== None:
            time.sleep(sleeptime_GN_FN)
            mode = eth_read()
            return mode
        else:
            return err
    except:
        return "error while getting current mode"

def set_current_protection_delay(delay,channel): # This command sets the over-current protection delay : 0 - 0.255 | MIN | MAX default 20ms
    try:
        err=eth_write_to_channel("CURR:PROT:DEL "+ str(delay), channel)
        return err
    except:
        return err

def get_current_protection_delay(channel): # returns the  current protection delay of channel
    try:
        err=eth_write_to_channel("CURR:PROT:DEL? "+ channel,False)
        if err== None:
            time.sleep(sleeptime_GN_FN)
            mode = float(eth_read())
            try:
                mode = float(mode)
                return mode
            except:
                return mode
        else:
            return err
    except:
        return "error while getting the current protection delay "
    
def set_current_protection_delay_start(mode,channel): # This command specifies the conditions under which the over-current protection delay timer starts 
    # mode: SCHange | CCTRans (default:SCHange)
    try:
        err=eth_write_to_channel("CURR:PROT:DEL:STAR "+ str(mode), channel)
        return err
    except:
        return err

def get_current_protection_delay_start(channel): # returns the current protection delay mode
    try:
        err=eth_write_to_channel("CURR:PROT:DEL:STAR? "+ channel,False)
        if err== None:
            time.sleep(sleeptime_GN_FN)
            mode = eth_read()
            return mode
        else:
            return err
    except:
        return "error while getting current protection delay mode"

def set_current_protection_state(mode,channel): # This command enables or disables the over-current protection (OCP) function
    # mode: OFF | 0 | ON | 1 (default:OFF)
    try:
        err=eth_write_to_channel("CURR:PROT:STAT "+ str(mode), channel)
        return err
    except:
        return err

def get_current_protection_state(channel): # returns the current protection delay state
    try:
        err=eth_write_to_channel("CURR:PROT:STAT?  "+ channel,False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            mode = eth_read()
            return mode
        else:
            return err
    except:
        return "error while getting current protection state"

def set_current_range(range,channel): # This command sets the output voltage range on models that have multiple ranges
    #Range:0 - maximum | MIN | MAX (default:MAX) Values entered are model dependent.
    try:
        err=eth_write_to_channel("VOLT:RANG "+ str(range), channel)
        return err
    except:
        return err

def get_current_range(channel): # returns the programmed current range on channels
    try:
        err=eth_write_to_channel("CURR:RANG? ", channel,False)
        if err== None:
            time.sleep(sleeptime_GN_FN)
            range = eth_read()
            try:
                range=float(range)
                return range
            except:
                return range
        else:
            return err
    except:
        return "error while getting current range"   

def set_current_slewrate(value,channel): # This command sets the current slew rate in volts per second
    #value :0 - 9.9E+37 | MIN | MAX | INFinity (default:9.9E+37) Values entered are model dependent.
    try:
        err=eth_write_to_channel("CUR:SLEW "+ str(value), channel)
        return err
    except:
        return err
    
def get_current_slewrate(channel): #  returns the remote sense relay state
    try:
        err=eth_write_to_channel("CURR:SLEW? ", channel,False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            value = eth_read()
            return value
        else:
            return err
    except:
        return "error while getting current slew rate"

def set_current_slewrate_max(value,channel): # This command sets the current slew rate maximum override
    #value :OFF | 0 | ON | 1(default:OFF) Values entered are model dependent.
    try:
        err=eth_write_to_channel("CURR:SLEW:MAX "+ str(value), channel)
        return err
    except:
        return err
    
def get_current_slewrate_max(channel): #  returns the remote sense relay state 
    try:
        err=eth_write_to_channel("CURR:SLEW:MAX? ", channel,False)
        if err==None:
            time.sleep(sleeptime_GN_FN)
            value = eth_read() # value: 0/1
            return value
        else:
            return err
    except:
        return "error while getting current max slew rate"



def connect(ip_address, _port):
    global eth_socket,connected
    # Connect
    eth_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    eth_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)
    eth_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 0)
    if eth_socket.connect_ex((ip_address, _port)) == 0:
        connected = True
        print('Connected to N6705B\r\n')
        return 'Connected to N6705B'
    else:
        print('Error while connecting to N6705B')
        return 'Error while connecting to N6705B'
        
def start_logging():
    global run_log
    global values
    global headers
    values = {}
    log_thread = threading.Thread(target=_n6705b_thread, args=(), daemon=True)
    log_thread.name = "N6707B"
    run_log = True
    log_thread.start()    
    
def stop_logging():
    global run_log
    global connected
    global eth_socket
    run_log = False

    if connected:
        connected = False
        eth_socket.close()

def _n6705b_thread():
    global headers
    global values
    global run_log
    global eth_socket
    global connected
    global k
    global time_elapsed
    if connected|TestMode1==True:
        print(threading.current_thread())
        time.sleep(1)
        eth_write("*cls")
        time.sleep(1)

        # main logging loop
        while run_log:
            start = timer()
            message=""
            for c, channel in list(enumerate(channels)): # reading the voltage and current
                voltage = get_voltage(channel)
                current = get_current(channel)
                message=str(voltage)+","+str(current)+";"+message # creating a message 
                
            message=str(k)+";"+message # adding the number of data in the front of the dmessage
            ch_queue.put_nowait(message) # sending the message in the queue
            k = k+1
            end = timer()
            time_elapsed[0]=end - start
            time.sleep(0.5)
            