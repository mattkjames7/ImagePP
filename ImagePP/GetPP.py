import numpy as np
from .LoadData import LoadData
import DateTimeTools as TT

def GetPP(*args):
	
	if len(args) == 1:
		utc = args[0]
	else:
		Date,ut = args
		utc = TT.ContUT(Date,ut)[0]
		
	
	data = LoadData()
	
	
	dt = np.abs(utc - data.utc)
	I = dt.argmin()
	print(I)
	if dt[I] > 1.0:
		return None
	else:
		return data[I]
