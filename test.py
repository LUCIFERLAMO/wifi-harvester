from scapy.all import *

#performig a tcp sync scan 

ports = [25,80,53,443,445,8080]

def Tcp_syn_scan(host):
   answered = sr(IP(dst=host)/TCP(sport=5555,dport=ports,flags="S"),verbose=0,timeout=5)[0]
   for s,r in answered:
      if s[TCP].dport == r[TCP].sport:
         print(s[TCP].dport)


# calling the dns function

def Dns_function(host):
   answered = sr(IP(dst=host)/UDP(sport=5555,dport=53)/DNS(rd=1, qd=DNSQR(qname="google.com")),verbose=0,timeout=5)[0]
   if answered:
      print("dns server at host")


   
Tcp_syn_scan("8.8.8.8")
Dns_function("8.8.8.8")
