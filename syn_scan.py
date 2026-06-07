from scapy.all import *

ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3232, 5900, 8080]

def Syn_scanner(Target):
    answered , unanswered = sr(
         IP(dst = Target ) / 
         TCP(sport = 555, dport = ports, flags = "S"),
         timeout = 8,
         verbose = 0 # how much extra information to print 
         #(0 = none, 1 = summary, 2 = full details
    )



    print("Open ports on " + Target + ":") 
    for sent , recived in answered: # see the img below
        if sent[TCP].dport == recived[TCP].sport:
            if recived[TCP].flags == "SA": # SYN-ACK
                print(f" port {sent[TCP].dport} is open")
            elif recived[TCP].flags == "RA": # RST-ACK
                print(f"port {sent[TCP].dport} is closed")


Syn_scanner("192.168.56.1")       


