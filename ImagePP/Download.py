import numpy as np
from . import Globals
from .ListFiles import ListFiles
import os
from ._Convert import _Convert

def Download():
	
	tmppath = Globals.DataPath + 'tmp/'
	ppapath = Globals.DataPath + 'ppa/'
	
	paths = [tmppath,ppapath]
	for p in paths:
		if not os.path.isdir(p):
			os.makedirs(p)
	
	
	
	#download the archives
	url = "http://enarc.space.swri.edu/EUV/ppa_Manual/"
	files0 = ["2000.zip","2001.zip","2002.zip","2003.zip","2004.zip"]
	tmps = []
	for i,f in enumerate(files0):
		newf = tmppath + '{:d}.zip'.format(i)
		tmps.append(newf)
		os.system('wget '+url+f+' -O '+newf)
	
	#extract the files
	CWD = os.getcwd()
	os.chdir(tmppath)
	for t in tmps:
		os.system('unzip '+t)
	
	#move them to ppa directory
	os.system('mv -f */*.ppa ../ppa/')
	os.chdir(CWD)
	
	#convert them
	_Convert(ppapath)
