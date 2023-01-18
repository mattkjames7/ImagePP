import numpy as np
from .LoadData import LoadData
import DateTimeTools as TT
from ._SmoothBoundary import _SmoothBoundary,_SmoothBoundaryGroups

def GetPP(*args,Smooth=0):
	
	if len(args) == 1:
		utc = args[0]
	else:
		Date,ut = args
		utc = TT.ContUT(Date,ut)[0]
		
	
	data = LoadData()
	
	
	dt = np.abs(utc - data.utc)
	I = dt.argmin()



	if dt[I] > 1.0:
		return None
	else:
		out = data[I]

	if Smooth > 0:
		out.x,out.y = _SmoothBoundary(out.x,out.y,Smooth)
		out.xg,out.yg = _SmoothBoundaryGroups(out.xg,out.yg,Smooth)
	
	return out