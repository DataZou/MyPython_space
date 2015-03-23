#!/usr/bin/env python
'''
Desc:convert a clustal format msa file (*.aln) into an interleaved phylip msa file (*.phi)
Usage:python clustal2phylip.py inFile.aln outFile.phi 
'''

import sys
import math
import numpy as np

fh = open(sys.argv[1]) # input a file with surfix .aln
head = fh.readline()
fh.readline()
fh.readline()
originalOrd = []
msa = {}
for line in fh.readlines():
	line = line.strip()
	if len(line) > 1:
		uid,seq = line.split()
		if uid not in msa:
			msa[uid] = seq
			originalOrd.append(uid)
		else:
			msa[uid] += seq
fh.close()

for k in originalOrd:   #add sequence ID to each sequence
	msa[k] = k[0:10] + msa[k]

def splitByWidth(string,width):
	return [string[x:x+width] for x in range(0,len(string),width)]

fho = open(sys.argv[2],'w')
seqLen = len(msa[originalOrd[0]])
print >>fho,len(originalOrd),seqLen
for r in range(int(math.ceil(seqLen/60.0))):
	s = r*60
	e = (r+1)*60
	if e <= seqLen:
		for k in originalOrd:
			subSeq = msa[k][s:e]
			print >>fho,"%s %s %s %s %s %s" % (subSeq[0:10],subSeq[10:20],subSeq[20:30],subSeq[30:40],subSeq[40:50],subSeq[50:60])
	else:
		for k in originalOrd:
			subSeq = msa[k][s:]
			outSeq = splitByWidth(subSeq,10)
			outStr = ' '.join(outSeq)
			print >>fho,outStr

fho.close()
