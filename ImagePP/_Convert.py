import numpy as np
from .ListFiles import ListFiles
from ._ReadPPA import _ReadPPA
import os
import DateTimeTools as TT
import PyFileIO as pf
from . import Globals
from ._SortPP import _SortPP

def _Convert(ppapath):
	
	#list all of the ppa files
	files,names = ListFiles(ppapath,ReturnNames=True)
	nf = files.size
	
	#read all of the ppa files in
	ppa = []
	Date = []
	ut = []
	n = 0
	for i in range(0,nf):
		print('\rReading File {:d} of {:d}'.format(i+1,nf),end='')
		nam,ext = os.path.splitext(names[i])
		yr = np.int32(nam[:4])
		dy = np.int32(nam[4:7])
		hr = np.int32(nam[7:9])
		mn = np.int32(nam[9:11])
			

			
		tmp = _ReadPPA(files[i])
		ppa.append(tmp)

		Date.append(TT.DayNotoDate(yr,dy)[0])
		ut.append(np.float32(hr) + np.float32(mn)/60.0)
			
		n += 1
	print()
	print('Done reading')
	#create an output data type
	dtype = [	('Date','int32'),
				('ut','float32'),
				('utc','float64'),
				('L','object'),
				('MLT','object'),
				('Cn','object'),
				('Sn','object'),
				('x','object'),
				('y','object'),
				('ng','int32'),
				('grps','object'),
				('xg','object'),
				('yg','object')]
	out = np.recarray(n,dtype=dtype)			
	
	#fill them in
	out.Date = np.array(Date)
	out.ut = np.array(ut)
	out.utc = TT.ContUT(out.Date,out.ut)
	for i in range(0,n):
		print('\rConverting File {:d} of {:d}'.format(i+1,n),end='')
		out.L[i] = ppa[i][0]
		phi = ppa[i][1]
		out.MLT[i] = (phi*12/np.pi + 12) % 24
		out.Cn[i] = ppa[i][2]
		out.Sn[i] = ppa[i][3]
		out.x[i] = out.L[i]*np.cos(phi)
		out.y[i] = out.L[i]*np.sin(phi)
		out.grps[i] = _SortPP(out.x[i],out.y[i])
		out.ng[i] = len(out.grps[i])
		out.xg[i] = []
		out.yg[i] = []
		for j in range(0,out.ng[i]):
			out.xg[i].append(out.x[i][out.grps[i][j]])
			out.yg[i].append(out.y[i][out.grps[i][j]])
	print()
	print('Done converting')
	#save it
	binfile = Globals.DataPath + 'pp.bin'
	pf.SaveObject(out,binfile)
	print('Saved '+binfile)
