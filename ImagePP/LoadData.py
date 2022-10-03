import numpy as np
from . import Globals
import PyFileIO as pf

def LoadData():
	
	if Globals.Data is None:
		fname = Globals.DataPath + 'pp.bin'
		Globals.Data = pf.LoadObject(fname)
		
	return Globals.Data
