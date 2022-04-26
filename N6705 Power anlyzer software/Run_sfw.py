# This script can be used to configure some parameters and run the hole software( GUI and the controler ).
from GUİ import*
from VP_function import *
import time
connect("192.168.214.9",5025)
configure((1,2,3,4),(5,2,1,1),(1,2,1,1))
power_on()
start_logging()
time.sleep(1)
startGUİ()
while True:
    time.sleep(1)
    