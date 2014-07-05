
import pylab
from numpy import array
from scipy.cluster import hierarchy
 
vectors = [  [10,0,0,0,0], [5,5,0,0,0], [0,0,10,0,0], 
             [2,2,2,2,2],  [0,0,0,5,5], [0,0,0,1,9], [0,0,0,0,10] ] 

texts = [ 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7' ]

Z = hierarchy.linkage( vectors, method='centroid', metric='euclidean' )

d = hierarchy.dendrogram( Z, labels=texts )

pylab.show()
            
