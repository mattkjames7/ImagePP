import numpy as np
import matplotlib.pyplot as plt
import DateTimeTools as TT
from .GetPP import GetPP
from .PlotPlanet import PlotPlanet
from ._SmoothBoundary import _SmoothBoundary,_SmoothBoundaryGroups


def PlotPP(*args,fig=None,maps=[1,1,0,0],Scatter=False,Smooth=0,SmoothGroups=0,**kwargs):
	
	data = GetPP(*args)
	
	if data is None:
		return
	
	if fig is None:
		fig = plt
		fig.figure()
	if hasattr(fig,'Axes'):	
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		ax.set_xlim(6,-6)
		ax.set_ylim(-6,6)
		ax.set_aspect(1.0)
		ax.set_xlabel('$y_{sm}$')
		ax.set_ylabel('$x_{sm}$')
	else:
		ax = fig

	if not 'color' in kwargs:
		kwargs['color'] = 'black'

	if Smooth > 0:
		xg,yg = _SmoothBoundary(data.x,data.y,Smooth)
		xg = [xg]
		yg = [yg]
	elif SmoothGroups > 0:
		xg,yg = _SmoothBoundaryGroups(data.xg,data.yg,SmoothGroups)
	else:
		xg,yg = data.xg,data.yg
	for x,y in zip(xg,yg):
		if Scatter:
			ax.scatter(y,x,marker='.',**kwargs)
		else:
			ax.plot(y,x,marker=',',**kwargs)
		
	PlotPlanet(ax)
	return ax
