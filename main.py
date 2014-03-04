import sys,optparse,random,copy
import matplotlib as mpl
import pylab as plt

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

	def _genPerms(self):
		indices =  [i for i in xrange(self._numNeurons)]
		random.shuffle(indices,random.random)
		return indices
	
	def calcStableStats(self,maxPat):
		cosMul = lambda x,y: x*y
		neurons = [[ 
			1 if sum(map(cosMul,self._weights[i],self._patterns[k]))>=0
			else -1 
			for i in xrange(self._numNeurons)] 
			for k in xrange(maxPat)]	
		cat = lambda x,y: (x,y)
		comp = lambda x: x[0] == x[1]
		compCorr = lambda x: x==self._numNeurons
		values = [len(filter(comp,map(cat,self._patterns[i],neurons[i]))) 
			for i in xrange(maxPat)]
		basinSizes = [ 0 for x in xrange(self._numPatterns)]
		#Generate 5 different permutations.
		perms = [ self._genPerms() for x in xrange(5) ]			
		for perm in perms:
			#Flip the new patterns..
			for i in xrange(maxPat):
				if values[i] == False:
					basVal[0]+=1
					continue
				#Copy the old patterns.
				modPatterns = copy.deepcopy(self._patterns[i])
				basVal = 0
				for j in xrange(50):
					modPatterns[perm[j]] = self._patterns[i][perm[j]]*-1
					upPatterns = copy.deepcopy(modPatterns)
					#Update 10 times...		
					for x in xrange(10):
						upPatterns = [
							1 if sum(map(cosMul,upPatterns,self._weights[z]))>=0
							else -1
							for z in xrange(self._numNeurons)]
					if (len(filter(comp,map(cat,self._patterns[i],upPatterns)))!= 
					self._numNeurons):
						basVal = j
						break
				basinSizes[basVal]+=1 		
		r = filter(compCorr,values)
		return (len(r),maxPat-len(r),maxPat,basinSizes)

	def __str__(self):
		tempStr = ""
		tempStr+="numRuns:"+str(self._numRuns)+"\nnumPatterns:"+str(self._numPatterns)
		tempStr+="\nnumNeurons:"+str(self._numNeurons)
		tempStr+="\nPatterns:"
		tempStr+="\n"+self._buildPatternString()
		tempStr+="\nWeights:"
		tempStr+="\n"+self._buildWeightString()
		return tempStr

def unGrad(hn,p):
	print p
	hn.imprintPatterns(p)
	return hn.calcStableStats(p)

def getColReg(x,idx):
	return map(lambda x: x[id])

def getCol(x,idx,stat):
	return map(lambda x: x[idx][stat],x)

def getProbCol(x,idx):
	return map(lambda x: x[idx][1]/float(x[idx][2]),x)
	
def getRows(x,idx):
	return map(lambda x: x[idx],x)

def getColumns(x,idx):
	return map(lambda x: x[idx],x)

def main(hn):
	"""
		Main entry point  of the program.
	"""
	results = [[unGrad(hn,p)	
		for p in xrange(1,hn.numPatterns+1)]
		for run in xrange(hn.numRuns)]
 
	avgStable = [	
		sum(getCol(results,p-1,0))/float(hn.numRuns)	
		for p in xrange(1,hn.numPatterns+1)]

	probNotStable = [
		sum(getProbCol(results,p-1))/float(hn.numRuns)
		for p in xrange(1,hn.numPatterns+1)]

	basins = [[
		currentTuple[3]
		for currentTuple in run]		
		for run in results] 

	avgBasins = [[
		sum(getColumns(getRows(basins,i),j))/float((hn.numRuns*(i+1)))
		for j in xrange(hn.numPatterns)]
		for i in xrange(hn.numPatterns)]

	print avgBasins


	plt.figure(1)
	plt.subplot(211)
	plt.plot(xrange(hn.numPatterns),avgStable)
	plt.ylim([0,20])	
	plt.subplot(212)
	plt.plot(xrange(hn.numPatterns),probNotStable)
	plt.ylim([0,1.1])

	plt.figure(2)
	plt.subplot(211)
	xVals = xrange(hn.numPatterns)
	[plt.plot(xVals,avgBasins[j]) for j in xrange(1,hn.numPatterns,2)]		
	plt.show()

if __name__ == "__main__":
	#Seed the random network.
	random.seed()
	#Initialize a default hopfield network.
 	hn = HopfieldNetwork(2,50,100)
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

