import os
import curses
import subprocess
from rich.console import Console
from rich.table import Table
from rich import box

sysinfo = {}
sysinfo['Hostname']=os.uname()[1] # Hostname
sysinfo['Kernel']=os.uname()[0] + ' ' + os.uname()[2] # Kernel
# Distro name
with open('/etc/os-release', 'r') as f:
    for x in f:
        if x.startswith('PRETTY'): 
            sysinfo['Distribution']=(x.strip()[x.strip().find('"')+1:len(x.strip())-1])
sysinfo['Active users']=str(len(list(set(subprocess.check_output("users").decode('utf-8').split())))) # Get active users
sysinfo['Uptime']=subprocess.check_output(["uptime", '-s']).decode('utf-8').strip() # Get uptime 
sysinfo['Shell']=os.environ['SHELL'] # Get shell


table = Table(title="system info", box=box.MINIMAL_DOUBLE_HEAD)
table.add_column('Property')
table.add_column('Value')
for x in range(len(sysinfo)):
    table.add_row(list(sysinfo.keys())[x], sysinfo[list(sysinfo.keys())[x]])
    console = Console()
console.print(table)
