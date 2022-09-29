import numpy as np
import PyFileIO as pf

def _ReadPPA(fname):
	
	
	
	#read the file
	lines = pf.ReadASCIIFile(fname)
	nl = lines.size
	
	#find the line containing L and phi
	i0 = 0
	for i in range(0,nl):
		if 'L' in lines[i] and 'phi' in lines[i]:
			i0 = i
			break
	
	#find first line which can't be split intto two elements
	i1 = np.copy(i0)
	for i in range(i0,nl):
		s = lines[i].split()
		if len(s) != 2:
			i1 = i
			break
			
	#find Cn,Sn and Multiplier
	iC = 0
	iS = 0
	iM = 0
	for i in range(i1,nl):
		if lines[i].startswith('Cn'):
			iC = i
		
		if lines[i].startswith('Sn'):
			iS = i
		
		if lines[i].startswith('Multiplier'):
			iM = i + 1
			
		if (iM > 0) and (iC > 0) and (iS > 0):
			break
			
	#get L and phi
	lineslp = lines[i0+1:i1]
	n = lineslp.size
	L = np.zeros(n,dtype='float32')
	phi = np.zeros(n,dtype='float32')
	for i in range(0,n):
		s = lineslp[i].split()
		L[i] = np.float32(s[0])
		phi[i] = np.float32(s[1])
		
	#get Multiplier
	Mult = np.float32(lines[iM])
		
		
	#get Cn
	lCn = lines[iC]
	ic0 = lCn.find('[')
	ic1 = lCn.rfind(']')
	Cn = np.float32(lCn[ic0+1:ic1].split(','))/Mult
	
	
	#get Sn
	lSn = lines[iS]
	is0 = lSn.find('[')
	is1 = lSn.rfind(']')
	Sn = np.float32(lSn[is0+1:is1].split(','))/Mult
	
	return L,phi,Cn,Sn
		
	
