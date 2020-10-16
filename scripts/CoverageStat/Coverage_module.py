#!/usr/local/bin/python
# -*- coding: utf-8 -*-  
import os,sys,linecache
import numpy as np


def fileLst(depthpath):
	filenameLst=[]
	for filename in os.listdir(depthpath):
		filenameLst.append(depthpath + "/" + filename)
	print filenameLst
	return filenameLst

def outHead():	
	headLst = []
	headLst.append("sample")
	headLst.append("flag")
	headLst.append("Cov10X")
	headLst.append("perct_100X")
	headLst.append("perct_1000X")
	headLst.append("mean")
	headLst.append("median")
	headLst.append("Q1")
	#headLst.append("Q2")	
	headLst.append("Q3")
	headLst.append("mean10p")
	headLst.append("mean20p")	
	headLst.append("mean30p")
	head = "\t".join(headLst)
	return head


def meandepth(defF):
	depLst = []
	for defFl  in  open(defF).readlines():
		dep = int(defFl.split("\t")[2])
		depLst.append(dep)
	meanDepth = round(np.mean(depLst),2)
	return  meanDepth

def CovStat(samp,defF,sampFlag,meanDepth):
	if  "1k" in sampFlag:
		Targt_genomLen = 29848 - 30
		startPosi = 30
		endposi = 29848
	if  "ARTIC" in sampFlag:
		Targt_genomLen = 29866 - 30
		startPosi = 30
		endposi = 29866	
	depLst = []
	dayu_10Xcount = 0
	dayu_100Xcount = 0
	dayu_1000Xcount = 0
	dayu_mean10PertCount = 0
	dayu_mean20PertCount= 0
	dayu_mean30PertCount = 0
	defFls = open(defF).readlines()
	for defFl in defFls:
		posi = defFl.split("\t")[1]
		dep = int(defFl.split("\t")[2])
		if  int(posi) >= startPosi and int(posi)  <= endposi :
			depLst.append(dep)
			if dep >= 10:
				dayu_10Xcount += 1
			if dep >= 100:
				dayu_100Xcount += 1
			if dep >= 1000:
				dayu_1000Xcount += 1	
			if dep >= meanDepth * 0.1:
				dayu_mean10PertCount += 1
			if dep >= meanDepth * 0.2:
				dayu_mean20PertCount += 1
			if dep >= meanDepth * 0.3:
				dayu_mean30PertCount += 1
	dayu_10X_Percent = round(float(dayu_10Xcount)*100/Targt_genomLen,2)
	dayu_100X_Percent = round(float(dayu_100Xcount)*100/Targt_genomLen,2)
	dayu_1000X_Percent = round(float(dayu_1000Xcount)*100/Targt_genomLen,2)
	dayu_mean10Pert = round(float(dayu_mean10PertCount)*100/Targt_genomLen,2)
	dayu_mean20Pert = round(float(dayu_mean20PertCount)*100/Targt_genomLen,2)
	dayu_mean30Pert = round(float(dayu_mean30PertCount)*100/Targt_genomLen,2)
	a = depLst

	mean = round(np.mean(a),2)
	median = round(np.median(a),2)
	dp_1_4=int(np.percentile(a,25))
	#dp_1_2=int(np.percentile(a,50))
	dp_3_4=int(np.percentile(a,75))

	OUTLst = []
	
	OUTLst.append(str(samp))
	OUTLst.append(sampFlag)
	OUTLst.append(str(dayu_10X_Percent))
	OUTLst.append(str(dayu_100X_Percent))
	OUTLst.append(str(dayu_1000X_Percent))
	OUTLst.append(str(mean))
	OUTLst.append(str(median))
	OUTLst.append(str(dp_1_4))
	#OUTLst.append(str(dp_1_2))	
	OUTLst.append(str(dp_3_4))
	OUTLst.append(str(dayu_mean10Pert))
	OUTLst.append(str(dayu_mean20Pert))
	OUTLst.append(str(dayu_mean30Pert))

	out = "\t".join(OUTLst)
	return out




