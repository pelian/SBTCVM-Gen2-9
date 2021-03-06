#!/usr/bin/env python
from . import libbaltcalc
btint=libbaltcalc.btint
import os
import sys
VMSYSROMS=os.path.join("VMSYSTEM", "ROMS")
def loadtrom(fname):
	for filenameg in [fname, fname+".trom", fname+".TROM"]:
		if os.path.isfile(filenameg):
			return(open(filenameg, "r"))
		elif os.path.isfile(os.path.join("ROMS", filenameg)):
			return(open(os.path.join("ROMS", filenameg), "r"))
		elif os.path.isfile(os.path.join("VMUSER", filenameg)):
			return(open(os.path.join("VMUSER", filenameg), "r"))
		elif os.path.isfile(os.path.join("VMSYSTEM", filenameg)):
			return(open(os.path.join("VMSYSTEM", filenameg), "r"))
		elif os.path.isfile(os.path.join(VMSYSROMS, filenameg)):
			return(open(os.path.join(VMSYSROMS, filenameg), "r"))
	sys.exit("ERROR: Nonexistant TROM!")
	


class memory:
	def __init__(self, trom):
		self.trom=trom
		self.INSTDICT={}
		self.DATDICT={}
		linecnt=libbaltcalc.mni(9)
		print("Setting up Virtual RAM subsystem")
		TROMFILE=loadtrom(trom)
		for rmline in TROMFILE:
			rmline=rmline.replace("\n", "").split(",")
			self.INSTDICT[linecnt]=btint(int(rmline[0]))
			self.DATDICT[linecnt]=btint(int(rmline[1]))
			linecnt += 1
		TROMFILE.close()
		#pad memory map to max size if not already maxxed.
		while linecnt<=libbaltcalc.mpi(9):
			self.INSTDICT[linecnt]=btint(0)
			self.DATDICT[linecnt]=btint(0)
			linecnt += 1
		print("Virtual RAM ready: " + str(len(self.DATDICT)) + " data words, \n" + str(len(self.INSTDICT)) + " instruction words\n")
	#memory read
	def getinst(self, addr):
		return self.INSTDICT[int(addr)]
	def getdata(self, addr):
		return self.DATDICT[int(addr)]
	#memory write
	def setinst(self, addr, value):
		(self.INSTDICT[int(addr)]).changeval(value)
	def setdata(self, addr, value):
		(self.DATDICT[int(addr)]).changeval(value)