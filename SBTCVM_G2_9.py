#!/usr/bin/env python
import VMSYSTEM.libbaltcalc as libbaltcalc
from VMSYSTEM.libbaltcalc import btint
import VMSYSTEM.MEM_G2x_9
import VMSYSTEM.CPU_G2x_9
import VMSYSTEM.IO_G2x_9
import VMSYSTEM.UIO_CURSES_G2x_9 as UIO
import time
import sys
import os
import curses
from threading import Thread
progrun=1

try:
	cmd=sys.argv[1]
except:
	cmd=None
try:
	arg=sys.argv[2]
except:
	arg=None
if cmd in ['help', '-h', '--help']:
	print('''SBTCVM Gen2-9 virtual machine. curses frontend.
help, -h, --help: this help.
-v, --version: VM version''')
elif cmd in ['-v', '--version']:
	print('v2.1.0.PRE-ALPHA')
else:
	slow=0
	if cmd==None:
		romfile='TESTSHORT.TROM'
	elif cmd in ['-r', '--run']:
		if arg==None:
			sys.exit("Error! Must specify trom to run!")
		romfile=arg
	elif cmd in ['-s', '--slow']:
		if arg==None:
			sys.exit("Error! Must specify trom to run!")
		romfile=arg
		slow=1
	else:
		romfile=cmd
	
	try:
		
		print("SBTCVM Generation 2 9-trit VM, v2.1.0.PRE-ALPHA\n")
		#initialize memory subsystem
		memsys=VMSYSTEM.MEM_G2x_9.memory(romfile)
		#initialize IO subsystem
		iosys=VMSYSTEM.IO_G2x_9.io()
		
		cpusys=VMSYSTEM.CPU_G2x_9.cpu(memsys, iosys)
		curses.initscr()
		curses.noecho()
		curses.cbreak()
		mainscr=curses.initscr()
		mainscr.keypad(1)
		
		#basic mainloop.
		mhig, mwid = mainscr.getmaxyx()
		statwin = curses.newwin(2, mwid, 0, 0)
		ttywin = curses.newwin(mhig-2, mwid, 2, 0)
		maxy, maxx=ttywin.getmaxyx()
		
		ttywin.addstr(maxy-1, 0, "SBTCVM Curses frontend. SBTCVM Gen2-9 v2.1.0")
		ttywin.scrollok(1)
		ttywin.scroll(1)
		ttywin.refresh()
		#statwin.addstr("r1: 0, r2: 0")
		#statwin.refresh()
		
		uiosys = UIO.uio(cpusys, memsys, iosys, statwin, ttywin)
		
		dispthr=Thread(target = uiosys.statup, args = [])
		dispthr.daemon=True
		dispthr.start()
		uiosys.ttyraw("ready.")
		while progrun:
			time.sleep(0.0001)
			if slow:
				time.sleep(0.5)
			retval=cpusys.cycle()
			if retval!=None:
				progrun=0
				uiosys.run=0
				curses.echo()
				curses.endwin()
				print("VMSYSHALT " + str(retval[1]) + ": " + retval[2])
				
	#in case of drastic failure, shutdown curses!
	finally:
		if progrun:
			uiosys.run=0
			curses.endwin()
		
			
