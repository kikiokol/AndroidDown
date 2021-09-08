# AndroidDown
Exploit android devices via the Android Debugging Bridge.

# Installation

git clone https://github.com/kikiokol/AndroidDown.git \
cd AndroidDown \
chmod +x install.sh \
./install.sh

# Usage

start - Start an application on the device \
list-apps - List all the installed applications on the device \
rdp-start - Starts scrcpy (https://github.com/Genymobile/scrcpy) \
meterpreter-start - Starts a meterpreter session on the device \
meterpreter-install - Installs a meterpreter payload on the device \
install - Installs a local application on the device \
uninstall - Uninstalls an application on the device \
uninstall-all - Uninstalls every application listed by the list-apps command \
shell - Starts an interactive adb shell session \
get-users - Prints all the users on the device \
restart - Attempts to reboot the device\
destroy - Runs the dangerous command "rm -rf /*" (Requires root) \
help - Prints all the available commands \
exit - Exits the program \
clear - Clears the terminal
