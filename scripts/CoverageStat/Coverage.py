#!/usr/local/bin/python
# -*- coding: utf-8 -*-  
import os,sys,linecache,time
from optparse import OptionParser
import numpy as np
import Coverage_module

#The script is to count the genomic coverage of each sample 
################################################################################################################################
#
# For help as a standalone program type: python Ct_Coverage.py   -h
#
# Usage:
#python Coverage.py  -i   $depthF   -o  $DepthStatF  -f  [ARTIC_Miseq|1k_Miseq|1k_MinION]	
################################################################################################################################


def main():
################################################################################################################################
# Parameters
################################################################################################################################
	usage = "usage:python  %prog [option]"
	parser = OptionParser(usage=usage)

	parser.add_option("-i","--inputpath",
	                  dest = "inputpath",
	                  default = "",
	                  metavar = "path",
	                  help = "Path to depth files generated from 'samtools depth' commond for all samples.  [required]")

	parser.add_option("-o","--outputfile",
	                  dest = "outputfile",
	                  default = "",
	                  metavar = "file",
	                  help = "output file,Statistics of Genome coverage of loci with output depth >= 10X for all samples [required]")
	parser.add_option("-f","--sampFlag",
	                  dest = "sampFlag",
	                  help = "sampFlag [ 1k_minION | 1k_miseq  |  400_Miseq ]  [required]")

	(options,args) = parser.parse_args()
	depthpath       = os.path.abspath(options.inputpath)
	outCoverageStatF = os.path.abspath(options.outputfile)
	sampFlag   = options.sampFlag

	startTime = time.time()

	print "input path :  " + depthpath
	print "output file   : " + outCoverageStatF
	head=Coverage_module.outHead()
	if (os.path.exists(outCoverageStatF)):
		os.remove(outCoverageStatF)
	defFO = open(outCoverageStatF,'a')
	defFO.write(head + "\n")
	defFO.close()

	filenameLst = Coverage_module.fileLst(depthpath)
	for depthF in filenameLst:
		samp = depthF.split("/")[-1].split(".txt")[0]	
		print  "Calculating for sample:   " + samp
		meanDepth = Coverage_module.meandepth(depthF)
		sampCovOut = Coverage_module.CovStat(samp,depthF,sampFlag,meanDepth)
		defFO = open(outCoverageStatF,'a')
		defFO.write(sampCovOut + "\n")
		defFO.close()

	endTime = time.time()
	print "Total samples: " + str(len(filenameLst))
	sys.stdout.write("Total time taken: "+str(endTime-startTime)+" seconds\n")



if __name__ == "__main__":
	main()



