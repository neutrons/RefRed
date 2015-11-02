import numpy as np

class AsciiLoader(object):
	
	filename = ''
	data_col1 = []
	data_col2 = []
	data_col3 = []
	data_col4 = []
	
	def __init__(self, filename=None, nbr_col=3):
		
		if nbr_col is not 3:
			raise nbrColumnError('only 3 supported for now!')
		
		data = np.genfromtxt(filename, dtype=float, comments='#')
		                    
		self.data_col1 = data[:,0]
		self.data_col2 = data[:,1]
		self.data_col3 = data[:,2]
#		self.data_col4 = data[:,3]
		
	def data(self):
		
		return [self.data_col1, self.data_col2, self.data_col3, self.data_col4]