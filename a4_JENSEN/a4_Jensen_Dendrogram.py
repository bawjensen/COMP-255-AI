import re
from numpy import array
from scipy.cluster import hierarchy
import pylab

def main():

	    MIN_HAMILTON = 15
	    MAX_HAMILTON = 65 
	    MIN_JAY = 66
	    MAX_JAY = 70
	    MIN_MADISON = 71
	    MAX_MADISON = 84
	    
	    fin  = open("preprocessedFeatureSet.csv", 'r')
	    #fout = open("commonCount.csv", 'w')

	    dict = {}
	    textNames = []
	    
	    i = 0
	    for line in fin:
			line = line.strip()
			# account of ending comma after last item on the line
			line = line.strip(',')
			if (i == 0): # header
				    texts = line.split(',')
				    # texts[0] will be "word" (don't use)
				    fileNames = texts[1:]
				    #print fileNames
				    # just keep ending of filename
				    for nextName in fileNames:
						#print nextName
						m = re.search('(FED_.+)\.txt$', nextName)
						#print m.group(1)
						textNames.append( m.group(1) )

				    
				    m = 0
				    for next in textNames:
						print m, textNames[m]
						m=m+1
				    
			else:
				    wc = line.split(',')
				    word = wc[0]
				    counts = wc[1:]
				    
				    dict[word] = []
				    for eachCount in counts:
						dict[word].append(0)
				    k = 0
				    for nextCount in counts:
						dict[word][k]=nextCount
						k = k+1
						
				    #print dict[word]
			i = i+1
			
			#if (i > 4):
			#	    exit()
			
			# end next line of data in file
	    
	    fin.close()
		
	    vectors = []
	    for i in range(0, len(textNames)):
			T = []
			for word in dict.keys():
				    T.append(dict[word][i])
			vectors.append(T)
	    
			
	    Z = hierarchy.linkage( vectors[:], method='median', metric='euclidean' )
	    d = hierarchy.dendrogram( Z, labels=textNames[:] )
	    pylab.show()
            
	    
						
	    # (finally) we can keep this word
	    #fout.write("%s"  % line)
	    #wordCount = wordCount + 1
	    # end for each line in file of data

	    
	    #fout.close()
			
	    #print "Number of words appearing in only M, H, and J at least once: ", wordCount
						
			
			
			
# ------------------------------
if __name__ == '__main__':
    main()