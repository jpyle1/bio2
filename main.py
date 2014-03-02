import sys,optparse,random

class HopfieldNetwork(object):
	"""
		Responsible for holding information relating to the network.
	"""
	def __init__(self,numRuns,numPatterns,numNeurons):
		self._numRuns = numRuns	
		self._numPatterns = numPatterns
		self._numNeurons = numNeurons
		randVal = lambda : 1 if random.random()>=.5 else -1 
		self._patterns = ([[randVal() for x in xrange(numNeurons)] 
			for y in xrange(numPatterns)]) 
		self._weights = [[0]*self._numNeurons]*self._numNeurons				

	@property
	def numPatterns(self):
		return self._numPatterns
	
	@numPatterns.setter
	def numPatterns(self,value):
		self._numPatterns = value

	@property
	def numNeurons(self):
		return self._numNeurons

	@numNeurons.setter
	def numNeurons(self,value):
		self._numNeurons = value	

	@property
	def numRuns(self):
		return self._numRuns
	
	@numRuns.setter
	def numRuns(self,value):
		self._numRuns = value

	def _buildWeightString(self):
		getStr = lambda x,y: str(x)+":"+str(y)
		return "\n".join(map(getStr,xrange(self._numNeurons),self._weights))
	
	def _buildPatternString(self):
		getStr = lambda x,y: "P"+str(x)+":"+str(y)
		return "\n".join(map(getStr,xrange(self._numPatterns),self._patterns))

	def _getPatCol(self,idx):
		return map(lambda x: x[idx],self._patterns)

	def imprintPatterns(self,maxPat):	
		cosMul = lambda x,y,p: 0 if p == None  else x*y 
		self._weights = (
		[[ 0 if i==j else 
 		sum(map(cosMul,self._getPatCol(i),self._getPatCol(j),xrange(maxPat)))/
		float(self._numNeurons) for i in xrange(self._numNeurons)] 
		for j in xrange(self._numNeurons)]) 		

	def calcStableStats(self,maxPat):
		cosMul = lambda x,y: x*y
		neurons = [[ 
			1 if sum(map(cosMul,self._weights[i],self._patterns[k]))>=0
			else -1 
			for i in xrange(self._numNeurons)] 
			for k in xrange(maxPat)]
		
		#getStr = lambda x,y: str(x)+":"+str(y)	
		#print "\n".join(map(getStr,xrange(maxPat),neurons))
				

	def __str__(self):
		tempStr = ""
		tempStr+="numRuns:"+str(self._numRuns)+"\nnumPatterns:"+str(self._numPatterns)
		tempStr+="\nnumNeurons:"+str(self._numNeurons)
		tempStr+="\nPatterns:"
		tempStr+="\n"+self._buildPatternString()
		tempStr+="\nWeights:"
		tempStr+="\n"+self._buildWeightString()
		return tempStr

def main(hn):
	"""
		Main entry point  of the program.
	"""	
	#print hn	
	hn.imprintPatterns(hn.numPatterns)
	print hn
	hn.calcStableStats(hn.numPatterns)
	#for p in xrange(hn.numPatterns):	
	#	hn.imprintPatterns(p) 
	#	print hn.calcStableStats(p)

if __name__ == "__main__":
	#Seed the random network.
	random.seed()
	#Initialize a default hopfield network.
 	hn = HopfieldNetwork(50,50,100)
	parser = optparse.OptionParser()
	parser.add_option("--numRuns")
	parser.add_option("--numPatterns")
	parser.add_option("--numNeurons")
	(options,args) = parser.parse_args()
	if(options.numRuns is not None):
		hn.numRuns = int(options.numRuns)
	if(options.numPatterns is not None):
		hn.numPatterns = int(options.numPatterns)
	if(options.numNeurons is not None):
		hn.numNeurons = int(options.numNeurons)
	main(hn)

