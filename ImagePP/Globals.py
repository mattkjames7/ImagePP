import numpy as np
import os

ModulePath = os.path.dirname(__file__)+'/'
StationPath = ModulePath+'__data/'
try:
	DataPath = os.getenv('PLASMAPAUSE_DATA')+'/'
except:
	DataPath = ''
	print('Please set $PLASMAPAUSE_DATA')
TmpPath = os.getenv('HOME')+'/.tmp/'
if not os.path.isdir(TmpPath):
	os.system('mkdir -pv '+TmpPath)

Data = None
