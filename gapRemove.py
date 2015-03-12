#!/usr/bin/env python
'''
Desc:This scripts process multiple alignment file by clustalw
Desc: and removes some sites which have too many gaps.
Usage: python gapRemove.py input.aln output.aln
Coder:Xu-Dong Zou
Time: 2015-03-12
'''

import sys
import math
import numpy as np

fh = open(sys.argv[1]) # input a alignment file of clustalw format: xx.aln
head1 = fh.readline()
fh.readline()
fh.readline()

msa = {} #define a dictionary to store each seq in multiple seqs alignment
for line in fh.readlines():
	line = line.strip()
	if len(line)> 1:
		uid,seq = line.split()
		if uid not in msa:
			msa[uid] = seq
		else:
			msa[uid] += seq
fh.close()

arr2d = [] #a two dimension array to store the msa,first dim represents a seqs
for k in msa:
	arr = list(msa[k]) # transform a seq(a string) into a list
	arr.insert(0,k) #insert the seq id into the start of the list
	arr2d.append(arr) # build a list of list 

ndarr = np.array(arr2d) # build a 2d array
ndarrT = ndarr.T #transpose the 2d array

print "Number of sequence input: %d" % (ndarr.shape[0])
print "Alignment sequence length: %d" % (ndarr.shape[1]-1)
print "Processing ..."

removeArr = []
#print "pre process:",ndarrT.shape
gapSta = np.zeros(ndarrT.shape[0]-1)
for i in range(1,ndarrT.shape[0]):
	arr = ndarrT[i,]
	#gapSta[i-1] = len(arr[arr=="-"])
	if len(arr[arr=="-"]) >= 1200: #change this number according to your seqs
		removeArr.append(i)
ndarrT = np.delete(ndarrT,removeArr,0)
#print "The minimum gap:",gapSta.min()
#print "The mean number of gap:",gapSta.mean()
#print "The maximum gap:",gapSta.max()
#print "Number of sites that with less than 1200 gaps:",len(gapSta[gapSta<1200])
#print "Post process:",ndarrT.shape
ndarrFinal = ndarrT.T

#Output as clustal format *.aln#
fho = open(sys.argv[2],'w')# output file
head1 = head1.strip()
print >>fho,head1
print >>fho,""
print >>fho,""
for r in range(int(math.ceil(float(ndarrFinal.shape[1])/60))):
	for i in range(ndarrFinal.shape[0]):
		s = r*60+1
		e = (r+1)*60
		if e <= ndarrFinal.shape[1]-1:
			arr = ndarrFinal[i,s:e+1]
			aline = ''.join(arr)
		else:
			arr = ndarrFinal[i,s:]
			aline = ''.join(arr)
		rowFlag = ndarrFinal[i,0] + ' '*(20-len(ndarrFinal[i,0]))
		print >>fho,"%s%s" % (rowFlag,aline)
	print >>fho,""
	print >>fho,""
fho.close()


print "Number of sequence input: %d" % (ndarrFinal.shape[0])
print "Sequence length: %d" % (ndarrFinal.shape[1]-1)
print "Complete!"
'''
#output as text file#
for i in range(ndarrFinal.shape[0]):
	arr = ndarrFinal[i,1:]
	aline = ''.join(arr)
	rowFlag = ndarrFinal[i,0] + ' '*(20-len(ndarrFinal[i,0]))
	print "%s%s" % (rowFlag,aline)
'''
