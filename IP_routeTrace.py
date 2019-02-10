
# python script to trace the route of the ip packet with all intermediate devices found till it reaches the target destination 

import os
import socket 
#from scapy.all import *
from tabulate import tabulate
import time
import scapy 
import sys



import time 
# script banner print



logo = """ \033[1m \033[91m    
       ____ ____ _  _ ___ ____   _____  
       |__| |  | |  |  |  |___ ____|      
       |  | |__| |__|  |  |___     |   


                                       


Program technology: Python Scapy Framework.....




[*] Starting python packet route tracer .....
[*] Started  tracing the packet route...
[*] Wait for a while .....

"""

print logo 

ipadress = ""   # string buffer object to store the ip addresses 

ans_unans = []
table = []  # table list object 

headers = ["TTL Value", "IP Adresses", "Target"]  # table parameters   where ttl is time to live value 

if len(sys.argv) < 2:
	print "argument required...exiting"  # argument count   verification 
else:

	try:

                packet = sr1(IP(dst="195.175.39.49")/UDP()/DNS(rd=1, qd=DNSQR(qname=sys.argv[1])), verbose=False)
                ip_adress = packet[1][DNSRR].rdata

	except:

		ipadress = sys.argv[1]
	for i in range(1,20):
		ans,unans = sr(IP(dst=ipadress, ttl=i)/ICMP(), verbose=False ,retry=3, timeout=0.5)
		time.sleep(0.01)   # time lag gap value 
	
		for send, rcv in ans:
                              
			if rcv.type == 11:

				table.append([i, rcv.src, "\033[94m Intermediate-Device IP \033[0m"])

			else:
				table.append([i, rcv.src, "\033[92m Final Ip \033[0m"])
				print ans 

				print ""
				print tabulate(table, headers)
				
				print ""
				sys.exit()  # exiting from the script  
	print tabulate(table, headers)

