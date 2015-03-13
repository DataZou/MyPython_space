#!/usr/bin/python
'''
Desc:This script screening wdsp results by the condition:
Condition: if tetradNum > 0, score >= 48;else score >= 60
Usage: python wdsp_result_screening.py wdsp_result.out
Author:Xu-Dong Zou
Time:2015-03-13
'''
import sys

#read the parameters from parameters.txt to get addition score for each repNum 
parameter = {}
fhi = open("parameters.txt")
for line in fhi:
	line = line.strip()
	if "blade num" in line:
		break
for line in fhi:
	if "=" in line:
		line = line.strip()
		words = line.split()
		parameter[words[0]] = float(words[2])
	else:
		break
fhi.close()

#deal with result file of wdsp
tetrad_num = {}
tetrad_score = {}
output = {}
entry = ''
ave_score = 0.0 #the total average score at ">" line
repNum = 0
fhi = open(sys.argv[1]) #input wdsp result file
fho = open("WD40s_6_48.out",'w') #output file (change to your own)
for line in fhi.readlines():
	words = line.split()
	if line[0]==">":
		if len(words)==4:  #only interested in entries that have beta sheet
			entry = words[1]
			ave_score = float(words[2])
			repNum = int(words[3])
			tetrad_score[entry] = 0.0
			tetrad_num[entry] = 0
			output[entry] = ''
	elif len(words)>3:
		output[entry] += line
		tetrad_score[entry] += float(words[-1])
		if float(words[-1]) >= 28.0:
			tetrad_num[entry] += 1
	else:
		if ave_score > 0 and repNum >= 6: #only interested in entries with ave_score lager than 0
			score = ave_score - tetrad_score[entry] - parameter[str(repNum)]
			if tetrad_num > 0:
				if score/repNum >= 48:
					print >>fho,"> %s %.2f %d" % (entry,ave_score,repNum)
					print >>fho,output[entry]
					entry = ''
					ave_score = 0.0
					repNum = 0
			else:
				if score/repNum >= 60:
					print >>fho,"> %s %.2f %d" % (entry,ave_score,repNum)
					print >>fho,output[entry]
					entry = ''
					ave_score = 0.0
					repNum = 0
fhi.close()
fho.close()
