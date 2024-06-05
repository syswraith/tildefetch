import os
import time
import subprocess
import curses
from curses import wrapper

club = """
 ███╗  ██████╗
██╔██╗██╔════╝
╚═╝╚═╝██║     
      ██║     
      ╚██████╗
       ╚═════╝
""".splitlines()

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

stdscr = curses.initscr()

# Window calculations
window_y, window_x = curses.LINES, curses.COLS
window_y = (window_y-1)//2 if window_y%2!=0 else window_y//2
window_x = (window_x-1)//2 if window_x%2!=0 else window_x//2

ascii_window = curses.newwin(window_y, window_x//2, 0, 0)
text_window = curses.newwin(window_y, window_x//2, 0, window_x)


def main(stdscr):
       curses.curs_set(0)

       for line in range(len(club)):
           padding = len(club) + line
           ascii_window.addstr(padding, 0, club[line].center(window_x//2-len(max(club, key=len))//2))
           ascii_window.refresh()
    
       for info in range(len(sysinfo.keys())):
           key = list(sysinfo.keys())[info]
           padding = (window_y - len(sysinfo.keys())) + info
           text_window.addstr(padding, 0, f'{key}: {sysinfo[key]}')
       text_window.refresh()
   
       stdscr.getkey()

curses.endwin() 
wrapper(main)
