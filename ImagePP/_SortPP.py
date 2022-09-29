import numpy as np
import copy

def _Dist(d,ind):
	
	return np.sum(d[ind[:-1],ind[1:]])
	
	
def _Swap(ind,i,j):
	tmp = ind[i]
	ind[i] = ind[j]
	ind[j] = tmp	
	
	return ind

def _SwapSort(d):
	
	n,_ = d.shape
	
	#start with an initial sorting order
	ind = np.arange(n)
	
	#calculate the current distance
	min_dist = _Dist(d,ind)
	p_dist = np.copy(min_dist)
	
	#loop through each point, attempting to reduce the path length
	maxit = 100
	nit = 0
	nsame = 0

	while nit < maxit:
		p_dist = np.copy(min_dist)
		#test some swaps
		for i in range(0,n):
			for j in range(0,n):
				ind = _Swap(ind,i,j)
				dist = _Dist(d,ind)
				if dist >= min_dist:
					#swap back
					ind = _Swap(ind,i,j)
				else:
					min_dist = np.copy(dist)
					print(nit,min_dist)
		if min_dist == p_dist:
			nsame += 1
		if nsame == 2:
			break
		nit += 1	

	return ind
	
def _NearestNeighbours(d):
	
	n,_ = d.shape
	
	#start at the beginning of the array
	c = 0
	
	#this is the remainging indices to do
	ind = list(np.arange(n)[1:])
	
	#this will be the output array
	out = [c]

	#loop through until there are no indexes to sort
	for i in range(0,n-1):
		#find the closest point to the beginning
		ind0 = ind[d[out[0],ind].argmin()]
		d0 = d[out[0],ind0]	
		
		#and closest to the end
		ind1 = ind[d[out[-1],ind].argmin()]
		d1 = d[out[-1],ind1]		

		#add the closest of the two
		if d0 < d1:
			out.insert(0,ind0)
			ind.remove(ind0)
		else:
			out.append(ind1)
			ind.remove(ind1)
			
	return np.array(out)
	
def _SplitGroups(ind,d,dmax):
	
	#distance between each element
	di = d[ind[:-1],ind[1:]]
	
	bad = np.where(di > dmax)[0] + 1
	i0 = np.append(0,bad)
	i1 = np.append(bad,ind.size)
	ng = i0.size
	
	#split
	grps = []
	for i in range(0,ng):
		grps.append(ind[i0[i]:i1[i]])
		
	return grps
	
def _Regroup(grps,x,y,dmax):
	
	
	ng0 = len(grps)
	png = len(grps)
	ng = len(grps)
	
	
	nit = 0
	while (ng > 1) and (nit < ng0-1):
		png = np.copy(ng)
		nxt = False
		for i in range(0,ng):
			for j in range(0,ng):
				if not j == i:
					x0 = np.array([x[grps[i]]])
					y0 = np.array([y[grps[i]]])
				
					x1 = np.array([x[grps[j]]]).T
					y1 = np.array([y[grps[j]]]).T
					
					dx = x1 - x0
					dy = y1 - y0
					d = np.sqrt(dx**2 + dy**2)
					
					if d.min() < dmax:
						#merge the two groups
						i0,i1 = np.where(d == d.min())
						i0 = i0[0]
						i1 = i1[0]
						
						g0a = grps[i][:i1]
						g0b = grps[i][i1:]
						g1 = grps[j]
						g = np.concatenate((g0a,g1,g0b))
						
						
						grps[i] = g
						grps.pop(j)
						
						nxt = True
				
					if nxt:
						break 	
			
			if nxt:
				break
		nit += 1

		
		ng = len(grps)
		if ng == png:
			break


	return grps

def _SortPP(x,y):
	
	#create a matrix of all of the distances between each pair of points
	n = np.size(x)
	x0 = np.array([x])
	y0 = np.array([y])
	x1 = x0.T
	y1 = y0.T
	
	dx = (x0 - x1)**2
	dy = (y0 - y1)**2
	
	d = np.sqrt(dx + dy)
	
	#this is slow and requires everyting to be srted in a fairly decent order in advance
	#ind = _SwapSort(d)
		
	
	#this doesn't always work
	ind = _NearestNeighbours(d)
	
	
	#split into groups
	grps = _SplitGroups(ind,d,0.5)
	
	#rejoin some groups if possible
	#this definitely doesn't work
	#grps = _Regroup(grps,x,y,0.5)
	
	return grps
	
	
	
	#the stuff below does not work
	# #start with the first point
	# todo = list(np.arange(x.size,dtype='int32'))
	# c = todo.pop(0)
	# done = []
	# while len(todo) > 0:
		# #find the closest index of the todo array to the current
		# indtd = todo[d[c][todo].argmin()]
		# dtd = d[c][indtd]
		
		# #distance to first element
		# if len(done) > 0:
			# d0 = d[c][done[0]]
		# else:
			# d0 = np.inf
			
		# #choose the closest one
		# if d0 < dtd:
			# done.insert(0,c)
		# else:
			# done.append(c)
			
		# if len(todo) == 0:
			# break
		# c = todo.pop(0)
	
	# d0 = d[c][done[0]]
	# d1 = d[c][done[-1]]
	
	# if d0 < d1:
		# done.insert(0,c)
	# else:
		# done.append(c)
	
	# return done
