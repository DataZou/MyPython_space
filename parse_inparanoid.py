#!/usr/bin/env python
'''
Desc:this script parse text file that INPARANOID generated,e.g. Output.A.thaliana-H.sapiens
Usage: python parse_inparanoid.py inputFile
Time:2015-3-30
Author: Zou Xu-Dong
'''
import sys

def parseInparanoid(filename):
	fh = open(filename,'r')
	while True: #pass the meta info
		head = fh.readline()
		head = head.strip()
		if head == 83*'_':
			break
		else:
			pass
	
	inparalogA = []
	inparalogB = []
	for line in fh.readlines():
		line_org = line
		line = line.strip()
		if line.startswith("Group of"):
			groupNum = line.split(" ")[3]
		elif line.startswith("Score difference"):
			pass
		elif line.startswith("Bootstrap"):
			pass
		elif line == 83*"_":
			print "%s\t%s" % (inparalogA,inparalogB)
			inparalogA = []
			inparalogB = []
		else:
			words = line.split()
			words = [f for f in words if len(f) > 0]
			if len(words) == 4:
				inparalogA.append((words[0],words[1]))
				inparalogB.append((words[2],words[3]))
			#	print "%s\t%s\t%s\t%s" % (seqA,btA,seqB,btB)
			elif len(words) == 2:
				if line_org.startswith(" "):
					inparalogB.append((words[0],words[1]))
					#print "%s\t%s\t%s\t%s\t%d" % (seqA,btA,seqB,btB,len(words))
					#print "%s\t%s\t%d" % ("--",btA,len(words))
				else:
					inparalogA.append((words[0],words[1]))
					#print "%s\t%s\t%s\t%s\t%d" % (seqA,btA,seqB,btB,len(words))
	print "%s\t%s" % (inparalogA,inparalogB)
	fh.close()

def main():
	inputFile = sys.argv[1]
	parseInparanoid(inputFile)

if __name__ == '__main__':
	main()
