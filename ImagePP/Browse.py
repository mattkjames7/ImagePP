import numpy as np
import matplotlib.pyplot as plt
from .LoadData import LoadData
from .PlotPP import PlotPP

class Browse(object):
	def __init__(self,i0=0,fname=None):
		self.I = i0
		self.ax = None
		self.fig = None
		self.fname = fname

		self.data = LoadData()

		self._Plot()
		self._EventHandle()		


	def _Plot(self):
		
		if self.fig is None:
			self.fig = plt.figure(figsize=(8,6))
		else:
			self.fig.clf()

		date = self.data.Date[self.I]
		ut = self.data.ut[self.I]

		self.ax = PlotPP(date,ut,fig=plt,Scatter=True)
		self.ax = PlotPP(date,ut,fig=self.ax,color='grey',zorder=-1)

		hh = np.int32(ut)
		mm = np.int32((ut - hh)*60.0)

		title = '{:d} {:08d} {:02d}:{:02d} UT'.format(self.I,date,hh,mm)
		self.ax.set_title(title)
		plt.draw()

	def _Next(self):
		self.I += 1
		if self.I >= self.data.size:
			self.I = self.data.size - 1
			print('Reached end of samples')
		
	def _Prev(self):
		self.I -= 1
		if self.I < 0:
			self.I = 0
			print('Reached start of samples')

	def _AddtoFile(self):
		if not self.fname is None:
			date = self.data.Date[self.I]
			ut = self.data.ut[self.I]
			out = '{:d} {:08d} {:05.2f}\n'.format(self.I,date,ut)

			f = open(self.fname,'a')
			f.write(out)
			f.close()
			print('Added image to file')

	def _EventHandle(self):
		#create three handlers for key presses, clicks and scrolls
		#assigning a procedure to run for each event type
		self.KeyID=self.fig.canvas.mpl_connect('key_press_event',self._OnKey)
		self.MouseID=self.fig.canvas.mpl_connect('button_press_event',self._OnClick)
		self.ScrollID=self.fig.canvas.mpl_connect('scroll_event',self._OnScroll)
	
	#For keyboard presses
	def _OnKey(self,event):

		#the event argument is automatically passed through by the event handler	
		if event.key == 'n':
			self._Next()
			self._Plot()
		elif event.key == 'b':
			self._Prev()
			self._Plot()
		elif event.key == 'a':
			self._AddtoFile()
			self._Next()
			self._Plot()
		elif event.key == 'q':
			self._EventUnHandle()
			plt.close()
		else:
			pass
		
	def _OnClick(self,event):
		if not event.inaxes is None:
			pass
	def _OnScroll(self,event):
		pass

	def _EventUnHandle(self):
		self.fig.canvas.mpl_disconnect(self.KeyID)
		self.fig.canvas.mpl_disconnect(self.MouseID)
		self.fig.canvas.mpl_disconnect(self.ScrollID)
