import numpy as np


def _SmoothBoundaryGroups(xg,yg,n):
	'''
	smooth a rough boundary if needed
	
	Inputs
	======
	xg : float
		array of groups of x-coords - each group is
		smoothed independently
	yg : float
		array of groups of y-coords
	n : int
		number of points to smooth over
	
	
	'''
	
	xout = []
	yout = []
	for x,y in zip(xg,yg):
		xs,ys = _SmoothBoundary(x,y,n)
		xout.append(xs)
		yout.append(ys)
		
	return xout,yout

def _SmoothBoundary(x,y,n):
	'''
	
	'''
	#convert to L and M
	L = np.sqrt(x**2 + y**2)
	M = np.arctan2(-y,-x)*12/np.pi


	srt = np.argsort(M)
	L = L[srt]
	M = M[srt]
	xs = x[srt]
	ys = y[srt]
	
	for i in range(0,M.size-1):
		dm = M[i+1] - M[i]
		if dm > 12:
			M[i+1:] -= 24.0
		elif dm < -12:
			M[i+1:] += 24.0
	
	o = np.ones(n)/n

	xout = np.convolve(xs,o,'valid')
	yout = np.convolve(ys,o,'valid')

	return xout,yout


