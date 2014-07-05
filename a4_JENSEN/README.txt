Authorship Attribution for the Federalist Papers

	Folder containing the .py and .csv files (the .xml and .txt source files for the Federalist Papers are excluded and the corresponding path commented out) for running machine learning techniques (specifically cluster analysis through numpy/scipy) on the Federalist Papers for authorship attribution purposes.

================================================================

FILES:

Figures:
	Foldering containing the resultant .png files from the cluster analysis, for use in the final report.

a4_Jensen_FeatureMaker.py:
	Python file for creating feature sets out of .txt files. Creates an MxN array of Words x Documents for use in the cluster analysis.

a4_Jensen_Dendrogram.py:
	Python file for using the feature sets in cluster analysis. Implements numpy and scipy along with matplotlib's pylab.

*.csv:
	Various .csv files as feature sets from the 		     a4_Jensen_FeatureMaker.py file.

Final Report:
	Final paper detailing findings of the cluster analysis in the authorship attribution of the disputed Federalist Papers.

=================================================================

Notes on design/implementation:

-	Only unsupervised techniques are implemented as technical issues prevented the use of either CART or Mallet. As such, the final report is incomplete.

-	Source code is largely uncommented as it is simply code to take .txt files and convert to a format usable by the numpy and scipy modules (.csv).