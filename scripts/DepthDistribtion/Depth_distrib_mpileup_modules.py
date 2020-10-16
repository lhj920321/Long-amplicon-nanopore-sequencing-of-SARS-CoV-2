#!/usr/local/bin/python
# -*- coding: utf-8 -*- \
import os,sys,linecache
import numpy as np
###############
#modules
###############


def fileLst(depthpath):
	filenameLst=[]
	for filename in os.listdir(depthpath):
		filenameLst.append(depthpath + "/" + filename)
	return filenameLst


def depStat(filenameLst):
	genomLen = 29903
	allFileMeandepDic = {}
	outDic = {}
	for depthF in filenameLst:
		defFls = open(depthF).readlines()
		depLst = []
		for defFl in defFls:		
			posi = defFl.split("\t")[1]
			if posi not in outDic:
				outDic[int(posi)] = []
			dep = int(defFl.split("\t")[2])
			depLst.append(dep)
		filemeanDep = round(np.mean(depLst),2)
		allFileMeandepDic[depthF] = filemeanDep

	filePosNmlzedCovDic = {}
	
	

	for depthF in filenameLst:
		#filePosNmlzedCovDic[depthF] = []
		defFls = open(depthF).readlines()
		for defFl in defFls:
			posi = defFl.split("\t")[1]
			dep = int(defFl.split("\t")[2])
			#NormalizedCov = round(float(dep)/allFileMeandepDic[depthF],2)
			#filePosNmlzedCovDic[depthF].append(NormalizedCov)
			outDic[int(posi)].append(dep)
	outLst = []
	#for position in xrange(1,29904):
	for position in xrange(1,29904):
		#print max(outDic[position])
		if position in outDic:			
			dp_1_4=int(np.min(outDic[position]))
			#dp_1_4=int(np.percentile(outDic[position],25))
			#flag = "1_4"
			#outline = str(position) + "\t" +  flag + "\t" + str(dp_1_4)
			#outLst.append(outline)
	
			#posiMeanC = int(np.mean(outDic[position]))
			#flag = "mean"
			#outline = str(position) + "\t" +  flag + "\t" + str(posiMeanC)
			#outLst.append(outline)
	
			dp_1_2=int(np.percentile(outDic[position],50))
			#flag = "1_2"
			#outline = str(position) + "\t" +  flag + "\t" + str(dp_1_2)
			#outLst.append(outline)
			dp_3_4=int(np.max(outDic[position]))
			#dp_3_4=int(np.percentile(outDic[position],75))
			#flag = "3_4"
		else:
			dp_1_4 = 0
			dp_1_2 = 0
			dp_3_4 = 0
		outline = str(position) + "\t" + str(dp_1_4) + "\t" + str(dp_1_2) + "\t" + str(dp_3_4)
		outLst.append(outline)
	
	out = "\n".join(outLst)


	return out





def outHead():	
	headLst = []
	#headLst.append("samp")
	headLst.append("posi")
	headLst.append("min")
	headLst.append("Q2")
	headLst.append("max")
	head = "\t".join(headLst)
	return head












