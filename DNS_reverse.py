import dns
import dns.resolver
import socket
import os

# making a dns request 


def DNS_Request(Domain):
    try:
        result = dns.resolver.resolve(Domain,"A")
        if result:
            for i in result:
                print(Reverse_dns(i.to_text()))
    except Exception as e:
        print("Some Error")

def Reverse_dns(IP):
    try:
      Domain_name = socket.gethostbyaddr(IP)
    except: 
        return []
    return [Domain_name[0]] + Domain_name[1]

def find_sub_domain(Domain,dictionary,nums):
    for word in dictionary:
        sub_domain = word + "." + Domain
        DNS_Request(sub_domain)

        if nums:
          for i in range(0,10):
           s = word+str(i)+"."+Domain
           DNS_Request(s)


result = []            
if os.path.exists("Subdomain_names"):
   with open("Subdomain_names","r")as f:
      result = f.read().splitlines()


domain = "google.com"
dictionary = result
nums = False

find_sub_domain(domain,dictionary,nums)
   