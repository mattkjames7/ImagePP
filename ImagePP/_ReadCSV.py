import numpy as np
import PyFileIO as pf
from .ListFiles import ListFiles
from . import Globals
import os

def _ReadCSV(fname):

	data = pf.ReadASCIIData(fname,Header=False,dtype=[('x','float64'),('y','float64')])

	L = np.sqrt(data.x**2 + data.y**2)
	Phi = np.arctan2(data.y,data.x)

	#extract date and time fromt he file name
	bname = os.path.splitext(os.path.basename(fname))[0]
	ds,ts = bname.split('-')
	Date = np.int32(ds)
	ut = np.float64(ts)


	return Date,ut,L,Phi

def _FindCSV():

	#search directories

	#firstly lookin the module/__data/csv path
	mdata = Globals.ModuleDataPath + 'csv/'
	mfiles = ListFiles(mdata)
	keep = np.zeros(mfiles.size,dtype='bool')
	for i in range(0,mfiles.size):
		if os.path.splitext(mfiles[i])[-1] == '.csv':
			keep[i] = True
	mfiles = mfiles[keep]

	#secondly look in the data path
	ddata = Globals.DataPath + 'csv/'
	if os.path.isdir(ddata):
		dfiles = ListFiles(ddata)
		keep = np.zeros(dfiles.size,dtype='bool')
		for i in range(0,dfiles.size):
			if os.path.splitext(dfiles[i])[-1] == '.csv':
				keep[i] = True
		dfiles = dfiles[keep]
	else:
		dfiles = np.array([],dtype='object')

	#join them
	csvfiles = np.append(mfiles,dfiles)

	return csvfiles

def _ReadAllCSV():

	files = _FindCSV()

	#read each one
	Date = []
	ut = []
	csv = []
	for i,f in enumerate(files):
		print('\rReading CSV {:d} of {:d}'.format(i+1,files.size),end='')
		d,t,L,Phi = _ReadCSV(f)
		Date.append(d)
		ut.append(t)
		csv.append((L,Phi,None,None))
	print()

	return Date,ut,csv

